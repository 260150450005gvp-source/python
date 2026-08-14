import json
import pandas as pd

a = int(input("Enter the number of students: "))

std = []
for i in range(a):
    print(f"Enter details for student {i + 1}")

    name = input("Student name: ")
    age = int(input("Age: "))
    course = input("Course: ")

    student = {
        "name": name,
        "age": age,
        "course": course
    }

    std.append(student)

file_name = "std.json"

with open(file_name, "w") as file:
    json.dump(std, file, indent=4)

with open(file_name, "r") as file:
    std_data = json.load(file)

print("All student information:")
for student in std_data:
    print(student)

df = pd.DataFrame(std_data)

print("DataFrame:")
print(df)

print("Last two student records:")
print(df.tail(2))

print("Column names:")
print(df.columns.tolist())

print("Column data:")
for column in df.columns:
    print(column)
    print(df[column])
print("Data types:")
print(df.dtypes)