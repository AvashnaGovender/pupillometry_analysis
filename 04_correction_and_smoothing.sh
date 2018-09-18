#!/bin/bash

global_config_file=conf/global_settings.cfg
source $global_config_file

if test "$#" -ne 1; then
    echo "################################"
    echo "Usage:"
    echo "./04_correction_and_smoothing.sh <path_to_csv_pupil_data>"
    echo ""
    echo "default path to data dir(Input): experiments/experiment_name/deblinking/"
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

if [ "$CORRECTION_AND_SMOOTHING" = TRUE ]; then
    echo "Step 4: "
    echo "Applying baseline correction on pupil data and smoothing ..."

    plots_dir=$experimentDir/smoothed/plots

    if [ "$downsample" == TRUE ]; then
      s_frequency=$downsamplingFreq
    else
        s_frequency=$samplingFreq
    fi

    #echo $s_frequency
    python scripts/baseline_correction_smoothing.py $s_frequency $actual_baseline $true_baseline $moving_average_window $nsubjects $file_pattern ${data_dir} $experimentDir $plots_dir

fi
