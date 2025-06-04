#plot average releases
import pandas as pd
import re
import matplotlib.pyplot as plt

file_path = "C:path to dataset\release_all_Libs.csv"
df = pd.read_csv(file_path, delimiter=",", encoding="utf-8")  

platform_names = ["Maven", "NPM", "Pypi", "CPAN", "Cargo", "CRAN", "Packagist", "NuGet"]
df = df[df["Platform"].isin(platform_names)] 

df["Release Year"] = df["release"].astype(str).str[:4]
def extract_unversioned(artifact):
    if isinstance(artifact, str):  
        return re.sub(r":\d+(\.\d+)*$", "", artifact)  
    return artifact  

df["Unversioned Artifact"] = df["artifact"].apply(extract_unversioned)

total_releases = df.groupby(["Platform", "Release Year"])["Unversioned Artifact"].count().reset_index(name="Total Releases")

artifact_counts = (
    df.groupby(["Platform", "Release Year", "Unversioned Artifact"])['artifact']
    .count()
    .groupby(["Platform", "Release Year"])
    .mean()
    .reset_index(name="Average Release Count")
)

df_release = artifact_counts

# selected platforms
selected_platforms = ["Maven", "NPM", "Pypi", "CPAN", "Cargo", "CRAN", "Packagist", "NuGet"]

start_years = {"Cargo": 2015, "Packagist": 2011, "NuGet": 2011}
default_start_year = 1995  

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#ff6600', '#6600ff']
linestyle_release = '-'  
linewidth = 2.5

fig, ax2 = plt.subplots(figsize=(14, 6))
release_legend = []

for i, platform in enumerate(selected_platforms):
    start_year = start_years.get(platform, default_start_year)

    platform_release = df_release[(df_release['Platform'] == platform) & (df_release["Release Year"] >= start_year)]

    if not platform_release.empty:
        line2, = ax2.plot(platform_release["Release Year"], platform_release["Average Release Count"],
                          label=f"{platform}", color=colors[i],
                          linestyle=linestyle_release, linewidth=linewidth, marker='o', markersize=7)
        release_legend.append(line2)

ax2.set_ylabel("Average Release Count", color='black', fontsize=18, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='black', labelsize=14)
ax2.set_xlim(1995, 2020.5)
ax2.grid(True, linestyle="--", linewidth=0.8)

plt.title("Average Release Count", fontsize=22, fontweight='bold')

ax2.set_xlabel("Release Year", fontsize=18, fontweight='bold')

ax2.legend(handles=release_legend, loc="upper left", fontsize=12, title="Ecosystem", title_fontsize=14)

plt.xticks(list(range(1995, 2021, 2)) + [2020], rotation=45, fontsize=14)

plt.show()
