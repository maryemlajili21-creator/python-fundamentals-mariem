import json
import csv
import yaml
import xml.etree.ElementTree as ET
from typing import TypedDict, NamedTuple
from dataclasses import dataclass
from pydantic import BaseModel
import numpy as np
import pandas as pd
import time

def main():
  
    users_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]

    # JSON
    with open("users.json", "w") as f:
        json.dump(users_data, f, indent=4)

    # CSV
    with open("users.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email"])
        writer.writeheader()
        writer.writerows(users_data)

    # YAML
    with open("users.yaml", "w") as f:
        yaml.dump(users_data, f)

    # XML
    root = ET.Element("users")
    for user in users_data:
        u = ET.SubElement(root, "user")
        for k, v in user.items():
            child = ET.SubElement(u, k)
            child.text = str(v)
    tree = ET.ElementTree(root)
    tree.write("users.xml")

    print("All files created: users.json, users.csv, users.yaml, users.xml")

   


    # TypedDict
    class UserTypedDict(TypedDict):
        id: int
        name: str
        email: str

    user_typed: UserTypedDict = {"id": 1, "name": "Alice", "email": "alice@example.com"}
    print("TypedDict:", user_typed)

    # NamedTuple
    class UserNamedTuple(NamedTuple):
        id: int
        name: str
        email: str

    user_named = UserNamedTuple(2, "Bob", "bob@example.com")
    print("NamedTuple:", user_named)

    # Dataclass
    @dataclass
    class UserDataClass:
        id: int
        name: str
        email: str

    user_dataclass = UserDataClass(3, "Charlie", "charlie@example.com")
    print("Dataclass:", user_dataclass)

    # Pydantic
    class UserPydantic(BaseModel):
        id: int
        name: str
        email: str

    user_pydantic = UserPydantic(id=4, name="David", email="david@example.com")
    print("Pydantic:", user_pydantic)

  
    py_list = [1, 2, 3, 4, 5]
    np_array = np.array([1, 2, 3, 4, 5])

    print("Python list:", py_list)
    print("NumPy array:", np_array)

  
    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} executed in {end - start:.6f} seconds")
            return result
        return wrapper


    @timer
    def python_list_mult(lst, scalar):
        return [x * scalar for x in lst]

    @timer
    def numpy_array_mult(arr, scalar):
        return arr * scalar

    print("\n--- Scalar-Vector Multiplication ---")
    python_list_mult(py_list, 10)
    numpy_array_mult(np_array, 10)


    df = pd.read_csv("users.csv")
    print("\nPandas DataFrame loaded from CSV:")
    print(df)


if __name__ == "__main__":
    main()
