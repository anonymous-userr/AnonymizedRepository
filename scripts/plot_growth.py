#Plot release, package and dependency growth
import pandas as pd
import matplotlib.pyplot as plt

file1 = r"/path to dataset/vertex_GAV.csv"
df1 = pd.read_csv(file1)
file2 = r"/path to dataset/vertex_GA.csv"
df2 = pd.read_csv(file2)
file3 = r"/path to dataset/Edges_GAV.csv"
df3 = pd.read_csv(file3)
file4 = r"/path to dataset/Edges_GA.csv"
df4 = pd.read_csv(file4)

#platforms to plot
selected_platforms = ["Maven", "NPM", "Pypi", "CPAN", "Cargo", "CRAN", "Packagist", "NuGet"]
start_years = {
    "Cargo": 2014, "Packagist": 2011, "NuGet": 2011,
    "NuGet": 2011, "Packagist": 2011, "Pypi": 2008,
    "Cargo": 2015, "NPM": 2010
}
default_start_year = 1995

# colors and lines
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#ff6600', '#6600ff']
linestyle = '-'
linewidth = 5

plt.figure(figsize=(26, 12), dpi=600)

for i, platform in enumerate(selected_platforms):
    start_year = start_years.get(platform, default_start_year)
    platform_df1 = df1[(df1['Platform'] == platform) & (df1["Release Year"] >= start_year)].sort_values(by="Release Year")
    if not platform_df1.empty:
        plt.plot(platform_df1["Release Year"], platform_df1["Vertex Count"],
                 label=f"{platform}", color=colors[i], linestyle=linestyle, linewidth=linewidth, marker='o', markersize=15)

for i, platform in enumerate(selected_platforms):
    start_year = start_years.get(platform, default_start_year)
    platform_df2 = df2[(df2['Platform'] == platform) & (df2["Year"] >= start_year)].sort_values(by="Year")
    if not platform_df2.empty:
        plt.plot(platform_df2["Year"], platform_df2["GA Count"],
                 label=f"{platform}", color=colors[i], linestyle=linestyle, linewidth=linewidth, marker='o', markersize=15)

for i, platform in enumerate(selected_platforms):
    start_year = start_years.get(platform, default_start_year)
    platform_df3 = df3[(df3['Platform'] == platform) & (df3["Release Year"] >= start_year)].sort_values(by="Release Year")
    if not platform_df3.empty:
        plt.plot(platform_df3["Release Year"], platform_df3["Vertex Count"],
                 label=f"{platform}", color=colors[i], linestyle=linestyle, linewidth=linewidth, marker='o', markersize=15)

for i, platform in enumerate(selected_platforms):
    start_year = start_years.get(platform, default_start_year)
    platform_df4 = df4[(df4['Platform'] == platform) & (df4["Release Year"] >= start_year)].sort_values(by="Release Year")
    if not platform_df4.empty:
        plt.plot(platform_df4["Release Year"], platform_df4["Vertex Count"],
                 label=f"{platform}", color=colors[i], linestyle=linestyle, linewidth=linewidth, marker='o', markersize=15)

plt.yscale("log")

plt.xlabel("Release Year", fontsize=28, fontweight="bold", labelpad=15)
plt.ylabel("Graph Size", fontsize=28, fontweight="bold", labelpad=15)

plt.title("Graph Sizes Across Years", fontsize=32, fontweight="bold", pad=25)

plt.legend(loc="upper left", fontsize=26, frameon=True, shadow=True)

plt.grid(True, linestyle="--", linewidth=1.2, alpha=0.8)

plt.xticks(list(range(1995, 2021, 2)) + [2020], rotation=45, fontsize=24)
plt.yticks(fontsize=22)

plt.xlim(1995, 2020.5)

plt.tight_layout()
plt.show()


