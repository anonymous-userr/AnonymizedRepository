#change in elites
import pandas as pd
import matplotlib.pyplot as plt
import os

category_colors = {"Top 10": "b", "Top 100": "g", "Top 500": "r"}

line_styles = {"Top 10": "-", "Top 100": "-", "Top 500": "-"}

fig, axes = plt.subplots(4, 4, figsize=(22, 15), sharey=True)
axes = axes.flatten()  

platforms_start_year = {
    "Maven": 2002, "NPM": 2010, "Pypi": 2005, "CPAN": 2002,
    "Cargo": 2014, "CRAN": 1999, "Packagist": 2011, "NuGet": 2011
}

data_folder = "path to dataset"

for i, (platform, start_year) in enumerate(platforms_start_year.items()):
    ax = axes[i]

    file_path = os.path.join(data_folder, "path to datset")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        ax.set_title(f"{platform} (No Data)", fontsize=12, color='red')
        ax.set_xticks(range(start_year, 2020, 2))  
        continue

    df = pd.read_csv(file_path)
    df_grouped = df.groupby(['aggregated_artifact', 'dependency_release_year'], as_index=False)['dependency_count'].sum()

    years = list(range(start_year, 2020))

    fractions = {"Top 10": [], "Top 100": [], "Top 500": []}
    prev_top = {"Top 10": set(), "Top 100": set(), "Top 500": set()}

    for year in years:
        year_data = df_grouped[df_grouped['dependency_release_year'] == year]

        top_10 = set(year_data.nlargest(10, 'dependency_count')['aggregated_artifact'])
        top_100 = set(year_data.nlargest(100, 'dependency_count')['aggregated_artifact'])
        top_500 = set(year_data.nlargest(500, 'dependency_count')['aggregated_artifact'])

        for key, top_set in zip(fractions.keys(), [top_10, top_100, top_500]):
            fractions[key].append((len(top_set - prev_top[key]) / len(top_set)) * 100 if top_set else 0)
            prev_top[key] = top_set

    for key in ["Top 10", "Top 100", "Top 500"]:  
        ax.plot(years, fractions[key], line_styles[key], 
                color=category_colors[key], label=key, 
                marker='o', markersize=6, markeredgewidth=2)

    ax.set_title(f"{platform}", fontsize=18, fontweight='bold') 
    ax.grid(True)
    
    ticks = list(range(start_year, 2018, 2)) + [2018, 2019]
    ax.set_xticks(ticks) 
    ax.set_xticklabels([str(y) for y in range(start_year, 2018, 2)] + ["", "2019"]) 

for j in range(i + 1, len(axes)):
    axes[j].axis('off')

for ax in axes[-4:]:
    ax.set_xlabel("Year", fontsize=18, fontweight='bold')

axes[0].set_ylabel("Fraction of New Packages (%)", fontsize=18, fontweight='bold', labelpad=20)
axes[0].yaxis.label.set_position((-0.1, 0.05))

plt.yticks(range(0, 110, 10))

legend = fig.legend(
    ["Top 10", "Top 100", "Top 500"], 
    loc="upper center", 
    ncol=3, 
    fontsize=22, 
    frameon=True, 
    bbox_to_anchor=(0.5, 1.02)  
)

for text in legend.get_texts():
    text.set_fontweight("bold")

plt.subplots_adjust(top=0.90, bottom=0.1, left=0.05, right=0.95)  

plt.tight_layout(pad=3.0)  

plt.show()

