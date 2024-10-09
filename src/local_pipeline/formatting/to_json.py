import pandas as pd
import json
import os

# Define the base path (working directory)
CWD = os.getcwd()

# Load the CSV file
df = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'merged', 'merged_20000_rows.csv'))
df.fillna('Unknown', inplace=True)

def convert_to_json(df):
    output = []
    
    for _, row in df.iterrows():
        # Handle missing values for numeric columns
        accident = {
            "accidentID": int(row["index"]),
            "type": row["accidentType"],
            "severity": row["incidentSeverity"],
            "time": row["incidentTime"] if row["incidentTime"] != "Unknown" else "Unknown",  # If it's an unknown datetime
            "numVehicleInv": int(row["numVehiclesInvolved"]) if row["numVehiclesInvolved"] != "Unknown" else "Unknown",
            "policeReport": int(row["policeReportBool"]) if row["policeReportBool"] != "Unknown" else "Unknown",
        }
        
        driver = {
            "driverID": int(row["index"]),
            "licenceType": row["licenceType"],
            "experience": int(row["driverExperience"]) if row["driverExperience"] != "Unknown" else "Unknown",
            "age": int(row["driverAge"]) if row["driverAge"] != "Unknown" else "Unknown",
            "gender": int(row["driverGender"]) if row["driverGender"] != "Unknown" else "Unknown",
            "education": row["educationLevel"],
            "timeAsCustomer": row["timeAsCustomer"]
        }
        
        vehicle = {
            "vehicleID": int(row["index"]),
            "name": "Unknown",  # We don't have the vehicle name in the dataset
            "age": row["vehicleAge"]
        }
        
        insurance = {
            "insuranceID": int(row["index"]),
            "access": row["insuranceAccess"],
            "premium": row["insurancePremium"]
        }
        
        claim = {
            "claimID": int(row["index"]),
            "decision": int(row["fraud"]) if row["fraud"] != "Unknown" else "Unknown",
            "totalAmount": row["totalClaimAmount"],
            "accident": accident,
            "driver": driver,
            "vehicle": vehicle,
            "insurance": insurance
        }
        
        output.append(claim)
    
    return output

# Convert to JSON structure
json_data = convert_to_json(df)

# Save to a JSON file
os.makedirs(os.path.join(CWD, 'assets', 'data', 'json'), exist_ok=True)  # Ensure the directory exists
with open(os.path.join(CWD, 'assets', 'data', 'json', '20000_rows.json'), 'w') as f:
    json.dump(json_data, f, indent=4)

print("JSON file generated successfully!")
