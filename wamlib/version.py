# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
# 

"""
Configuration and version information for the Relaxed based WAM.
"""

__author__ = "Morten Goodwin"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

import os

def get_tempdir():
   return os.environ.get('TMP',os.environ.get('TEMP',os.environ.get('TMPDIR','/tmp')))

def _(s):
   """
   Preparation for gettext i18n support.
   """
   return s

wamid   = _("http://www.egovmon.no/2.0/RelaxedWAM/")
wamname = _("Tingtun PDF WAM")
copyright = _("Copyright (c) 2013 Tingtun")
version = "2.2"
description = _("""PDF Web Accessibility Module for Tingtun derived from the eGovMon project""")

