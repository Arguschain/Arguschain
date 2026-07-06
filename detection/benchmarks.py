"""Performance benchmarking utilities."""

import time

class BenchmarkTimer:
    """Simple timer for benchmarking."""
    
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        elapsed = time.time() - self.start
        print(f"{self.name}: {elapsed:.3f}s")
