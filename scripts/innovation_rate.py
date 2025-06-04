#plot innovation rate

import pandas as pd
import matplotlib.pyplot as plt

file_path = "/path to dataset/release_all_Libs.csv"
df = pd.read_csv(file_path)

df['ga'] = df['artifact'].apply(lambda x: ':'.join(x.split(':')[:2]) if isinstance(x, str) and len(x.split(':')) > 2 else x.split(':')[0] if isinstance(x, str) else '')

df['year'] = df['release'].str[:4].astype(int)

platforms_of_interest = ['Maven', 'NPM', 'Pypi', 'CPAN', 'Cargo', 'CRAN', 'Packagist', 'NuGet']
df_filtered = df[df['Platform'].isin(platforms_of_interest)]

def extract_major_version(artifact):
    if not isinstance(artifact, str):
        return None
    try:
        return int(artifact.split(':')[-1].split('.')[0])  
    except (IndexError, ValueError):
        return None

df_filtered['major_version'] = df_filtered['artifact'].apply(extract_major_version)
df_filtered = df_filtered[df_filtered['major_version'].notna()]

df_sorted = df_filtered.sort_values(['Platform', 'ga', 'year'])
df_sorted['major_change'] = df_sorted.groupby(['Platform', 'ga'])['major_version'].diff().fillna(0) > 0

df_innovations = df_sorted[df_sorted['major_change']]
innovation_counts = df_innovations.groupby(['Platform', 'year'])['ga'].nunique().reset_index(name='Innovation Count')

least_year_ga = df_filtered.groupby(['Platform', 'ga'])['year'].min().reset_index()
least_year_counts = least_year_ga.groupby(['Platform', 'year'])['ga'].nunique().reset_index(name='First GA Count')

oldest_year_ga = df_filtered.groupby(['Platform', 'ga'])['year'].max().reset_index()
oldest_year_counts = oldest_year_ga.groupby(['Platform', 'year'])['ga'].nunique().reset_index(name='Last GA Count')

ga_counts = pd.merge(least_year_counts, oldest_year_counts, on=['Platform', 'year'], how='inner')
ga_counts = pd.merge(ga_counts, innovation_counts, on=['Platform', 'year'], how='left')
ga_counts['Innovation Count'] = ga_counts['Innovation Count'].fillna(0)

ga_counts['Innovation1'] = ga_counts['First GA Count'] / ga_counts['Last GA Count'].replace(0, float('nan'))
ga_counts['Innovation2'] = ga_counts['Innovation Count'] / ga_counts['Last GA Count'].replace(0, float('nan'))

start_year = 1995
end_year = 2018
ga_counts_filtered = ga_counts[(ga_counts['year'] >= start_year) & (ga_counts['year'] <= end_year)]

platform_colors = {
    'Maven': 'b', 'NPM': 'g', 'Pypi': 'r', 'CPAN': 'c',
    'Cargo': 'm', 'CRAN': 'y', 'Packagist': 'k', 'NuGet': '#ff6600'
}

fig1, ax1 = plt.subplots(figsize=(12, 7))

for platform in platforms_of_interest:
    platform_data = ga_counts_filtered[ga_counts_filtered['Platform'] == platform]
    if not platform_data.empty:
        ax1.plot(platform_data['year'], platform_data['Innovation1'], marker='o', linestyle='-',
                 color=platform_colors.get(platform, 'black'), label=f"{platform}")

ax1.axhline(y=1, color='red', linestyle='--', linewidth=2, label="Ratio = 1")

ax1.set_title('Innovation1 (FirstPackage / LastPackage)', fontsize=22, fontweight='bold')
ax1.set_xlabel('Year', fontsize=18, fontweight='bold')
ax1.set_ylabel('Ratio', fontsize=18, fontweight='bold')
ax1.set_xticks(list(range(1995, 2019, 2)) + [2018])
ax1.set_xlim(1995, 2018.5)
ax1.set_ylim(0, 6) 
ax1.grid(True, linestyle='--', linewidth=0.5)
ax1.legend(title="Platforms")

fig1.savefig("innovation1_chart.png")


fig2, ax2 = plt.subplots(figsize=(12, 7))

for platform in platforms_of_interest:
    platform_data = ga_counts_filtered[ga_counts_filtered['Platform'] == platform]
    if not platform_data.empty:
        ax2.plot(platform_data['year'], platform_data['Innovation2'], marker='o', linestyle='-',
                 color=platform_colors.get(platform, 'black'), label=f"{platform}")

ax2.set_title('Innovation2 (MajorReleasePackage / LastPackage)', fontsize=22, fontweight='bold')
ax2.set_xlabel('Year', fontsize=18, fontweight='bold')
ax2.set_ylabel('Ratio', fontsize=18, fontweight='bold')
ax2.set_xticks(list(range(1995, 2019, 2)) + [2018])
ax2.set_xlim(1995, 2018.5)
ax2.set_ylim(0, 1)  
ax2.grid(True, linestyle='--', linewidth=0.5)
ax2.legend(title="Platforms")

fig2.savefig("innovation2_chart.png")

plt.show()
