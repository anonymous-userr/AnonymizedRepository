#pre-process the release_all dataset

import pandas as pd

csv_file_path = 'path to dataset/libraries-1.6.0-2020-01-12/versions-1.6.0-2020-01-12.csv'

output_file_path = 'path to dataset/release_all_Libs.csv'

# Process in chunks
chunk_size = 100000
write_header = True
processed_rows = 0

for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
    chunk['artifact'] = chunk['Project Name'] + ":" + chunk['Number']

    chunk.rename(columns={'Published Timestamp': 'release'}, inplace=True)

    chunk = chunk[['Platform', 'artifact', 'release']]

    chunk.to_csv(output_file_path, mode='a', header=write_header, index=False)

    write_header = False

    processed_rows += len(chunk)
    print(f"Processed {processed_rows} rows so far...")

print(f"Processed data has been saved to {output_file_path}")


