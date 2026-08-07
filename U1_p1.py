model_name="gemini"
Temperature="10"
Maximum_tokens="10000"
API_Version="v1beta"

std={
    "name":"shamlu",
    "course":"pgdca",
    "semester":"1",
    "marks":"76"
    }

print(f"model_name: {model_name}")
print(f"Temperature: {Temperature}") 
print(f"Maximum_token: {Maximum_tokens}")
print(f"API_Version: {API_Version}")

for v in std.items():
 print(v[0],v[1])


a=int(input("update std marks :"))
std["marks"]=a
print(std)

file_name=(input("enter file name:"))
import os

fileName=input("Enter text file name: ")
l=fileName.rsplit(".",2)

if l[1]=="txt":
    if os.path.exists(fileName):
        print(f"File size: {os.path.getsize(fileName)} bytes")
        if os.path.getsize(fileName)==0:
            print("File empty.")
        else:
            print("File not empty.")
    else:
        print("File does not exists.")
else:
    print("Not a text file.")
