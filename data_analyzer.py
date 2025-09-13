
import sys

# Vérifier si l'utilisateur a donné 2 arguments (nom et âge)
if len(sys.argv) < 3:
    print("Utilisation : python data_analyzer.py <nom> <âge>")
    sys.exit(1)

# Arguments de la ligne de commande
name = sys.argv[1]           # le premier argument = nom (exemple: "Mariem")
age = int(sys.argv[2])       # le deuxième argument = âge (exemple: 22)
# Variables

fruits = ["apple", "banana", "orange","strawberry"]  # list
person = {"name": "abir", "age": 25}    # dictionary

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

# Data structures
numbers = [10, 20, 30]           
coordinates = (5, 10)            
person_info = {"name": "Sara", "age": 28}  

# Built-in functions
for i in range(3):  # range
    print("Range value:", i)

print("ID of age variable:", id(age))  # id()


# String to int
age_str = "25"
age_int = int(age_str)  
print("age:", age_int)


from utils import greet
message = greet(name)
print(message)


if __name__ == "__main__":
    print("\n--- Running data_analyzer.py ---")
    print("Name:", name)
    print("Age:", age)
    print("Status:", status)
    print("Fruits:", fruits)

    print("Numbers:", numbers)
    print("Coordinates:", coordinates)
    print("Person info:", person_info)

