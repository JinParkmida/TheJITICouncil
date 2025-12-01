import sys
import os
import time

# Add src to pythonpath
sys.path.insert(0, os.path.abspath("src"))

from jiti import jiti_implementation
from jiti.holocron import Holocron

# Clear cache for testing
if os.path.exists("holocron.json"):
    os.remove("holocron.json")
    print("🧹 Cleared Holocron.")

print("🧪 Starting JITI Verification...")

@jiti_implementation
def fibonacci(n: int) -> int:
    """
    Returns the nth Fibonacci number.
    0, 1, 1, 2, 3, 5, 8...
    """
    pass

print("\n--- Round 1: The Council Convenes (First Run) ---")
start = time.time()
try:
    result = fibonacci(10)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    # If Ollama is not running or model is missing, this might fail.
    # We'll catch it to show the user what happened.
    print("⚠️  (If this failed, ensure Ollama is running with 'qwen2.5-coder')")

print(f"Time taken: {time.time() - start:.4f}s")

print("\n--- Round 2: The Holocron (Cached Run) ---")
start = time.time()
try:
    result = fibonacci(10)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
print(f"Time taken: {time.time() - start:.4f}s")

# Verify cache file exists
if os.path.exists("holocron.json"):
    print("\n✅ Holocron exists.")
else:
    print("\n❌ Holocron was not created.")
