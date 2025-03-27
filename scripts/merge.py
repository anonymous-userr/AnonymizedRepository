#Clean and merge datasets
import pandas as pd

source_target_df = pd.read_csv("path to dataset\Links_all_Libs.csv")
artifact_release_df = pd.read_csv("path to dataset\release_all_Libs.csv")

artifact_release_df.rename(columns={'artifact': 'source'}, inplace=True)

merged_source = pd.merge(
    source_target_df,
    artifact_release_df,
    on=['source', 'Platform'],  
    how='left'
)

merged_source.rename(columns={'release': 'source_release'}, inplace=True)

artifact_release_df.rename(columns={'source': 'target'}, inplace=True)

merged_final = pd.merge(
    merged_source,
    artifact_release_df[['target', 'release', 'Platform']],
    on=['target', 'Platform'],  
    how='left'
)

merged_final.rename(columns={'release': 'target_release'}, inplace=True)

source_release_count = merged_final['source_release'].notnull().sum()
target_release_count = merged_final['target_release'].notnull().sum()

print(f'Number of populated fields in source_release: {source_release_count}')
print(f'Number of populated fields in target_release: {target_release_count}')

output_file_path = 'path to dataset\merged_final_output.csv'
merged_final.to_csv(output_file_path, index=False)

print(merged_final.head())

print(f'Total rows in merged dataset: {len(merged_final)}')
