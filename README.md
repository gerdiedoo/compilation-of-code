# Multiclass Classification Transformer

### Folders

1. `training_notebooks` contains the training notebooks that were used in this study.
2. `website` contains the same website deployed in [Pancit Canton](https://pancitcanton.azurewebsites.net).
3. `metrics` contains the [Julia](https://julialang.org/) scripts that were used for evaluating model performance. This folder also contain some sample `pickle` files. Unfortunately, these pickle files were lost.
4. `clone_repositories` contains the script to download a list of repositories in a text, and a script to delete multiple copies of a file. Also contains the textfile of all repositories that was used
5. `LSTM` contains the LSTM training notebooks.
6. `data_augmentation` contains scripts that can concatenate files and change identifiers. Also contains the preliminary dataset of the study.
7. `calculate_metrics` - contains a script that calculates the multilabel metrics and a separate script that calculates subset accuracy from pkl files.
8. `csv-downloader` contains scripts that are essential in downloading and calculating metrics from csvs from neptune.ai
9. `data-labeling` contains a script that computes for the interrater reliability and another script that generates crosswalk worksheets.
10. `final-augmented-dataset` contains a script that calculates the datapoints with n labels.
11. `initial-training` contains the model that uses unweighted binary crossentropy loss that the researchers have used in the initial training.
12. `minor_script` contains a script that translates csv file to latex table.
