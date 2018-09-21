#!/bin/bash

if test "$#" -ne 1; then
    echo "################################"
    echo "Usage:"
    echo "./01_setup.sh <experiment name>"
    echo ""
    echo "Give your experiment a name eg., nancy_sus"
    echo "################################"
    exit 1
fi

current_working_dir=$(pwd)
experiments_dir=${current_working_dir}/experiments

myexperiment_name=$1

data_dir=${current_working_dir}/data
mydata_dir=${data_dir}/${myexperiment_name}
transcripts=${data_dir}/${myexperiment_name}/transcripts


myexperiment_dir=${experiments_dir}/${myexperiment_name}

mkdir -p ${data_dir}
mkdir -p ${mydata_dir}
mkdir -p $transcripts
mkdir -p ${experiments_dir}
mkdir -p ${myexperiment_dir}

mkdir -p ${myexperiment_dir}/preprocessing
mkdir -p ${myexperiment_dir}/preprocessing/WER
mkdir -p ${myexperiment_dir}/deblinking
mkdir -p ${myexperiment_dir}/deblinking/plots
mkdir -p ${myexperiment_dir}/smoothed
mkdir -p ${myexperiment_dir}/smoothed/plots
mkdir -p ${myexperiment_dir}/averaging
mkdir -p ${myexperiment_dir}/averaging/plots





global_config_file=conf/global_settings.cfg

### Set some default settings ###
echo "######################################" > $global_config_file
echo "############# PATHS ##################" >> $global_config_file
echo "######################################" >> $global_config_file
echo "" >> $global_config_file

echo "workDir=${current_working_dir}" >>  $global_config_file
echo "dataDir=${mydata_dir}" >>  $global_config_file
echo "experimentDir=${myexperiment_dir}" >>  $global_config_file


echo "" >> $global_config_file

echo "######################################" >> $global_config_file
echo "############# PARAMS FOR PREPROCESSING #################" >> $global_config_file
echo "######################################" >> $global_config_file
echo "" >> $global_config_file

echo "experiment_name=${myexperiment_name}" >> $global_config_file
echo "nsubjects=3          #Number of participants" >> $global_config_file
echo "blocks=6            #Number of blocks" >> $global_config_file
echo "trials=20             #Number of trials in each block" >> $global_config_file
echo "practicetrials=5            #Trials in Block 1" >> $global_config_file
echo "samplingFreq=500" >> $global_config_file
echo "downsamplingFreq=50" >> $global_config_file
echo "discardTrial=[1,2,3,21,22,23,41,42,43,61,62,63,81,82,83]  #Trials to exclude" >> $global_config_file
echo "file_pattern=p              #pattern of file eg. p1" >> $global_config_file
echo "file_extension=xlsx #Extension for input to preprocessing" >> $global_config_file
echo "group_mapppings=${mydata_dir}/mappings.txt" >> $global_config_file
echo "wer_threshold=20 #as a percentage" >> $global_config_file

echo "" >> $global_config_file

echo "######################################" >> $global_config_file
echo "############# PARAMS FOR DEBLINKING #################" >> $global_config_file
echo "######################################" >> $global_config_file
echo "" >> $global_config_file

echo "missing_data_symbol=." >> $global_config_file
echo "blink_threshold=0.2 #20%" >> $global_config_file
echo "max_trial_duration=7 #in seconds" >> $global_config_file
echo "start_blink_onset=50 #number of samples" >> $global_config_file
echo "end_blink_offset=80 #number of samples" >> $global_config_file
echo "exclusion_list=experiments/$experiment_name/preprocessing/exclude.txt #exclude file list" >> $global_config_file

echo "" >> $global_config_file

echo "############# DEBLINKING FLAGS #################" >> $global_config_file

echo "plotting=FALSE #plot at samplingFreq" >> $global_config_file
echo "downsample=TRUE #downsample data" >> $global_config_file

echo "" >> $global_config_file

echo "######################################" >> $global_config_file
echo "############# PARAMS FOR CORRECTION & SMOOTHING #################" >> $global_config_file
echo "######################################" >> $global_config_file

echo "actual_baseline=2" >> $global_config_file
echo "true_baseline=1" >> $global_config_file
echo "moving_average_window=10" >> $global_config_file
echo "smoothed_plots=TRUE" >> $global_config_file



echo "############# PROCESSING FLAGS #################" >> $global_config_file

echo "PREPROCESSING=TRUE" >> $global_config_file
echo "DEBLINKING=TRUE" >> $global_config_file
echo "CORRECTION_AND_SMOOTHING=TRUE" >> $global_config_file
echo "AVERAGING=TRUE" >> $global_config_file
echo "" >> $global_config_file

echo "Step 1 completed"
echo "Default configuration settings have been configured in \"$global_config_file\""
echo ""
echo "Make sure that you modify these parameters as per your data..."
echo "eg., sampling frequency, no. of participants etc"
echo ""

echo "setup is done...!"
echo ""
echo "Next you need to copy your pupil data files into here before proceeding:"
echo "\"${mydata_dir}\""
echo ""
