import neptune.new as neptune
import pandas as pd
import os

project = input('Project Name: ')
run_id = input('Run ID prefix: ') # Before the '-'
start = int(input('Run ID starts at: '))
end = int(input('Ends at: '))

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
        test_accuracy = run['test/accuracy'].fetch_values()
        f1_score = run['test/f1_score'].fetch_values()
        test_loss_per_epoch = run['test/loss_per_epoch'].fetch_values()
        train_accuracy = run['training/accuracy'].fetch_values()
        train_loss_per_epoch = run['training/loss_per_epoch'].fetch_values()

        #which_split
        tags = list(run['sys/tags'].fetch())
        print('Fetching splits.')
        for idx in range(len(tags)):
            if 'fold' in tags[idx]:
                split = tags[idx][-1]

        if not os.path.exists(f'{project}'):
            print('Creating local project directory.')
            os.mkdir(f'{project}')

        print('Saving to csv file.')
        test_accuracy.to_csv(f'{project}/test_accuracy_{split}.csv')
        f1_score.to_csv(f'{project}/test_F1_score_{split}.csv')
        test_loss_per_epoch.to_csv(f'{project}/test_loss_per_epoch_{split}.csv')
        train_accuracy.to_csv(f'{project}/training_accuracy_{split}.csv')
        train_loss_per_epoch.to_csv(f'{project}/training_loss_per_epoch_{split}.csv')
    except:
        print(f'{i} is missing')