import neptune.new as neptune
import pandas as pd
import os

project = input('Project Name: ')
run_id = input('Run ID prefix: ') # Before the '-'
start = int(input('Run ID starts at: '))
end = int(input('Ends at: '))

split = 0 # for ordered runs

for i in range(start, (end + 1)):
    try:
        print('Connecting to RUN #', i)
        run = neptune.init(
            project=f'pancit-canton/{project}',
            api_token='', # change this with your own API token
            run= f'{run_id}-{i}' # run id format
        )

        # query
        print('Querying metrics.')
        hamming = run['training/hamming loss'].fetch_values()
        micro = run['training/Micro F1'].fetch_values()
        macro = run['training/Macro F1'].fetch_values()
        train_loss = run['training/train loss'].fetch_values()
        validation_loss = run['training/validation loss'].fetch_values()

        #which_split
        tags = list(run['sys/tags'].fetch())
        print('Fetching splits.')
        for idx in range(len(tags)):
            if 'split' in tags[idx]:
                split = int(tags[idx][-1])

        if not os.path.exists(f'{project}'):
            print('Creating local project directory.')
            os.mkdir(f'{project}')

        print('Saving to csv file.')
        hamming.to_csv(f'{project}/training_hamming_loss_{split}.csv')
        micro.to_csv(f'{project}/training_Micro_F1_{split}.csv')
        macro.to_csv(f'{project}/training_Macro_F1_{split}.csv')
        train_loss.to_csv(f'{project}/training_train_loss_{split}.csv')
        validation_loss.to_csv(f'{project}/training_validation_{split}.csv')

        split = split + 1 # for ordered runs
    
    except:
        print(f'{i} is missing')