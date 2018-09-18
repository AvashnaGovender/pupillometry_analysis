import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def average(aggregated_df, figure_name):

    system_names = aggregated_df.SYSTEMS.unique()

    for system in system_names:
        systems_data = aggregated_df[aggregated_df['SYSTEMS'] == system].copy()
        ax = systems_data['SMOOTHED'].plot(use_index=False, label=system, legend=True)
    plt.savefig(figure_name)
    plt.cla()

    aggregated_df['SUBJECT'] = n

    return aggregated_df


if __name__ == '__main__':

    #print(sys.argv)
    nsubjects = int(sys.argv[1])
    file_pattern = sys.argv[2]
    dataDir=sys.argv[3]
    sampling_freq = sys.argv[4]
    plots_filepath = sys.argv[5]
    experimentDir = sys.argv[6]
    # Averaging for each participant individually

    nsubjects = int(nsubjects) + 1
    file_indexes = []
    for n in range(1,nsubjects):
        index=file_pattern+str(n)
        file_indexes.append(index)

    df1 = pd.DataFrame( columns=['SAMPLE_INDEX'], dtype=int)
    df2 = pd.DataFrame( columns=['SMOOTHED'], dtype=float)
    df3 = pd.DataFrame( columns=['SYSTEMS'], dtype=str)
    df4 = pd.DataFrame(columns=['SUBJECT'], dtype=str)

    all_data_df = pd.concat([df1, df2, df3,df4], axis=1)

    for n in file_indexes:
        print("Loading pupil data:",n)

        filename=dataDir+'/'+str(n)+'.csv'
        pupil_data = pd.read_csv(filename, usecols=['SAMPLE_INDEX','SMOOTHED','SYSTEMS','SUBJECT'])

        aggregate = pupil_data.groupby(['SYSTEMS','SAMPLE_INDEX'])['SMOOTHED'].mean().reset_index()
        figure_name = plots_filepath+"/"+str(n)+"_average.pdf"

        averaged_df = average(aggregate, figure_name).copy()

        print("Saving CSV file participant:",n)
        csv_filename=experimentDir+"/averaging/"+str(n)+".csv"
        averaged_df.to_csv(csv_filename, encoding='utf-8', index=False)

        all_data_df = all_data_df.append(averaged_df, ignore_index=True)

    print("Saving CSV file for all participants ...")
    csv_filename=experimentDir+"/averaging/all_data.csv"
    all_data_df.to_csv(csv_filename, encoding='utf-8', index=False)


    # Averaging across all participants

    pupil_data_all = pd.read_csv(csv_filename, usecols=['SAMPLE_INDEX','SMOOTHED','SYSTEMS','SUBJECT'])

    aggregate_all = pupil_data_all.groupby(['SYSTEMS','SAMPLE_INDEX'])['SMOOTHED'].mean().reset_index()
    figure_name_all = plots_filepath+"/all_participants_average.pdf"
    all_averaged_df = average(aggregate_all, figure_name_all).copy()
