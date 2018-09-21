#!/bin/bash

global_config_file=conf/global_settings.cfg
source $global_config_file

if test "$#" -ne 1; then
    echo "################################"
    echo "Usage:"
    echo "./02_preprocessing.sh <path_to_pupil_data>"
    echo ""
    echo "default path to data dir(Input): data/experiment_name"
    echo "################################"
    exit 1
fi

data_dir=$1

if [ ! "$(ls -A ${data_dir})" ]; then
    echo "Please place your pupil data files in: ${data_dir}"
    exit 1
fi


####################################
########## Preprocessing ##########
####################################

preprocessing=true
concatenate=true  #concatenates all subjects data into a single CSV file
calc_intelligibility=true

if [ "$preprocessing" = true ]; then
    echo "Step 2: "
    echo "Preprocessing data in $data_dir ..."

    echo $discardTrial
    python scripts/preprocessing.py $discardTrial $practicetrials $nsubjects $file_pattern $file_extension $dataDir $experiment_name

fi

if [ "$concatenate" = true ]; then
    echo "Concatenating all the pupil data"

    cat experiments/$experiment_name/preprocessing/*.csv > experiments/$experiment_name/preprocessing/all_pupil_data.csv

    echo "done...!"
fi

if [ "$calc_intelligibility" = true ]; then
    echo "Calculating the intelligibility"

    wer_dir=experiments/$experiment_name/preprocessing/WER
    wer_exclude_list=experiments/$experiment_name/preprocessing/exclude.txt
    touch experiments/$experiment_name/preprocessing/exclude.txt

    python scripts/calc_intelligibility.py $dataDir/transcripts $nsubjects $exclusion_list $file_pattern $group_mapppings $wer_dir $wer_threshold $wer_exclude_list


    echo "done...!"
fi
