##!/usr/bin/env python3
import sys
from .add import add

# commandline execute:
# >> cd ~/jenkins-terraform-k8s-secure/app
# >> python3 -m src.app 5 7

def main():
    # Expect exactly 2 arguments (excluding script name)
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]}  ")
        sys.exit(1)

    try:
        # Convert arguments to floats (works for integers too)
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
    except ValueError:
        print("Error: Both arguments must be numbers.")
        sys.exit(1)

    result = add(num1, num2)
    print(f"The sum of {num1} and {num2} is {result}")

if __name__ == "__main__":
    main()
  