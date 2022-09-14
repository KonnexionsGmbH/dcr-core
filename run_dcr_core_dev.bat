@echo off

rem ----------------------------------------------------------------------------
rem
rem run_dcr_core_dev.bat: Process a given document.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set DCR_CORE_FULL_NAME_IN_DEFAULT=data\inbox_dev\Font_Variations.pdf
set DCR_CORE_ENVIRONMENT_TYPE=dev
set PYTHONPATH=src\dcr_core

if ["%1"] EQU [""] (
    set /P DCR_CORE_FULL_NAME_IN="Enter the full name of the document file [default: %DCR_CORE_FULL_NAME_IN_DEFAULT%] "

    if ["!DCR_CORE_FULL_NAME_IN!"] EQU [""] (
        set DCR_CORE_FULL_NAME_IN=%DCR_CORE_FULL_NAME_IN_DEFAULT%
    )
) else (
    set DCR_CORE_FULL_NAME_IN=%1
)

echo.
echo Script %0 is now running

if exist logging_dcr_core.log (
    del /f /q logging_dcr_core.log
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo DCR-CORE - Process a given document.
echo -----------------------------------------------------------------------
echo FULL_NAME_IN     : %DCR_CORE_FULL_NAME_IN%
echo ENVIRONMENT_TYPE : %DCR_CORE_ENVIRONMENT_TYPE%
echo PYTHONPATH       : %PYTHONPATH%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

pipenv run python src\launcher.py !DCR_CORE_FULL_NAME_IN!
if ERRORLEVEL 1 (
    echo Processing of the script: %0 - step: 'python src\launcher.py %DCR_CORE_FULL_NAME_IN%' was aborted
)

echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
