import random
import multiprocessing

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def find_word(word: str, queue, p_id, debug: bool=False):
  random.seed()
  plain = []
  counter = 0
  
  while True:
    new_letter = random.choice(ALPHABET)
    if len(plain) == len(word):
      plain.pop(0)
    plain.append(new_letter)
    
    str_plain = "".join(plain)
    counter += 1
    
    if debug: print(str_plain)
    
    if str_plain == word:
      queue.put((p_id, counter))
      return

if __name__ == "__main__":
  WORD = "affe"
  PROCESSES_COUNT = multiprocessing.cpu_count()
  
  queue = multiprocessing.Queue()
  processes = []
  
  for i in range(PROCESSES_COUNT):
    p = multiprocessing.Process(target=find_word, args=(WORD, queue, i+1))
    processes.append(p)
    p.start()
  
  p_id, attempts = queue.get()
  
  for p in processes:
    p.terminate()
    p.join()
  
  print(f"Word: {WORD}")
  print(f"Process: {p_id}/{PROCESSES_COUNT}")
  print(f"Attempts: {attempts:,}")
