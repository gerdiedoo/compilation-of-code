import pandas as pd

def get_df(file):
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print(f'{file} not found...')
    
    size = len(df)
    data_map = df[["quicksort", "mergesort", "selectionsort", "insertionsort", "bubblesort", "linearsearch", "binarysearch", "linkedlist", "hashmap"]]
    label_count = data_map.sum()
    datapoints_with_n_labels = list(data_map.sum(axis=1))

    print("Number of files per label")
    print(label_count)
    
    print("\n\nDatapoints with n labels")
    for i in range(10):
        print(f"{i}: {datapoints_with_n_labels.count(i)}")

get_file = 'prototype/prototype.csv'
file_df = get_df(get_file)