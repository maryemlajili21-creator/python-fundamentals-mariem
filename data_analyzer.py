import sys
if len(sys.argv) > 2:
        cli_name = sys.argv[1]
        cli_age = int(sys.argv[2])
        print(f"Command-line Name: {cli_name}")
        print(f"Command-line Age: {cli_age}")




# Variables
name = "mariem"         
age = 22                


fruits = ["apple", "banana", "orange", "strawberry"]  # list
person = {"name": "abir", "age": 25}                  # dictionary

# Fonction principale
def main():
    # Conditionals
    if age < 18:
        status = "minor"
    elif age < 65:
        status = "adult"
    else:
        status = "senior"

    # For loop
    print("Fruits in the list:")
    for idx, fruit in enumerate(fruits):   
        print(f"{idx+1}. {fruit}")

    # While loop
    counter = 0
    while counter < 3:
        print("Counter:", counter)
        counter += 1

    

    # Built-in functions
    for i in range(3):  # range
        print("Range value:", i)

    print("ID of age variable:", id(age))  # id()

    # String to int
    age_str = "22"
    age_int = int(age_str)  
    print("age:", age_int)

   
    from utils import greet
    message = greet(name)
    print(message)

  
    print("\n--- Running data_analyzer.py ---")
    print("Name:", name)
    print("Age:", age)
    print("Status:", status)
    print("Fruits:", fruits)
   


# Exécution du script
if __name__ == "__main__":
    main()