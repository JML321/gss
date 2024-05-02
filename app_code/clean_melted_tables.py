import os
import pandas as pd

# Define the paths
input_folder_path = "../own_data_objects/melted_tables/"
output_folder_path = "../own_data_objects/cleaned_tables/"

# Ensure the output folder exists, create if it doesn't
os.makedirs(output_folder_path, exist_ok=True)

file_path = "../GSS_sas/Paradata_variables.txt"

# Load the words from the text file into a set for quick lookup
with open(file_path, 'r') as file:
    words_to_remove = set(line.strip() for line in file)

# Function to clean the CSV files
def clean_csv(input_file_path, output_file_path, words_to_remove):
    # Load the CSV file
    df = pd.read_csv(input_file_path)
    
    # Filter out the rows where the second column's value is in words_to_remove
    df = df[~df.iloc[:, 1].isin(words_to_remove)]
    
    # Save the cleaned CSV to the new output file path
    df.to_csv(output_file_path, index=False)

# Loop through all files in the input_folder_path that are CSVs
for filename in os.listdir(input_folder_path):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)
        clean_csv(input_file_path, output_file_path, words_to_remove)
        print(f"Cleaned and saved {filename} in cleaned_tables folder")
