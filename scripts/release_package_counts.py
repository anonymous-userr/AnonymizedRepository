#Compute release, package and dependency counts
#releases
import pandas as pd
df = pd.read_csv("path to dataset\release_all_Libs.csv")
df['year'] = df['release'].str[:4].astype(int)

grouped_data = df.groupby(['Platform', 'year']).size().reset_index(name='count')
grouped_data.columns = ['Platform', 'Release Year', 'Vertex Count']
output_path = "path to dataset\vertex_GAV.csv"
grouped_data.to_csv(output_path, index=False)


#release edge
df = pd.read_csv("path to dataset\merged_final_output.csv")

df = df.dropna(subset=['source_release'])

df['year'] = df['source_release'].str[:4]
df = df[df['year'].str.isdigit()]
df['year'] = df['year'].astype(int)
grouped_data = df.groupby(['Platform', 'year']).size().reset_index(name='count')
grouped_data.columns = ['Platform', 'Release Year', 'Vertex Count']

output_path = "path to dataset\tbl\\Edges_GAV.csv"
grouped_data.to_csv(output_path, index=False)

#package releases
yearly_counts = {}

for chunk in pd.read_csv("path to dataset\merged_final_output.csv", chunksize=100000):
    chunk['source_release'] = chunk['source_release'].fillna('').astype(str)
    
    chunk['year'] = pd.to_numeric(chunk['source_release'].str[:4], errors='coerce').dropna().astype(int)
    platform = chunk['Platform'].iloc[0] if 'Platform' in chunk.columns else 'Unknown'
    chunk['platform'] = platform
    chunk = chunk.drop_duplicates(subset=['year', 'source', 'target'])
    yearly_counts_chunk = chunk.groupby(['platform', 'year']).size()
    for (platform, year), count in yearly_counts_chunk.items():
        yearly_counts[(platform, year)] = yearly_counts.get((platform, year), 0) + count

aggregated_counts = pd.DataFrame(
    [(platform, year, count) for (platform, year), count in yearly_counts.items()],
    columns=['Platform', 'Release Year', 'Vertex Count']
)

output_path = "path to dataset\Edges_GAV.csv"
aggregated_counts.to_csv(output_path, index=False)


#Packages edges


yearly_counts = {}

for chunk in pd.read_csv("path to dataset\merged_final_output.csv", chunksize=100000):
    chunk['source_release'] = chunk['source_release'].fillna('').astype(str)
    
    chunk['year'] = pd.to_numeric(chunk['source_release'].str[:4], errors='coerce').dropna().astype(int)    
    chunk['source_ga'] = chunk['source'].str.extract(r'^([^:]+:[^:]+)')[0]
    chunk['target_ga'] = chunk['target'].str.extract(r'^([^:]+:[^:]+)')[0]
    platform = chunk['Platform'].iloc[0] if 'Platform' in chunk.columns else 'Unknown'
    chunk['platform'] = platform
    chunk = chunk.drop_duplicates(subset=['year', 'source_ga', 'target_ga'])
    yearly_counts_chunk = chunk.groupby(['platform', 'year']).size()
    for (platform, year), count in yearly_counts_chunk.items():
        yearly_counts[(platform, year)] = yearly_counts.get((platform, year), 0) + count

aggregated_counts = pd.DataFrame(
    [(platform, year, count) for (platform, year), count in yearly_counts.items()],
    columns=['Platform', 'Release Year', 'Vertex Count']
)

output_path = "path to dataset\Edges_GA.csv"
aggregated_counts.to_csv(output_path, index=False)
