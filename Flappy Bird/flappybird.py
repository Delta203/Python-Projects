import random
import numpy as np
import pygame
import matplotlib.pyplot as plt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

WIDTH = 400
HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -8
GAME_SPEED = 1

PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 3

BIRD_RADIUS = 15
BIRD_NEURON_LAYERS = [5, 50, 30, 1]
BIRD_AMOUNT = 100
MUTATION_RATE = 0.05

pygame.init()
pygame.display.set_caption("Flappy Bird")

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT_SCORE = pygame.font.SysFont(None, 40)
FONT_STATS = pygame.font.SysFont(None, 25)

BIRD_FLAP_UP = pygame.image.load("assets/bird_flap_up.png")
BIRD_FLAP_UP = pygame.transform.scale(BIRD_FLAP_UP, (int(BIRD_FLAP_UP.get_size()[0] * BIRD_RADIUS / 6.9), int(BIRD_FLAP_UP.get_size()[1] * BIRD_RADIUS / 6.9)))
BIRD_FLAP_MIDDLE = pygame.image.load("assets/bird_flap_middle.png")
BIRD_FLAP_MIDDLE = pygame.transform.scale(BIRD_FLAP_MIDDLE, (int(BIRD_FLAP_MIDDLE.get_size()[0] * BIRD_RADIUS / 6.9), int(BIRD_FLAP_MIDDLE.get_size()[1] * BIRD_RADIUS / 6.9)))
BIRD_FLAP_DOWN = pygame.image.load("assets/bird_flap_down.png")
BIRD_FLAP_DOWN = pygame.transform.scale(BIRD_FLAP_DOWN, (int(BIRD_FLAP_DOWN.get_size()[0] * BIRD_RADIUS / 6.9), int(BIRD_FLAP_DOWN.get_size()[1] * BIRD_RADIUS / 6.9)))
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))
PIPE_IMAGE = pygame.transform.scale(pygame.image.load("assets/pipe.png"), (PIPE_WIDTH, HEIGHT))

class NeuralNetwork:
    def __init__(self, layer_sizes=[], weights=None, biases=None):
        self.weights = weights if weights is not None else []
        self.biases = biases if biases is not None else []
        if layer_sizes:
            for i in range(len(layer_sizes) - 1):
                self.weights.append(np.random.randn(layer_sizes[i], layer_sizes[i+1]))
                self.biases.append(np.zeros((1, layer_sizes[i+1])))

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, X):
        self.activations = [X]
        for i in range(len(self.weights)):
            X = self.relu(np.dot(X, self.weights[i]) + self.biases[i])
            self.activations.append(X)
        return X

    def mutate(self):
        for i in range(len(self.weights)):
            mask_weights = np.random.rand(*self.weights[i].shape) < MUTATION_RATE
            self.weights[i] += mask_weights * np.random.randn(*self.weights[i].shape) * 0.1
            mask_biases = np.random.rand(*self.biases[i].shape) < MUTATION_RATE
            self.biases[i] += mask_biases * np.random.randn(*self.biases[i].shape) * 0.1

class Bird:
    def __init__(self, neural_network):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.alive = True
        self.score = 0
        self.neural_network = neural_network
        self.learning_score = 0

    def draw(self):
        # pygame.draw.circle(SCREEN, GOLD, (self.x, int(self.y)), BIRD_RADIUS)
        BIRD_IMAGE = BIRD_FLAP_UP
        if self.velocity > 2: BIRD_IMAGE = BIRD_FLAP_MIDDLE
        if self.velocity < -2: BIRD_IMAGE = BIRD_FLAP_DOWN

        angle = -self.velocity * 5
        angle = max(min(angle, 25), -90)
        rotated_image = pygame.transform.rotate(BIRD_IMAGE, angle)
        rect = rotated_image.get_rect(center=(self.x, int(self.y)))
        SCREEN.blit(rotated_image, rect.topleft)

    def move(self):
        if self.alive:
            self.velocity += GRAVITY
            self.y += self.velocity
        else: self.x -= PIPE_SPEED

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def get_rect(self):
        return pygame.Rect(self.x - BIRD_RADIUS, self.y - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.passed = False

    def draw(self):
        # pygame.draw.rect(SCREEN, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # pygame.draw.rect(SCREEN, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))
        SCREEN.blit(PIPE_IMAGE, (self.x, self.height - PIPE_IMAGE.get_height()))
        SCREEN.blit(pygame.transform.flip(PIPE_IMAGE, False, True), (self.x, self.height + PIPE_GAP))

    def move(self):
        self.x -= PIPE_SPEED

    def get_rects(self):
        return [pygame.Rect(self.x, 0, PIPE_WIDTH, self.height), pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)]

