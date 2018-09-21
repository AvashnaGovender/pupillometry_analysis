#This script calculates the intelligibility scores for each participants:
#Input is the transcripts of each participant, the correct transcripts,
#mapping of participant (for multiple permutations)

import sys
import csv
import os
import pandas as pd

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

def save_WER(scores, n, systems, wer_output_dir, threshold, exclude_path ):
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
    scores_final.to_csv(csv_filename, encoding='utf-8', index=False)

    print("WER scores saved in: ",csv_filename)

    print("Generating exclude list for a threshold of",threshold,"%")

    exclusions = scores_final[scores_final['WER_Percent'] > int(threshold)]
    exclusion_list = exclusions.index.tolist()
    excluded_trials = n + "#"
    for trial in exclusion_list:
        trial_index = trial + 1
        excluded_trials = excluded_trials + str(trial_index) + " "

    with open(exclude_path, 'a') as exclusions:
        exclusions.write(excluded_trials)
        exclusions.write("\n")

    return 0


if __name__ == '__main__':

    #print(sys.argv)
    dataDir = sys.argv[1]
    nsubjects = sys.argv[2]
    exclude_list = sys.argv[3]
    file_pattern = sys.argv[4]
    group_mapppings = sys.argv[5]
    wer_output_dir = sys.argv[6]
    wer_threshold = sys.argv[7]
    exclude_path = sys.argv[8]

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
        save_WER(scores, n, systems, wer_output_dir, wer_threshold, exclude_path )
