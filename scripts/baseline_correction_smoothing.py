import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def correction_and_smoothing(single_data_trial, actual_baseline, true_baseline, n, trial_index, plots_filepath, sampling_freq):
    if actual_baseline != true_baseline:
        remove_samples = int(sampling_freq*(actual_baseline-true_baseline))
        single_data_trial.drop(single_data_trial.index[:remove_samples], inplace=True)

    baseline_samples_n = sampling_freq*true_baseline + 1
    baseline = single_data_trial.PUPIL_SIZE[:baseline_samples_n]
    mean_baseline = np.mean(baseline)
    corrected_pupil_size = ((single_data_trial.PUPIL_SIZE - mean_baseline)/mean_baseline)*100
    smoothing = corrected_pupil_size.rolling(window=moving_average_window).mean()
    values = [i for i in range(sampling_freq,len(corrected_pupil_size)+sampling_freq) if i % sampling_freq == 0]
    corrected_pupil_size.plot(color='C0', xticks=values, use_index=False)
    smoothing.plot(color='C2', xticks=values, use_index=False)
    figure_name = plots_filepath+"/"+str(n)+"_trial_"+str(trial_index)+".pdf"
    print(figure_name)
    plt.savefig(figure_name)
    plt.cla()

    single_data_trial['CORRECTED'] = corrected_pupil_size
    single_data_trial['SMOOTHED'] = smoothing

    return single_data_trial



if __name__ == '__main__':

    print(sys.argv)

    #Some global variables to be extracted from the cofig filepath

    sampling_frequency = int(sys.argv[1])
    actual_baseline = int(sys.argv[2])
    true_baseline = int(sys.argv[3])
    moving_average_window = int(sys.argv[4])
    nsubjects = int(sys.argv[5])
    file_pattern = sys.argv[6]
    dataDir=sys.argv[7]
    experimentDir=sys.argv[8]
    plots_filepath=sys.argv[9]


    nsubjects = int(nsubjects) + 1
    file_indexes = []
    for n in range(1,nsubjects):
        index=file_pattern+str(n)
        file_indexes.append(index)

    for n in file_indexes:
        print("Loading pupil data:",n)

        df1 = pd.DataFrame( columns=['TRIAL_INDEX'], dtype=int)
        df2 = pd.DataFrame( columns=['PUPIL_SIZE'], dtype=float)
        df3 = pd.DataFrame( columns=['STIMULI','SYSTEMS'], dtype=str)
        df4 = pd.DataFrame(columns=['BLOCKS'], dtype=int)
        df5 = pd.DataFrame(columns=['SUBJECT'], dtype=str)
        df6 = pd.DataFrame( columns=['SAMPLE_INDEX'], dtype=int)
        df7 = pd.DataFrame( columns=['raw_pupil_data'], dtype=float)

        all_trials_df = pd.concat([df1, df2, df3,df4,df5,df6,df7], axis=1)

        filename=dataDir+'/'+str(n)+'.csv'
        pupil_data = pd.read_csv(filename, usecols=['TRIAL_INDEX','PUPIL_SIZE','STIMULI','SYSTEMS','BLOCKS','SUBJECT'])
        trials = pupil_data.TRIAL_INDEX.unique()
        numTrial=len(trials)

        for idx,trial_index in enumerate(trials):
            single_data_trial = pupil_data[pupil_data['TRIAL_INDEX'] == trial_index].copy()
            single_data_trial['SAMPLE_INDEX'] = list(range(1,len(single_data_trial)+1))
            print("Correcting Trial:",(idx+1),"out of",numTrial, "for",n)

            smoothed_trial = correction_and_smoothing(single_data_trial, actual_baseline, true_baseline, n, trial_index, plots_filepath,sampling_frequency )
            all_trials_df = all_trials_df.append(smoothed_trial, ignore_index=True)

        print("Correction and smoothing completed for", n)
        print("Saving CSV file for",n)
        csv_filename=experimentDir+"/smoothed/"+str(n)+".csv"
        all_trials_df.to_csv(csv_filename, encoding='utf-8', index=False)
