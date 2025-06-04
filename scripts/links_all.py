#pre-process the links_all dataset

import pandas as pd
input_csv_path = 'path to dataset/libraries-1.6.0-2020-01-12/dependencies-1.6.0-2020-01-12.csv'
final_output_path = 'path to dataset/links_all_Libs.csv'

selected_columns = [
    "Project Name",
    "Version Number",
    "Dependency Name",
    "Dependency Requirements"
]

chunk_size = 100000
write_header = True
processed_rows = 0

# Process/transform data in chunks
try:
    for chunk in pd.read_csv(input_csv_path, usecols=selected_columns, chunksize=chunk_size):
        chunk['source'] = chunk['Project Name'] + ":" + chunk['Version Number']
        chunk['target'] = chunk['Dependency Name'] + ":" + chunk['Dependency Requirements']
        chunk = chunk.drop(columns=['Project Name', 'Version Number', 'Dependency Name', 'Dependency Requirements'])
        chunk.to_csv(final_output_path, mode='a', header=write_header, index=False)
        write_header = False
        processed_rows += len(chunk)
        print(f"Processed {processed_rows} rows so far...")
except Exception as e:
    print(f"An error occurred: {e}")

print(f"Transformed data has been saved to {final_output_path}")
