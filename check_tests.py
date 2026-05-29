import os
import sys

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print("\nLooking for test files:")
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.startswith('test') and file.endswith('.py'):
            print(f"  {os.path.join(root, file)}")