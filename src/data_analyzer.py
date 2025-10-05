import sys
from typing import Any

# Variables
name: str = "mariem"
age: int = 22

fruits: list[str] = ["apple", "banana", "orange", "strawberry"]
person: dict[str, Any] = {"name": "abir", "age": 25}


def main() -> None:
    # Handle CLI args
    if len(sys.argv) > 2:
        cli_name: str = sys.argv[1]
        cli_age: int = int(sys.argv[2])
        print(f"Command-line Name: {cli_name}")
        print(f"Command-line Age: {cli_age}")

    # Conditionals
    if age < 18:
        status: str = "minor"
    elif age < 65:
        status = "adult"
    else:
        status = "senior"

    # For loop
    print("Fruits in the list:")
    for idx, fruit in enumerate(fruits):
        print(f"{idx+1}. {fruit}")

    # While loop
    counter: int = 0
    while counter < 3:
        print("Counter:", counter)
        counter += 1

    # Built-in functions
    for i in range(3):
        print("Range value:", i)

    print("ID of age variable:", id(age))

    # String to int
    age_str: str = "22"
    age_int: int = int(age_str)
    print("age:", age_int)

    print("\n--- Running data_analyzer.py ---")
    print("Name:", name)
    print("Age:", age)
    print("Status:", status)
    print("Fruits:", fruits)


if __name__ == "__main__":
    main()
