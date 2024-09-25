import os
import json

# Define the paths for the original and output folders
original_folder = "./config/"
output_folder = "./output/"

# Function to load JSON from a file
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to check the modifications between two files
def check_modifications(original_file, output_file):
    original_data = load_json(original_file)
    output_data = load_json(output_file)
    
    # Check if the only modification is in "checkTickersFrequency"
    for original_asset in original_data.get("underlyingAssets", []):
        asset_symbol = original_asset.get("assetSymbol", "")
        
        # Get checkTickersFrequency from both files
        original_frequency = original_data.get("checkTickersFrequency")
        output_frequency = output_data.get("checkTickersFrequency")
        
        # If asset ends with "USDT", check if the frequency is 10000
        if asset_symbol.endswith("USDT"):
            if output_frequency != 10000 or original_frequency == output_frequency:
                return False
        
        # For non-USDT assets, check if the frequency is 90000
        else:
            if output_frequency != 90000 or original_frequency == output_frequency:
                return False
    
    # Verify that there are no other differences
    # Exclude the checkTickersFrequency field and compare the rest
    original_data.pop("checkTickersFrequency", None)
    output_data.pop("checkTickersFrequency", None)
    
    # Check if the rest of the file is identical
    return original_data == output_data

# Function to iterate through all JSON files and verify
def verify_all_files():
    for filename in os.listdir(original_folder):
        if filename.endswith(".json"):
            original_file = os.path.join(original_folder, filename)
            output_file = os.path.join(output_folder, filename)
            
            # Skip if the output file doesn't exist
            if not os.path.exists(output_file):
                print(f"Output file for {filename} does not exist.")
                return False
            
            # Perform the comparison check
            if not check_modifications(original_file, output_file):
                print(f"Mismatch found in {filename}.")
                return False
    
    print("All files match the modification criteria.")
    return True

# Call the function and print the result
result = verify_all_files()
print("Verification result:", result)
