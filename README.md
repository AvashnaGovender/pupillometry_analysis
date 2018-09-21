# Toolkit to analyse data for Pupillometry

This repo offers scripts and tools to analyse pupil data that has been collected from an eye-tracker.

The INPUTS required to use the toolkit is:

- Place all pupil data (unprocessed) in the data/<experiment_name> directory
Example format:
<participant ID>.xlsx

- For intelligibility scoring - A mappings.txt file is required
Example format:
p1 1 group1_correct.txt ['I','C','G','A','E']
p2 2 group2_correct.txt ['G','I','A','E','C']
p1 - participant ID
1 - group number
group1_correct.txt - correct group transcriptions
['I','C','G','A','E'] - system ordering for that group

- in data/transcripts:
Text files for recalled transcriptions for each participant as well as each of the correct group transcriptions
Example format:
<participant ID>.txt
group1_correct.txt

________________________________________________

1. First run: ./01_setup <experiment_name>
2. Edit the config file in conf/global_settings.cfg
3. ./02_preprocessing.sh data/<experiment_name>
    There are 3 flags in this script:
    preprocessing=true
    concatenate=true  
    calc_intelligibility=true
    which can be switched on/off depending on what you wish to do.

    -- preprocessing: Formats the data into a format that can be used for remaining processes which is saved in      expriments/preprocessing. This is created for SR Eyelink 1000 Plus which generates an xlsx file.
    --concatenate: Concatenated all the preprocessed files of all participants into a single file
    --calc_intelligibility: Calculates the WER scores and saves as CSV in expriments/preprocessing/WER
    --calc_intelligibility: Generates an exclude_list.txt based on the threshold set in the config file (excludes trials with WER > threshold)

    If you processed you own data, then it should follow the format:
    [INDEX,TRIAL_INDEX,PUPIL_SIZE,STIMULI,SYSTEMS,BLOCKS,SUBJECT]

4. ./03_deblinking.sh <experiments/<experiment_name>/preprocessing/> or the path to where your data lies
    This script deblinks the data and updates the table above and saves as CSV in <experiments/<experiment_name>/deblinking
    It also gives you the option to downsample your data if needed. (This is set in the config file)
    It also plots each trial for each participant and saves this in plots - GOOD for debugging!


5. ./04_correction_and_smoothing.sh <experiments/<experiment_name>/deblinking/>
    This script calculates the baseline and performs baseline correction, following by a moving average smoothing filter
    The corrected and smoothed data is stored as a CSV file in <experiments/<experiment_name>/smoothed/>
    It also plots each trial for each participant and saves this in plots - GOOD for debugging!


6. ./05_average_plotting.sh <experiments/<experiment_name>/smoothed/>
    This script averages across the trials for each participant with respect to the system/condition
    It averages per participant as well as for the final plot with all data averaged.
    The averaged data is stored as a CSV file in <experiments/<experiment_name>/averaging/>
