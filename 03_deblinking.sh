#!/bin/bash

global_config_file=conf/global_settings.cfg
source $global_config_file

if test "$#" -ne 1; then
    echo "################################"
    echo "Usage:"
    echo "./03_deblinking.sh <path_to_csv_pupil_data>"
    echo ""
    echo "default path to data dir(Input): experiments/experiment_name/preprocessing/"
    echo "################################"
    exit 1
fi

data_dir=$1

if [ ! "$(ls -A ${data_dir})" ]; then
    echo "Please place your pupil data csv files in: ${data_dir}"
    exit 1
fi


####################################
########## Deblinking ##########
####################################

if [ "$DEBLINKING" = TRUE ]; then
    echo "Step 3: "
    echo "Deblinking pupil data in $data_dir ..."

    plots_dir=$experimentDir/deblinking/plots

    python scripts/deblinking.py $samplingFreq $missing_data_symbol $file_pattern $blink_threshold $max_trial_duration $start_blink_onset $end_blink_offset $plotting $nsubjects ${data_dir} $plots_dir $downsample $downsamplingFreq $exclusion_list $experimentDir

fi
