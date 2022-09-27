@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr_core_dev.bat: Process one or more given documents.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CORE_ENVIRONMENT_TYPE=dev
set DCR_CORE_INPUT_SOURCE_DEFAULT=data\inbox_dev
set PYTHONPATH=src\dcr_core

if ["%1"] EQU [""] (
    set /P DCR_CORE_INPUT_SOURCE="Enter the full name of a document file or a file directory containing the document files to process [default: %DCR_CORE_INPUT_SOURCE_DEFAULT%] "

    if ["!DCR_CORE_INPUT_SOURCE!"] EQU [""] (
        set DCR_CORE_INPUT_SOURCE=%DCR_CORE_INPUT_SOURCE_DEFAULT%
    )
) else (
    set DCR_CORE_INPUT_SOURCE=%1
)

echo.
echo Script %0 is now running

if exist logging_dcr_core.log (
    del /f /q logging_dcr_core.log
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo DCR-CORE - Process one or more given documents.
echo -----------------------------------------------------------------------
echo ENVIRONMENT_TYPE : %DCR_CORE_ENVIRONMENT_TYPE%
echo INPUT_SOURCE     : %DCR_CORE_INPUT_SOURCE%
echo PYTHONPATH       : %PYTHONPATH%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

pipenv run python src\launcher.py !DCR_CORE_INPUT_SOURCE!
if ERRORLEVEL 1 (
    echo Processing of the script: %0 - step: 'python src\launcher.py %DCR_CORE_INPUT_SOURCE%' was aborted
)

echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================