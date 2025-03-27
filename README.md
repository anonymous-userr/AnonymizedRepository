## Reproducing Results



### Prerequisites

1. Install neo4j (version 4.x)
2. Use Python version 3.*, tested with 3.12.2
3. Install the dependencies contained in [requirements.text](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/requirements.txt)

*Note: To install dependencies on MacOS, you may want to use `brew`*


### Steps

#### Step 1: Acquire dataset from [Libraries.IO](https://doi.org/10.5281/zenodo.3626071) and convert tar file

| Script | Input | Output |
| --- | --- | --- |
|[load_zip_file](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/load_zip_file.py) |[Libraries.IO dataset](https://doi.org/10.5281/zenodo.3626071)  |[Extracted files](https://doi.org/10.5281/zenodo.15093005)





#### Step 2: Extract releases and dependencies data 

| Script | Input | Output |
| --- | --- | --- |
|[release_all](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/release_all.py) , [links_all](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/links_all.py)|[Extracted files](https://doi.org/10.5281/zenodo.15093005)  |[release_all_Libs,links_all_Libs](https://doi.org/10.5281/zenodo.15093005)



Note: Ensure the converted CSV files `links_all.csv` and `release_all.csv` are saved in your current directory.

#### Step 3: Merge and clean datasets 

| Script | Input | Output |
| --- | --- | --- |
|[merge.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/merge.py)|[links_all.csv, release_all.csv](https://doi.org/10.5281/zenodo.15093005) |[merged_final_output.csv](https://doi.org/10.5281/zenodo.15093005)


#### Step 4: Compute release, package and dependency counts
| Script | Input | Output |
| --- | --- | --- |
|[release_package_count.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/release_package_counts.py)|  [merged_final_output.csv](https://doi.org/10.5281/zenodo.15093005)| [(vertex_GAV,vertex_GA,Edges_GAV,Edges_GA).csv](https://doi.org/10.5281/zenodo.15093005)|



#### Step 5: Plot release, package and dependency growth
| Script | Input | Output |
| --- | --- | --- |
|[plot_growth.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/plot_growth.py)|[(vertex_GAV,vertex_GA,Edges_GAV,Edges_GA).csv](https://doi.org/10.5281/zenodo.15093005)|[plots](https://github.com/anonymous-userr/AnonymizedRepo/tree/main/plots)|


#### Step 6: Compute average releases
| Script | Input | Output |
| --- | --- | --- |
|[average_release.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/average_release.py)| [release_all_Libs.csv](https://doi.org/10.5281/zenodo.15093005) |[average_main](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/plots/average_main.png) |


#### Step 7: Compute noise ratio
| Script | Input | Output |
| ---| --- | --- |
|[noise_ratio.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/noise_ratio.py)| [(release_all_Libs, links_all_Libs).csv](https://doi.org/10.5281/zenodo.15093005)  |[noise by year main](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/plots/noise%20by%20year%20main.png)|

#### Step 8: Compute Gini
| Script | Input | Output |
| ---| --- | --- |
|[gini.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/gini.py)| [(release_all_Libs, links_all_Libs).csv](https://doi.org/10.5281/zenodo.15093005) |[giniGA](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/plots/gini_GA(-2020).png)|



#### Step 9: Compute innovation rate
| Script | Input | Output |
| ---| --- | --- |
|[innovation_rate.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/innovation_rate.py)| [release_all_Libs](https://doi.org/10.5281/zenodo.15093005) |[innovation1_chart,innovation2_chart](https://github.com/anonymous-userr/AnonymizedRepo/tree/main/plots)|


#### Step 10: Compute top 500
| Script | Input | Output |
| ---| --- | --- |
|[compute_top_500.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/compute_top_500.py)| [merged_final_output.csv](https://doi.org/10.5281/zenodo.15093005) |[top_500](https://doi.org/10.5281/zenodo.15093005)|


#### Step 11: Relative change in elites
| Script | Input | Output |
| ---| --- | --- |
|[relative_change_in_elites.py](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/scripts/relative_change_in_elites.py)| [top_500](https://doi.org/10.5281/zenodo.15093005) |[FractionOfReplacement_main](https://github.com/anonymous-userr/AnonymizedRepo/blob/main/plots/FractionOfReplacement_main.png)|




