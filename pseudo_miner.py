import hashlib
import datetime
import json
import time
import multiprocessing

DIFFICULTY = "00000"

BLOCK = {
  "id": 0,
  "nonce": 0,
  "time": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
  "transactions": [1, 2, 3]
}

def mine(block: dict, queue, p_id, p_max):
  block["nonce"] = p_id - 1
  block_nonce = block["nonce"]
  
  block_prefix = f'{{"id": {block["id"]}, "nonce": '.encode("utf-8")
  block_suffix = f', "time": "{block["time"]}", "transactions": {json.dumps(block["transactions"])}}}'.encode("utf-8")
  
  sha256 = hashlib.sha256
  bytes_difficulty = bytes.fromhex(DIFFICULTY[:(len(DIFFICULTY) // 2) * 2])
  
  start_time = time.perf_counter()
  
  while True:
    bytes_block = block_prefix + f"{block_nonce}".encode("ascii") + block_suffix
    bytes_hash_block = sha256(bytes_block).digest()
    
    if bytes_hash_block.startswith(bytes_difficulty):
      hash_block = bytes_hash_block.hex()
      if hash_block.startswith(DIFFICULTY):
        end_time = time.perf_counter()
        duration = max(end_time - start_time, 0.000001)
        queue.put((p_id, hash_block, bytes_block.decode("utf-8"), block_nonce // duration))
        return
    
    block_nonce += p_max

if __name__ == "__main__":
  PROCESSES_COUNT = multiprocessing.cpu_count()
  
  queue = multiprocessing.Queue()
  processes = []
  
  for i in range(PROCESSES_COUNT):
    p = multiprocessing.Process(target=mine, args=(BLOCK, queue, i+1, PROCESSES_COUNT))
    processes.append(p)
    p.start()
  
  p_id, hash_block, str_block, hashrate = queue.get()
  
  for p in processes:
    p.terminate()
    p.join()
  
  print(f"Process: {p_id}/{PROCESSES_COUNT}")
  print(f"Block: {str_block}")
  print(f"Hash: {hash_block}")
  print(f"Total Hashrate: {hashrate:,.0f} H/s")
