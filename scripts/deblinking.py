import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from itertools import groupby
from operator import itemgetter
import sys


def plot_blinking(pupil_data, indexes,sampling_frequency, figure_name):
    sns.set_style("whitegrid")
    sns.set(style="ticks", rc={"lines.linewidth": 0.7})
    ax = plt.subplots();
    ax = sns.pointplot(x=indexes, y=pupil_data);

    ax.set_xlabel("samples",fontsize=15);
    ax.set_ylabel("pupil size",fontsize=15);
    ax.tick_params(labelsize=10);

    ax.xaxis.set_major_locator(ticker.MultipleLocator(sampling_frequency));
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter());

    ax.figure.savefig(figure_name);

def deblinking(single_data_trial, sampling_frequency, missing_data_symbol, subject, trial_index, blink_threshold, max_trial_duration, start_blink_onset, end_blink_offset, plotting):
    sd = np.nanstd(single_data_trial.PUPIL_SIZE.astype(float))
    mean = np.nanmean(single_data_trial.PUPIL_SIZE.astype(float))

    # 3 times standard deviation is computed for outliers
    sd_less = mean - 3*sd
    sd_more = mean + 3*sd

    raw_pupil_data = single_data_trial.PUPIL_SIZE.astype(float).copy()

    outliers = single_data_trial[(single_data_trial['PUPIL_SIZE'].astype(float) < sd_less) | (single_data_trial['PUPIL_SIZE'].astype(float) > sd_more) | (single_data_trial['PUPIL_SIZE'].isnull()) ].copy()


    blink_sets = []

    for k, g in groupby(enumerate(outliers.SAMPLE_INDEX), lambda ix : ix[0] - ix[1]):
        blink_sets.append(list(map(itemgetter(1), g)))

    nBlinks = len(blink_sets)

    if len(outliers) == 0:
        print("No blinks detected")

        return 0,single_data_trial

    elif (len(outliers) > blink_threshold * sampling_frequency * max_trial_duration):
        print("Exclude trial", trial_index, "too many blinks!")
        return 1,single_data_trial
    else:
        print(nBlinks,"blinks were detected")
        print("Deblinking now....")

        for blinks in blink_sets:
            start_blink = blinks[0]
            end_blink = blinks[len(blinks)-1]
            #print(start_blink)
            #print(end_blink)
            # If the blink occured within the first 50samples of the trial, then we set the start_value to the mean of the
            #values from sample 1 until the start of the blink, the same applies for taking 80 samples after blink -
            # we only take the values from the end of the blink until the end of trial even is it is less than 80.

            if start_blink < 50:
                interp_start_index = 1
            else:
                interp_start_index = start_blink - 50

            if (end_blink + 80) > len(single_data_trial):
                interp_end_index = len(single_data_trial) - 1
            else:
                interp_end_index = end_blink + 80

            interp_values = single_data_trial.PUPIL_SIZE[interp_start_index:interp_end_index]
           # print(interp_start_index,interp_end_index)

            gap = interp_end_index - interp_start_index + 1
            start_value = single_data_trial.loc[single_data_trial['SAMPLE_INDEX'] == interp_start_index, 'PUPIL_SIZE'].iloc[0]
           # print(start_value)
            end_value = single_data_trial.loc[single_data_trial['SAMPLE_INDEX'] == interp_end_index,'PUPIL_SIZE'].iloc[0]
           # print(end_value)
            step = (float(end_value) - float(start_value))/gap
           # print(step)
            interpolated_vals = []
            for m in range(1,gap):
                y = float(start_value)+m*step
                interpolated_vals.append(y)
           # print(interpolated_vals)

            start_value_index = single_data_trial.loc[single_data_trial['SAMPLE_INDEX'] == interp_start_index]
            start_n = start_value_index.index[0]
            end_value_index = single_data_trial.loc[single_data_trial['SAMPLE_INDEX'] == interp_end_index]
            end_n = end_value_index.index[0]
            indexes = []
            for i in range(start_n,end_n):
                indexes.append(i)

            #print(indexes)
            updated_values = pd.Series(interpolated_vals, name='PUPIL_SIZE', index=indexes)
            single_data_trial.update(updated_values)

        if plotting:
            print("Plotting pre and post-blink data ....")
            single_data_trial['raw_pupil_data'] = raw_pupil_data
            single_data_trial['PUPIL_SIZE'] = single_data_trial['PUPIL_SIZE'].astype('float64', copy=False)
            indexes = single_data_trial.SAMPLE_INDEX
            figure_name = (plots_filepath+"/"+subject+"_trial_"+str(trial_index)+".pdf")
            single_data_trial.plot(x="SAMPLE_INDEX", y=["raw_pupil_data","PUPIL_SIZE"])
            plt.savefig(figure_name)
            plt.cla()
            print("Plot saved in", figure_name)

        return 0,single_data_trial



