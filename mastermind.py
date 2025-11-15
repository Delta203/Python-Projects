import random
import os
clear = lambda: os.system("cls")

MAX_GUESSES = 10
MAX_CODE_LENGTH = 4
DOT_MAIN = "⬤"
DOT_RIGHT_GUESS = "⦿ "
DOT_RIGHT_COLOR = "○ "
COLORS = {
  "R": f"\x1b[38;2;255;0;0m{DOT_MAIN}\x1b[0m",
  "G": f"\x1b[38;2;0;255;0m{DOT_MAIN}\x1b[0m",
  "B": f"\x1b[38;2;0;0;255m{DOT_MAIN}\x1b[0m",
  "O": f"\x1b[38;2;255;165;0m{DOT_MAIN}\x1b[0m",
  "Y": f"\x1b[38;2;255;255;0m{DOT_MAIN}\x1b[0m",
  "W": f"\x1b[38;2;255;255;255m{DOT_MAIN}\x1b[0m",
  "P": f"\x1b[38;2;255;192;203m{DOT_MAIN}\x1b[0m",
  "C": f"\x1b[38;2;0;255;255m{DOT_MAIN}\x1b[0m",
}

code = random.sample(list(COLORS.keys()), MAX_CODE_LENGTH)
game = []

def print_game(result: bool=False):
  for g in game:
    print(g)
  print()
  if result:
    print(" ".join(COLORS[c] for c in code))
  else:
    print(" ".join(COLORS.values()))

def is_guess_valid(guess: list) -> bool:
  if len(guess) != 4: return False
  if not all(g in COLORS for g in guess): return False
  return True

def guess_result(guess: list) -> str:
  right_guesses = [g for g, c in zip(guess, code) if g == c]
  right_colors = [g for g in list(set(guess) - set(right_guesses)) if g in code]
  return f"{DOT_RIGHT_GUESS * len(right_guesses)}{DOT_RIGHT_COLOR * len(right_colors)}"

guess_counter = 1
while guess_counter <= MAX_GUESSES:
  clear()
  print_game()
  print(f"Guess ({guess_counter}/{MAX_GUESSES}):")
  guess = input().upper().split()
  if not is_guess_valid(guess): continue
  result = guess_result(guess)
  game.append(f"{guess_counter}:\t{" ".join([COLORS[g] for g in guess])}\t{result}")
  guess_counter += 1
  if result == DOT_RIGHT_GUESS * MAX_CODE_LENGTH: break
clear()
print_game(True)