#!/bin/bash

global_config_file=conf/global_settings.cfg
source $global_config_file

if test "$#" -ne 1; then
    echo "################################"
    echo "Usage:"
    echo "./05_averaging_and_plotting.sh <path_to_csv_pupil_data>"
    echo ""
    echo "default path to data dir(Input): experiments/experiment_name/smoothed/"
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

if [ "$AVERAGING" = TRUE ]; then
    echo "Step 5: "
    echo "Averaging and plotting participant data ..."

    plots_dir=$experimentDir/averaging/plots

    if [ "$downsample" == TRUE ]; then
      s_frequency=$downsamplingFreq
    else
      s_frequency=$samplingFreq
    fi

    python scripts/average_plotting.py $nsubjects $file_pattern ${data_dir} $s_frequency $plots_dir $experimentDir


fi
