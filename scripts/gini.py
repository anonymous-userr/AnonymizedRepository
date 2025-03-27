#plot ginis

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('path to dataset')

data.columns = data.columns.str.strip()

platforms = data['Platform'].unique()
years = range(1995, 2021)

gini_values = {platform: [] for platform in platforms}

for year in years:
    for platform in platforms:
        value = data[(data['Platform'] == platform) & (data['Year'] == year)]['Gini Index']
        gini_values[platform].append(value.values[0] if not value.empty else None)

plt.figure(figsize=(14, 8), dpi=100)

for platform in platforms:
    plt.plot(years, gini_values[platform], marker='o', markersize=8, linewidth=2.5, label=platform)

plt.title('Gini (Packages)', fontsize=22, fontweight='bold')
plt.xlabel('Year', fontsize=18, fontweight='bold')
plt.ylabel('Gini Index', fontsize=18, fontweight='bold')
plt.xticks(range(1995, 2021, 5), fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=16, loc='upper left', frameon=True)
plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)
plt.savefig('gini_progression.png', dpi=600, bbox_inches='tight')
plt.show()

