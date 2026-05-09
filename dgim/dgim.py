from collections import deque
import os

class Bucket:
    def __init__(self, timestamp, size):
        self.timestamp = timestamp
        self.size = size

class DGIM:
    def __init__(self, window_size):
        self.N = window_size
        self.buckets = deque()  
        self.current_time = 0

    def update(self, bit):
        self.current_time += 1
        
        # drop oldder buckets 
        while self.buckets and self.buckets[-1].timestamp <= self.current_time - self.N:
            self.buckets.pop()

        # count only 1s
        if bit == 1:
            new_bucket = Bucket(self.current_time, 1)
            self.buckets.appendleft(new_bucket)
            self._merge_buckets()

    def _merge_buckets(self):
        i = 0
        while i < len(self.buckets) - 2:
            # check if the bucket size is same as the older two
            if (self.buckets[i].size == self.buckets[i+1].size == self.buckets[i+2].size):
                # erge the two oldest 
                self.buckets[i+1].size *= 2
                del self.buckets[i+2]
                continue 
            i += 1

    def estimate_count(self):
        if not self.buckets:
            return 0
            
        total_sum = 0
        for b in self.buckets:
            total_sum += b.size
            
        # main formula
        last_bucket_size = self.buckets[-1].size
        return int(total_sum - (last_bucket_size / 2))

def run_dgim_on_file(file_path, window_size):
    exact_window = deque(maxlen=window_size) 
    actual_ones = 0
    # read char by char in file and apply algo
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    dgim_manager = DGIM(window_size)
    
    print(f"Reading {file_path}...")
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            
            for char in chunk:
                if char in ('0', '1'):
                    bit = int(char)

                    dgim_manager.update(bit)

                    if len(exact_window) == window_size:
                        oldest_bit = exact_window[0]
                        if oldest_bit == 1:
                            actual_ones -= 1
                    
                    exact_window.append(bit)
                    if bit == 1:
                        actual_ones += 1

    # final print
    estimate = dgim_manager.estimate_count()
    print("-" * 30)
    print(f"Window Size:  {window_size}")
    print(f"DGIM Estimate: {estimate}")
    print(f"Actual Count:  {actual_ones}")
    
    if actual_ones > 0:
        error = abs(estimate - actual_ones) / (actual_ones * 100)
        print(f"Relative Error: {error:.6f}%")
    print("-" * 30)

if __name__ == "__main__":
    run_dgim_on_file('data.txt', 1000)