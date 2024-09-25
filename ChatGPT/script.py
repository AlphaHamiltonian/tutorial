import os
import json

# Define the input and output folders
input_folder = os.path.abspath("./tutorial/ChatGPT/config/")
output_folder = os.path.abspath("./tutorial/ChatGPT/output/")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to modify the JSON file based on assetSymbol
def modify_json(file_path, output_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    modified = False
    if "underlyingAssets" in data:
        for asset in data["underlyingAssets"]:
            if "assetSymbol" in asset:
                if asset["assetSymbol"].endswith("USDT"):
                    # Modify to 10000 if assetSymbol ends with USDT
                    data["checkTickersFrequency"] = 10000
                else:
                    # Modify to 90000 otherwise
                    data["checkTickersFrequency"] = 90000
                modified = True
    
    # If modified or no "checkTickersFrequency" key is found
    if modified or "checkTickersFrequency" not in data:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        # Copy the file without modification
        with open(file_path, 'r') as original, open(output_path, 'w') as copy:
            copy.write(original.read())

# Iterate over all JSON files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        modify_json(file_path, output_path)

print("All files have been processed and saved in the output folder.")
