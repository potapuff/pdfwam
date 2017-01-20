#!/usr/bin/python
"""
Configuration and version information for the Relaxed based WAM.
"""

#      Copyright 2008-2010 eGovMon
#      This program is distributed under the terms of the GNU General
#      Public License.
#
#  This file is part of the eGovernment Monitoring
#  (eGovMon)
#
#  eGovMon is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  eGovMon is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with eGovMon; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
#  MA 02110-1301 USA

__author__ = "Morten Goodwin"
__updated__ = "$LastChangedDate$"
__version__ = "$Id: version.py 1974 2006-04-24 18:35:47Z num $"


import os

def get_tempdir():
   return os.environ.get('TMP',os.environ.get('TEMP',os.environ.get('TMPDIR','/tmp')))

def _(s):
   """
   Preparation for gettext i18n support.
   """
   return s

wamid   = _("http://www.eiao.net/2.3/PDFWAM/")
wamname = _("EGOVMON PDF WAM")
copyright = _("Copyright (c) 2009, EGOVMON project. GNU GPL")
version = "0.4"
description = _("""PDF WAM""")
dumpfile=os.path.join(get_tempdir(),'PDFWAM.dump')
