import numpy as np
import pandas as pd
import os 

print(os.getcwd())

data = pd.read_excel("./Equiment.xlsx")

model_data = open("./equipment.json", "w")

model_data.write("[\n")

type_dict = {
    "PC/Laptop": "PC",
    "VR Headset": "VRH",
    "Camera/Sensors": "CS",
    "PC Peripherals": "PP",
    "Furniture": "Furn",
    "Tripod": "Trip",
    "Other": "Oth",
    "VR Controller": "VRC",
    "Phones/Tablets": "PT",
    "Power/Cable": "PCBL"
}


status_choices = {
        "Pending": "Pend",
        "Available": "Avail", 
        "Decommisioned ": "Decom",
        "Unavailable": "Unavail", 
        "On_loan": "Loan",
        "Repairing": "Repair",
        np.nan: "Avail"
 }
count = 0 
MODEL_NAME = "Bookings.Equipment"
for index, row in data.iterrows(): 
    model_data.write(",{")
    model_data.write(f' "model" : "{MODEL_NAME}" ,')
    model_data.write(f' "pk" : {count},')
    model_data.write(' "fields" : {')
    model_data.write(f'      "name": "{row["Device Name"].title()}",')
    model_data.write(f'      "type": "{type_dict[row["Device Type"]]}",')
    model_data.write(f'      "status": "{status_choices[row["Status"]]}",')
    model_data.write(f'      "location": "{row["Location"]}",')
    model_data.write(f'      "comment": "{" " if row["Comments"] == np.nan else row["Comments"] }",')
    model_data.write(f'      "quantity": {row["Quantity"]},')
    model_data.write(f'      "last_audit": "{row["Audit"].strftime('%Y-%m-%d')}"')
    model_data.write('  }')
    model_data.write('}\n')

    count += 1
model_data.write("]\n")



model_data.close()
