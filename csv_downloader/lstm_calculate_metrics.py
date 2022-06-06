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
    temp_df = main_df[list(range(0, 7))].astype(float).to_numpy()

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

test_accuracy_files = [f'lstm-insertion-sort/test_accuracy_{i}.csv' for i in range(8)]
test_f1_files = [f'lstm-insertion-sort/test_F1_score_{i}.csv' for i in range(8)]
test_loss_files = [f'lstm-insertion-sort/test_loss_per_epoch_{i}.csv' for i in range(8)]
training_accuracy_files = [f'lstm-insertion-sort/training_accuracy_{i}.csv' for i in range(8)]
training_loss_files = [f'lstm-insertion-sort/training_loss_per_epoch_{i}.csv' for i in range(8)]

test_accuracy_df = get_df(test_accuracy_files)
test_f1_df = get_df(test_f1_files)
test_loss_df = get_df(test_loss_files)
training_accuracy_df = get_df(training_accuracy_files)
training_loss_df   = get_df(training_loss_files)

print('Test Accuracy')
print(test_accuracy_df)

print('\n\nTest F1')
print(test_f1_df)

print('\n\nTest Loss')
print(test_loss_df)

print('\n\nTraining Accuracy')
print(training_accuracy_df)

print('\n\nTraining Loss')
print(training_loss_df)

test_accuracy_df.to_csv('test_accuracy.csv')
test_f1_df.to_csv('test_f1.csv')
test_loss_df.to_csv('test_loss.csv')
training_accuracy_df.to_csv('training_accuracy.csv')
training_loss_df.to_csv('training_loss.csv')