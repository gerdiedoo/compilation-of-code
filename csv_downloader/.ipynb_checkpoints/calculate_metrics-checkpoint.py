from cmath import sqrt
import pandas as pd 
import numpy as np 
from scipy.stats import t

def get_df(files):
    dfs = []

    for file in files:
        try:
            df = pd.read_csv(file, header=None)
            dfs.append(df)
        except FileNotFoundError:
            print(f'{file} not found...')
    
    size = len(dfs)
    steps = list(map(int, dfs[0].loc[1:, 0]))
    losses = []
    for df in dfs:
        losses.append(np.array(df.loc[1:, 2]))

    main_df = pd.DataFrame(columns=['steps'] + list(range(len(dfs))) + ['mean', 'std', 'ci_low', 'ci_high'])
    main_df.loc[:, 'steps'] = steps

    for idx, loss in enumerate(losses):
        main_df.loc[:, idx] = loss 
    temp_df = main_df[list(range(0, 9))].astype(float).to_numpy()

    means = np.mean(temp_df, axis=1)
    stds = np.std(temp_df, axis=1)

    def ci(x_bar, z, s, n, high=True):
        b = z * (s / np.sqrt(n))
        if high:
            return x_bar + b
        else:
            return x_bar - b 

    # print(means)
    # print(stds)
    ci_high = ci(means, 1.96, stds, 10)
    ci_low = ci(means, 1.96, stds, 10, high=False)

    main_df['mean'] = means 
    main_df['std'] = stds
    main_df['ci_high'] = ci_high 
    main_df['ci_low'] = ci_low
    
    return main_df

hamming_files = [f'worst-three-retrain/training_hamming_loss_{i}.csv' for i in range(10)]
macro_files = [f'worst-three-retrain/training_Macro_F1_{i}.csv' for i in range(10)]
micro_files = [f'worst-three-retrain/training_Micro_F1_{i}.csv' for i in range(10)]
training_files = [f'worst-three-retrain/training_train_loss_{i}.csv' for i in range(10)]
validation_files = [f'worst-three-retrain/training_validation_{i}.csv' for i in range(10)]

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

hamming_df.to_csv('hamming.csv')
macro_df.to_csv('macro.csv')
micro_df.to_csv('micro.csv')
train_df.to_csv('training.csv')
val_df.to_csv('validation.csv')