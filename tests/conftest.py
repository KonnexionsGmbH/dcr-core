# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test config_setup.dcr.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG = "setup.cfg"
FILE_NAME_SETUP_CFG_BACKUP = "setup.cfg_backup"


