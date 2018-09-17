# This script pre-processes the raw data into a standard format for analysis
# It takes in an xlsx format file as input (which is typically the output of the SR eyelink)

import numpy as np
import pandas as pd
import sys
import ast


# This must be grabbed from the config file
x = sys.argv[1]
discardTrials = ast.literal_eval(x)
practiceTrials = sys.argv[2]
nsubjects = sys.argv[3]
file_pattern=sys.argv[4]
file_extension=sys.argv[5]
dataDir=sys.argv[6]
experiment_name=sys.argv[7]

##########################################################################

nsubjects = int(nsubjects) + 1
file_indexes = []
for n in range(1,nsubjects):
    index=file_pattern+str(n)
    file_indexes.append(index)

for n in file_indexes:
    print("Preprocessing file for:",n)

    filename=dataDir+'/'+str(n)+'.'+file_extension
    single_participants_data = pd.read_excel(filename)

    eye_tracked = single_participants_data.EYE_TRACKED[0]
    print(eye_tracked+'eye was tracked...')

    if eye_tracked == 'Right':
        pupil_size = single_participants_data.RIGHT_PUPIL_SIZE
    else:
        pupil_size = single_participants_data.LEFT_PUPIL_SIZE

    stimuli = single_participants_data.sound

    trial_index = single_participants_data.TRIAL_INDEX

    system = single_participants_data.system

    df = pd.DataFrame(data=trial_index)
    df['PUPIL_SIZE'] = pupil_size
    df['STIMULI']=stimuli
    df['SYSTEMS']=system

    df['BLOCKS'] = pd.factorize(df['SYSTEMS'])[0] + 1

    remove_practice = df[(df['BLOCKS'] > 1)].copy()

    updated_indexes = remove_practice['TRIAL_INDEX'] - int(practiceTrials)
    remove_practice['TRIAL_INDEX'] = updated_indexes

    updated_block_indexes = remove_practice['BLOCKS'] - 1
    remove_practice['BLOCKS'] = updated_block_indexes

    remove_practice = remove_practice[remove_practice['TRIAL_INDEX'].isin(discardTrials) == False]

    remove_practice['SUBJECT'] = n

    final_subject_data = remove_practice.copy()

    print('Saving %s data as csv file' %n)
    final_subject_data.to_csv('experiments/%s/preprocessing/%s.csv'%(experiment_name,n), sep=',')
