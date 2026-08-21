import os
import pandas as pd

try:
    file_name = input("Enter file path: ").strip()

    if not os.path.exists(file_name):
        raise Exception(f"[ERROR]'{file_name}' file not exists!check file path.")

    else:
        ext = os.path.splitext(file_name)[1].lower()
        if ext == ".csv":
            print("this file is csv.")
            try:
                data=pd.read_csv(file_name)
            except:
                print("Error: EmptyCSV.")
        elif ext == ".json":
            print(" this file is json .")
            try:
                data=pd.read_json(file_name)
            except:
                print("Error: Invalid json")
        else:
            raise Exception(f"this file'{ext}' is format not aloow becouse only json or csv file allow!")

        print("Number of records:",len(data.index))
        print("Number of fields:",len(data.columns))
        print("name of columns:",data.columns)
        print("missing value:\n",data.isna().sum())
        print("Column data datatype:\n",data.dtypes)
        print("display the data summary:")
        data.info()
        data.describe().to_json("analysis.json", indent=4)

except Exception as e:
    print("Error: ", e)