def crossover(parent1_network, parent2_network):
    child_weights = []
    child_biases = []
    for parent1_weights, parent2_weights in zip(parent1_network.weights, parent2_network.weights):
        mask = np.random.rand(*parent1_weights.shape) < 0.5
        child_weights.append(np.where(mask, parent1_weights, parent2_weights))
    for parent1_biases, parent2_biases in zip(parent1_network.biases, parent2_network.biases):
        mask = np.random.rand(*parent1_biases.shape) < 0.5
        child_biases.append(np.where(mask, parent1_biases, parent2_biases))
    return NeuralNetwork(weights=child_weights, biases=child_biases)

def new_birds(birds, percentage=0.05):
    """This generates new birds based on a percentage of the best birds."""
    best_birds = sorted(birds, key=lambda bird: bird.learning_score, reverse=True)
    top_birds = best_birds[:max(2, int(len(best_birds) * percentage))]
    new_birds = []
    while len(new_birds) < len(birds):
        parent1, parent2 = random.sample(top_birds, 2)
        child_network = crossover(parent1.neural_network, parent2.neural_network)
        child_network.mutate()
        new_birds.append(Bird(child_network))
    return new_birds

def new_birds_top2(birds):
    """This generates new birds using the best two birds."""
    best_birds = sorted(birds, key=lambda bird: bird.learning_score, reverse=True)
    new_birds = []
    for _ in range(len(birds)):
        child_network = crossover(best_birds[0].neural_network, best_birds[1].neural_network)
        child_network.mutate()
        new_birds.append(Bird(child_network))
    return new_birds

running = True
birds = [Bird(NeuralNetwork(BIRD_NEURON_LAYERS)) for _ in range(BIRD_AMOUNT)]
generation_stats = []
highscore = 0

while running:
    birds = new_birds(birds)
    dead_birds = []
    pipes = [Pipe(WIDTH)]
    clock = pygame.time.Clock()

    while running:
        # SCREEN.fill(WHITE)
        SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

        for pipe in pipes:
            pipe.move()
            pipe.draw()

        if pipes[0].x + PIPE_WIDTH < 0:
            pipes.pop(0)

        if pipes[-1].x + PIPE_WIDTH < WIDTH // 2:
            pipes.append(Pipe(WIDTH))

        pipe_passed = False

        for bird in birds:
            bird.move()
            bird.draw()

            if not bird.alive: continue

            distance = pipes[0].x - bird.x
            pipe_top = pipes[0].height
            pipe_bottom = pipes[0].height + PIPE_GAP
            if distance + PIPE_WIDTH < 0:
                distance = pipes[1].x - bird.x
                pipe_top = pipes[1].height
                pipe_bottom = pipes[1].height + PIPE_GAP

            inputs = np.array([[bird.y, bird.velocity, distance, pipe_top, pipe_bottom]])
            if bird.neural_network.forward(inputs)[0, 0] > 10:
                bird.jump()

            if not pipes[0].passed and pipes[0].x + PIPE_WIDTH < bird.x:
                pipe_passed = True
                bird.score += 1
                bird.learning_score += 1

            if bird.y - BIRD_RADIUS < 0 or bird.y + BIRD_RADIUS > HEIGHT:
                bird.alive = False
                bird.learning_score -= 2

            for pipe_rect in pipes[0].get_rects():
                if bird.get_rect().colliderect(pipe_rect):
                    bird.alive = False
                    bird.learning_score -= 1

            if not bird.alive and bird not in dead_birds:
                dead_birds.append(bird)

        if pipe_passed: pipes[0].passed = True

        score = max(bird.score for bird in birds)
        if highscore < score: highscore = score

        score_text = FONT_SCORE.render(f"{score}", True, BLACK)
        score_text_rect = score_text.get_rect(center=(WIDTH / 2, 30))
        SCREEN.blit(score_text, score_text_rect)

        alive_birds_text = FONT_STATS.render(f"Birds: {len([bird for bird in birds if bird.alive])}", True, BLACK)
        SCREEN.blit(alive_birds_text, (10, HEIGHT - 75))
        highscore_text = FONT_STATS.render(f"Highscore: {highscore}", True, BLACK)
        SCREEN.blit(highscore_text, (10, HEIGHT - 50))
        generation_text = FONT_STATS.render(f"Generation: {len(generation_stats) + 1}", True, BLACK)
        SCREEN.blit(generation_text, (10, HEIGHT - 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(dead_birds) == len(birds): break
        pygame.display.update()
        clock.tick(60 * GAME_SPEED)

    scores = [bird.learning_score for bird in birds]
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)
    generation_stats.append({
        "generation": len(generation_stats) + 1,
        "max_score": max_score,
        "avg_score": avg_score
    })

pygame.quit()

generations = [stats["generation"] for stats in generation_stats]
max_scores = [stats["max_score"] for stats in generation_stats]
avg_scores = [stats["avg_score"] for stats in generation_stats]

plt.figure(figsize=(10, 6))
plt.plot(generations, max_scores, label="Max Learning Score", marker='o')
plt.plot(generations, avg_scores, label="Average Learning Score", linestyle='--')
plt.xlabel("Generation")
plt.ylabel("Learning Score")
plt.title("Generation Stats")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
