import pandas as pd 
import numpy as np 
from scipy.stats import tstd

def get_df(files):
    dfs = []

    for file in files:
        try:
            df = pd.read_csv(file, header=None)
            dfs.append(df)
        except FileNotFoundError:
            print(f'{file} not found...')
    
    size = len(dfs)
    steps = list(map(int, dfs[0].loc[:, 0]))
    losses = []
    for df in dfs:
        losses.append(np.array(df.loc[:, 2]))

    main_df = pd.DataFrame(columns=['steps'] + list(range(len(dfs))) + ['average', 'std'])
    main_df.loc[:, 'steps'] = steps

    for idx, loss in enumerate(losses):
        main_df.loc[:, idx] = loss 

    # Get standard deviation for each row.
    for j in range(len(main_df)):
        print(j)
        row = np.array([main_df.loc[j, i] for i in range(len(dfs))])
        main_df.loc[j, 'std'] = tstd(row)
        main_df.loc[j, 'average'] = np.average(row)

    return main_df

hamming_files = [f'focal loss/training_hamming_loss_{i}.csv' for i in range(8)]
macro_files = [f'focal loss/training_Macro_F1_{i}.csv' for i in range(8)]
micro_files = [f'focal loss/training_Micro_F1_{i}.csv' for i in range(8)]
training_files = [f'focal loss/training_train_loss_{i}.csv' for i in range(8)]
validation_files = [f'focal loss/training_validation_{i}.csv' for i in range(8)]

hamming_df = get_df(hamming_files)
macro_df = get_df(macro_files)
micro_df = get_df(micro_files)
train_df = get_df(training_files)
val_df   = get_df(validation_files)

print('Hamming')
print(hamming_df)

print('\n\nMacro F1')
print(macro_df)

print('\n\nMicro F1')
print(micro_df)

print('\n\nTraining')
print(train_df)

print('\n\nValidation')
print(val_df)

hamming_df.to_csv('hamming_focal_loss.csv')
macro_df.to_csv('macro_focal_loss.csv')
micro_df.to_csv('micro_focal_loss.csv')
train_df.to_csv('training_focal_loss.csv')
val_df.to_csv('validation_focal_loss.csv')