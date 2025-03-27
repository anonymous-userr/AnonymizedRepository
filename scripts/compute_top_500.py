#compute top 500
import pandas as pd
import numpy as np

def calculate_top_500_for_platform(file_path, platform_name):
    def gini_coefficient(x):
        """Compute Gini coefficient for an array x and return Lorenz curve."""
        x = np.array(x, dtype=float)
        x.sort()
        cumulative_sum = np.cumsum(x)
        n = len(x)
        total_sum = cumulative_sum[-1]
        if total_sum == 0:
            return 0.0, None
        lorenz_curve = np.concatenate(([0], cumulative_sum / total_sum))
        gini = 1 - (2 / n) * np.sum(lorenz_curve[1:]) + (1 / n)
        return gini, lorenz_curve

    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    df = df.rename(columns={'source': 'Dependencies', 'target': 'Artifact', 'source_release': 'dependency_release_date', 'target_release': 'artifact_release_date'})

    df['dependency_release_date'] = df['dependency_release_date'].astype(str)
    df['artifact_release_date'] = df['artifact_release_date'].astype(str)

    df['dependency_release_year'] = df['dependency_release_date'].str[:4]
    df['artifact_release_year'] = df['artifact_release_date'].str[:4]

    df['dependency_release_year'] = pd.to_numeric(df['dependency_release_year'], errors='coerce')

    df['aggregated_artifact'] = df['Artifact'].apply(lambda x: ':'.join(x.split(':')[:2]) if isinstance(x, str) and len(x.split(':')) > 2 else (x.split(':')[0] if isinstance(x, str) else ''))

    artifact_dependency_counts = df.groupby(['aggregated_artifact', 'dependency_release_year'])['Dependencies'].count().reset_index()
    artifact_dependency_counts.rename(columns={'Dependencies': 'dependency_count'}, inplace=True)

    top_artifacts_per_year = artifact_dependency_counts.groupby('dependency_release_year').apply(lambda x: x.nlargest(500, 'dependency_count')).reset_index(drop=True)

    output_file = f"top_500_aggregated_artifacts_per_year_{platform_name}.csv"
    top_artifacts_per_year.to_csv(output_file, index=False)

    return top_artifacts_per_year



platforms_start_year = {
    "Maven": 2002, "NPM": 2010, "Pypi": 2005, "CPAN": 2002,
    "Cargo": 2014, "CRAN": 1999, "Packagist": 2011, "NuGet": 2011
}

for platform, start_year in platforms_start_year.items():
    file_path = f"/path to dataset/merged_final_output.csv"  
    calculate_top_500_for_platform(file_path, platform)