if __name__ == '__main__':

    print(sys.argv)
    #Some global variables to be extracted from the cofig filepath
    sampling_frequency = int(sys.argv[1])
    missing_data_symbol = sys.argv[2]
    file_pattern = sys.argv[3]
    blink_threshold = float(sys.argv[4])
    max_trial_duration = int(sys.argv[5])
    start_blink_onset = int(sys.argv[6])
    end_blink_offset = int(sys.argv[7])
    plotting = sys.argv[8]
    nsubjects = int(sys.argv[9])
    dataDir=sys.argv[10]
    plots_filepath=sys.argv[11]
    downsampling=sys.argv[12]
    downsampleFreq=sys.argv[13]
    exclusion_list=sys.argv[14]
    experimentDir=sys.argv[15]


    with open(exclusion_list) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    nsubjects = int(nsubjects) + 1
    file_indexes = []
    for n in range(1,nsubjects):
        index=file_pattern+str(n)
        file_indexes.append(index)

    for n in file_indexes:
        print("Deblinking pupil data for:",n)

        filename=dataDir+'/'+str(n)+'.csv'


        # Read single participants data at a time

        print("Loading data for ....",n)
        df1 = pd.DataFrame( columns=['TRIAL_INDEX'], dtype=int)
        df2 = pd.DataFrame( columns=['PUPIL_SIZE'], dtype=float)
        df3 = pd.DataFrame( columns=['STIMULI','SYSTEMS'], dtype=str)
        df4 = pd.DataFrame(columns=['BLOCKS'], dtype=int)
        df5 = pd.DataFrame(columns=['SUBJECT'], dtype=str)
        df6 = pd.DataFrame( columns=['SAMPLE_INDEX'], dtype=int)
        df7 = pd.DataFrame( columns=['raw_pupil_data'], dtype=float)

        all_trials_df = pd.concat([df1, df2, df3,df4,df5,df6,df7], axis=1)

        all_pupil_data = pd.read_csv(filename, usecols=['TRIAL_INDEX','PUPIL_SIZE','STIMULI','SYSTEMS','BLOCKS','SUBJECT'])

        trials = all_pupil_data.TRIAL_INDEX.unique()
        numTrial=len(trials)
        exclude_trials = ''
        for idx,lists in enumerate(content):
            if n in lists:
                exclude = content[idx]
                exclude_trials = exclude.split("#")
                exclude_trials = exclude_trials[1]

        print(exclude_trials)
        for trial_index in trials:

            if str(trial_index) not in exclude_trials:

                single_data_trial = all_pupil_data[all_pupil_data['TRIAL_INDEX'] == trial_index].copy()
                single_data_trial['PUPIL_SIZE'].replace(missing_data_symbol, np.nan, inplace=True)
                single_data_trial['SAMPLE_INDEX'] = list(range(1,len(single_data_trial)+1))
                print("Deblinking Trial:",trial_index,"out of",numTrial, "for",n)
                exclude,single_data_trial = deblinking(single_data_trial, sampling_frequency, missing_data_symbol, n, trial_index, blink_threshold, max_trial_duration, start_blink_onset, end_blink_offset, plotting)

                if exclude == 0:
                    if downsampling:
                        print("Downsampling data from",sampling_frequency,"Hz to",downsampleFreq)
                        downsampled_trial = single_data_trial.iloc[0::10, :].copy()
                        all_trials_df = all_trials_df.append(downsampled_trial, ignore_index=True)
                else:
                    print("Excluded trial",trial_index," for ",n)

        print("Deblinking and exclusion completed for", n)
        print("Saving CSV file for",n)
        csv_filename=experimentDir+"/deblinking/"+str(n)+".csv"
        all_trials_df.to_csv(csv_filename, encoding='utf-8', index=False)
