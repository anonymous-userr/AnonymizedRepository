#plot noise ratio
import pandas as pd
import matplotlib.pyplot as plt

artifact_file = "path to dataset\release_all_Libs.csv"
edge_file = "path to dataset\merged_final_output.csv"

artifact_chunks = pd.read_csv(artifact_file, sep=",", usecols=["Platform", "artifact"], chunksize=500000)

artifact_list = []
for chunk in artifact_chunks:
    chunk["component"] = chunk["artifact"].str.split(":").str[0]  
    artifact_list.append(chunk[["Platform", "component"]])

df_artifact = pd.concat(artifact_list, ignore_index=True)

edge_chunks = pd.read_csv(edge_file, sep=",", usecols=["Platform", "source", "target"], chunksize=500000)

source_list, target_list = [], []
for chunk in edge_chunks:
    chunk["source_component"] = chunk["source"].str.split(":").str[0]
    chunk["target_component"] = chunk["target"].str.split(":").str[0]
    source_list.append(chunk[["Platform", "source_component"]])
    target_list.append(chunk[["Platform", "target_component"]])

df_edges_source = pd.concat(source_list, ignore_index=True)
df_edges_target = pd.concat(target_list, ignore_index=True)

version_counts = df_artifact.groupby(["Platform", "component"])["component"].transform("count")
single_version_components = df_artifact[version_counts == 1]["component"].unique()

dependent_components = set(df_edges_target["target_component"].dropna().unique())

noise_components = {comp for comp in single_version_components if comp not in dependent_components}

total_components = df_artifact.groupby("Platform")["component"].nunique()
noise_count = df_artifact[df_artifact["component"].isin(noise_components)].groupby("Platform")["component"].nunique()

noise_ratio = (noise_count / total_components).fillna(0)

selected_platforms = ["Maven", "NPM", "Pypi", "CPAN", "Cargo", "CRAN", "Packagist", "NuGet"]
years = range(1995, 2020) 

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#6600ff']
platform_colors = dict(zip(selected_platforms, colors))

gini_values = {platform: [] for platform in selected_platforms}
for year in years:
    for platform in selected_platforms:
        value = noise_ratio.get(platform, 0)  
        gini_values[platform].append(value)

plt.figure(figsize=(14, 8), dpi=100)

for platform in selected_platforms:
    if platform in gini_values:
        plt.plot(years, gini_values[platform], marker='o', markersize=8, linewidth=2.5,
                 label=platform, color=platform_colors[platform])

plt.title('Noise Ratio per Platform', fontsize=22, fontweight='bold')
plt.xlabel('Year', fontsize=18, fontweight='bold')
plt.ylabel('Noise Ratio', fontsize=18, fontweight='bold')
plt.xticks(list(range(1995, 2020, 5)) + [2020], fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=16, loc='upper left', frameon=True)
plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)
plt.savefig('noise.png', dpi=600, bbox_inches='tight')
plt.show()
