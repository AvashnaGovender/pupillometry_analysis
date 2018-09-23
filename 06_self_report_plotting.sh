#!/bin/bash

global_config_file=conf/global_settings.cfg
source $global_config_file

if test "$#" -ne 1; then
    echo "################################"
    echo "Usage:"
    echo "./06_self_report_plotting.sh <path_to_self_report_csvs>"
    echo ""
    echo "default path to data dir(Input): data/<experiment_name>/"
    echo "################################"
    exit 1
fi

data_dir=$1

if [ ! "$(ls -A ${data_dir})" ]; then
    echo "Please place your self report csv files in: ${data_dir}"
    exit 1
fi


####################################
########## Self Report Analysis ##########
####################################

if [ "$SELF_REPORT" = TRUE ]; then
    echo "Step 6: "
    echo "Analysing and plotting self-report measures ..."

    plots_dir=$experimentDir/self_reporting/plots

    if [ "$system_mapping" == TRUE ]; then
      systems_map_file=${system_mapping_filepath}
    else
      systems_map_file=None
    fi

    csv_filepath=${data_dir}/self_report.csv
    python scripts/self_reporting.py $csv_filepath $systems_map_file $plots_dir $experimentDir/self_reporting

    echo "Done!"
fi
