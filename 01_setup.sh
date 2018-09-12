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

myexperiment_dir=${experiments_dir}/${myexperiment_name}

mkdir -p ${data_dir}
mkdir -p ${mydata_dir}
mkdir -p ${experiments_dir}
mkdir -p ${myexperiment_dir}

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
echo "############# PARAMS #################" >> $global_config_file
echo "######################################" >> $global_config_file
echo "" >> $global_config_file

echo "experiment_name=${myexperiment_name}" >> $global_config_file
echo "nsubjects=5          #Number of participants" >> $global_config_file
echo "blocks=6            #Number of blocks" >> $global_config_file
echo "trials=20             #Number of trials in each block" >> $global_config_file
echo "practicetrials=5            #Trials in Block 1" >> $global_config_file
echo "samplingFreq=500" >> $global_config_file
echo "downsamplingFreq=50" >> $global_config_file
echo "discardTrial=[1,2,3,21,22,23,41,42,43,61,62,63,81,82,83]  #Trials to exclude" >> $global_config_file
echo "" >> $global_config_file

echo "file_pattern=p              #pattern of file eg. p1" >> $global_config_file
echo "file_extension=xlsx" >> $global_config_file

echo "" >> $global_config_file

echo "PREPROCESSING=TRUE" >> $global_config_file
echo "DEBLINKING=TRUE" >> $global_config_file
echo "DOWNSAMPLING=TRUE" >> $global_config_file
echo "TRIALEXCLUSION=TRUE" >> $global_config_file
echo "AVERAGING=TRUE" >> $global_config_file
echo "SMOOTHING=TRUE" >> $
echo "PLOTTING=TRUE" >> $global_config_file


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
