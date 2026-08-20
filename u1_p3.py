import os 
from dotenv import load_dotenv
load_dotenv()
a=os.getenv("API_KEY")
b=os.getenv("API_URL")

if a:
    mask=""
    for i, c in enumerate(a):
        if i<len(a)-4:
            mask+="*"
        else:
            mask+=c

    print("API KEY:",mask)
else:
    print("API key absent.")
if b:
    print("API URL:",b)
else:
    print("API url absent.")

with open("requirements.txt", "r", encoding="utf-16") as file:
    lib=file.readlines()

req=""
dot=""
panda=""
for l in lib:
    if "requests" in l:
        req=l
    if "dotenv" in l:
        dot=l
    if "pandas" in l:
        panda=l

if req:
    print(req)
else:
    print("Requests is absent.")
if dot:
    print(dot)
else:
    print("Python Dotenv is absent.")
if panda:
    print(panda)
else:
    print("Pandas is absent.")
