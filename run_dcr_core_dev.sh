#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_dcr_core_dev.sh: Process a given document.
#
# ----------------------------------------------------------------------------------

export DCR_CORE_FULL_NAME_IN_DEFAULT=data/inbox_dev/Font_Variations.pdf
export DCR_CORE_ENVIRONMENT_TYPE=dev
export PYTHONPATH=src/dcr_core

if [ -z "$1" ]; then
    read -rp "Enter the full name of the document file [default: ${DCR_CORE_FULL_NAME_IN_DEFAULT}] " DCR_CORE_FULL_NAME_IN
    export DCR_CORE_FULL_NAME_IN=${DCR_CORE_FULL_NAME_IN:-$DCR_CORE_FULL_NAME_IN_DEFAULT}
else
    export DCR_CORE_FULL_NAME_IN=$1
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
echo "DCR-CORE - Process a given document."
echo "------------------------------------------------------------------------------"
echo "FULL_NAME_IN     : ${DCR_CORE_FULL_NAME_IN}"
echo "ENVIRONMENT_TYPE : ${DCR_CORE_ENVIRONMENT_TYPE}"
echo "PYTHONPATH       : ${PYTHONPATH}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="

pipenv run python src/launcher.py "${DCR_CORE_FULL_NAME_IN}"

echo ""
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="
