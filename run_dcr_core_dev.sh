#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr_core_dev.sh: Process one or more given documents.
#
# ----------------------------------------------------------------------------------

export DCR_CORE_ENVIRONMENT_TYPE=dev
export DCR_CORE_INPUT_SOURCE_DEFAULT=data/inbox_dev
export PYTHONPATH=src/dcr_core

if [ -z "$1" ]; then
    read -rp "Enter the full name of a document file or a file directory containing the document files to process [default: ${DCR_CORE_INPUT_SOURCE_DEFAULT}] " DCR_CORE_INPUT_SOURCE
    export DCR_CORE_INPUT_SOURCE=${DCR_CORE_INPUT_SOURCE:-$DCR_CORE_INPUT_SOURCE_DEFAULT}
else
    export DCR_CORE_INPUT_SOURCE=$1
fi

echo ""
echo "Script $0 is now running"

rm -f logging_dcr_core.log
export LOG_FILE=logging_dcr_core.log
rm -f run_dcr_core_dev.log

echo ""
echo "You can find the run log in the file $LOG_FILE"
echo ""

exec &> >(tee -i $LOG_FILE) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "DCR-CORE - Process one or more given documents."
echo "------------------------------------------------------------------------------"
echo "ENVIRONMENT_TYPE : ${DCR_CORE_ENVIRONMENT_TYPE}"
echo "INPUT_SOURCE     : ${DCR_CORE_INPUT_SOURCE}"
echo "PYTHONPATH       : ${PYTHONPATH}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="

pipenv run python src/launcher.py "${DCR_CORE_INPUT_SOURCE}"

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
