#This script calculates the intelligibility scores for each participants:
#Input is the transcripts of each participant, the correct transcripts,
#mapping of participant (for multiple permutations)

import sys
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

def convert_to_csv(input_filepath):

    basename = input_filepath.split('.')[0]
    line1 = "email|type|group|completed|"
    line2 = "test@ed.ac.uk|A|A01|11 11 100|"

    count = 0
    with open(input_filepath, 'r') as results:
        line1 = ""
        line2 = ""
        for sent in results:
            count = count + 1
            elements = sent.split(" ", 1)
            audio = elements[0]
            transcription = elements[1].strip()


            line1 = line1 + "result_%s|" %audio
            line2 = line2 + "%s|" %transcription

    with open('%s.csv'%basename, 'w') as csvfile:
        csvfile.write(line1)
        csvfile.write("\n")
        csvfile.write(line2)

    return

def calc_WER(correct_path, transcript, output_path):

        call = "./HResults.pl %s %s %s dictionary " %(correct_path, transcript, output_path)
        #print(call)
        os.system(call)

        return 0

def save_WER(scores, n, systems, wer_output_dir, threshold, exclude_path, exclude_flag ):
    scores_final = pd.melt(scores)
    scores_final = scores_final[:-1]

    scores_final['WER_Percent'] = scores_final['value'] * 100
    scores_final['Subject'] = n

    nTrials = len(scores_final)/len(systems)
    system_trials = []
    for system in systems:
        for i in range(0,int(nTrials)):
            system_trials.append(system.strip())

    scores_final['System'] = system_trials
    scores_final.rename(columns={'variable': 'Stimuli', 'value': 'WER'}, inplace=True)
    csv_filename = wer_output_dir+"/"+n+"_wer.csv"
    scores_final.to_csv(csv_filename, encoding='utf-8', index=True)

    print("WER scores saved in: ",csv_filename)

    if exclude_flag:
        print("Generating exclude list for a threshold of:",threshold,"% (to exlude from further analysis)")

        exclusions = scores_final[scores_final['WER_Percent'] > int(threshold)]
        exclusion_list = exclusions.index.tolist()
        excluded_trials = n + "#"
        for trial in exclusion_list:
            trial_index = trial + 1
            excluded_trials = excluded_trials + str(trial_index) + " "

        with open(exclude_path, 'a') as exclusions:
            exclusions.write(excluded_trials)
            exclusions.write("\n")

    return scores_final


def generate_exclusions_file(scores, n, systems,wer_output_dir, wer_trial_exclusion_threshold, wer_trial_exclusion_file):

    print("Generating exclude list for WER calculation ...")
    print("Threshold to exlude is:",wer_trial_exclusion_threshold )

    exclusions = scores[scores['WER_Percent'] == int(wer_trial_exclusion_threshold)]
    exclusion_list = exclusions.index.tolist()
    excluded_trials = n + "#"
    for trial in exclusion_list:
        trial_index = trial + 1
        excluded_trials = excluded_trials + str(trial_index) + " "

    with open(wer_trial_exclusion_file, 'a') as exclusions:
        exclusions.write(excluded_trials)
        exclusions.write("\n")

    return exclusion_list

def calc_average_WER(all_wer, output_dir):

    aggregate_all = all_wer.groupby(['System'])['WER_Percent'].mean().reset_index()

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)

    ax = aggregate_all.plot(x = 'System', y ='WER_Percent' , kind = 'bar' )


    figure_name = output_dir+"/systems_wer.pdf"
    ax.figure.savefig(figure_name, bbox_inches="tight")

    plt.cla()

    print("Plot saved in", figure_name)

    csv_filename = output_dir+"/"+"systems_average_wer.csv"
    aggregate_all.to_csv(csv_filename, encoding='utf-8', index=True)
    return 0


if __name__ == '__main__':

    print(sys.argv)
    dataDir = sys.argv[1]
    nsubjects = sys.argv[2]
    exclude_path = sys.argv[3]
    file_pattern = sys.argv[4]
    group_mapppings = sys.argv[5]
    wer_output_dir = sys.argv[6]
    wer_threshold = sys.argv[7]
    exclude_flag = sys.argv[8]
    average_WER = sys.argv[9]
    generate_exclusions = sys.argv[10]
    wer_trial_exclusion_threshold = sys.argv[11]
    wer_trial_exclusion_file = sys.argv[12]
    systems_map_file = sys.argv[13]

    if not generate_exclusions:
        with open(wer_trial_exclusion_file) as f:
            exclude_content = f.readlines()
            exclude_content = [x.strip() for x in exclude_content]

    with open(group_mapppings) as map:
        mappings = map.readlines()
        mappings = [y.strip() for y in mappings]

    delete_call = "rm -rf %s/*.csv"%dataDir
    os.system(delete_call)

    nsubjects = int(nsubjects) + 1
    file_indexes = []
    for n in range(1,nsubjects):
        index=file_pattern+str(n)
        file_indexes.append(index)

    df1 = pd.DataFrame( columns=['Stimuli'], dtype=str)
    df2 = pd.DataFrame( columns=['WER'], dtype=float)
    df3 = pd.DataFrame( columns=['WER_Percent'], dtype=float)
    df4 = pd.DataFrame(columns=['SUBJECT'], dtype=str)
    df5 = pd.DataFrame( columns=['System'], dtype=str)

    all_data_df = pd.concat([df1, df2, df3,df4, df5], axis=1)

    for n in file_indexes:
        print("Converting to csv format:",n)
        filepath=dataDir+'/'+str(n)+'.txt'

        for idx,perm in enumerate(mappings):
            if n in perm:
                permutation = mappings[idx]
                perm = permutation.split(" ")
                perm_num = int(perm[1])
                correct_file = perm[2]
                systems = perm[3]
                systems = eval(systems)

        correct_path = dataDir+"/"+correct_file
        print(correct_path)

        transcript = dataDir+"/"+n+".csv"
        print(transcript)

        output_path = dataDir+"/"+n+"_output.csv"
        print(output_path)

        convert_to_csv(filepath)

        print("Calculating WER for: ",n)
        calc_WER(correct_path,transcript,output_path)

        print("Saving results to CSV")
        scores = pd.read_csv(output_path, sep = "|")
        wer_scores = save_WER(scores, n, systems, wer_output_dir, wer_threshold, exclude_path, exclude_flag )

        if generate_exclusions:
            excluded_trials = generate_exclusions_file(wer_scores, n, systems,wer_output_dir, wer_trial_exclusion_threshold, wer_trial_exclusion_file )
        else:
            for idx,lists in enumerate(exclude_content):
                if n in lists:
                    exclude = exclude_content[idx]
                    exclude_trials = exclude.split("#")
                    excluded_trials = exclude_trials[1]
                    excluded_trials = excluded_trials.split(" ")
                    excluded_trials = [int(i) for i in excluded_trials]

        final_scores = wer_scores.drop(wer_scores.index[excluded_trials])

        if systems_map_file != None:
            with open(systems_map_file, 'r') as ids:
                system_ids = ids.readlines()
                system_ids = [y.strip() for y in system_ids]

            for system in system_ids:
                info = system.split(":")
                final_scores['System'].replace(info[0], info[1], inplace=True)

        all_data_df = all_data_df.append(final_scores, ignore_index=False)

    print("Saving CSV file for all participants ...")
    csv_filename=wer_output_dir+"/all_data.csv"
    all_data_df.to_csv(csv_filename, encoding='utf-8', index=False)

    if average_WER:
        print("Calculating average WER across all participants and conditions ...")
        calc_average_WER(all_data_df, wer_output_dir)
