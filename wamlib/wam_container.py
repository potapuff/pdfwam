# -- coding: utf-8
#! /usr/bin/env python
#
# Copyright (C) Tingtun AS 2013.
# 

"""
eGovMon WAM container, that binds AWAM results to BWAM object
instances, iterates through the BWAM objects, performs the 
BWAM tests on all AWAM locations and generates an EARL
report that is returned to the caller.

It defines one function bwams(file_or_url, resultMap, ruleset)
that takes the file or url to be tested, the resultmap and
optionally a specification of the BWAM rule set to use. bwams() 
performs the BWAM evaluation on the rule set and returns EARL.
"""

__author__ = "Anand B. Pillai"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

performanceTest = 0

import os
import datetime

import sys
import AbstractWAM
import report as a_report
import StringIO
from WAM_Results import *
import version

# Flag for time-profiling
profile = 0

# Flag whether BWAM test modules are loaded or not
bwamModulesLoaded=0

# Logger for logging messages
logger = None

def setLogger(logobject):
   global logger
   logger = logobject
   
def bwams(file_or_url, resultMap, testModuleList=None, ruleset=None, htmlHack=0, codeExtracts=0, content=""):
   """
   Perform BWAM tests on the AWAM results in resultMap.
   file_or_url is the URL being checked.
   ruleset indicates the enabled BWAM/MWAM rules.
   Returns: EARL

   file_or_url is the file or URL to be tested.
  
   resultMap is the AWAM result data structure

   testModuleList is a list of BWAM modules to load.

   htmlHack is a flag to enable HTML specific code for 
   conveying information about Tidy usage and HTML parsing
   failure via the earl:testSubject class. This should be
   moved into MWAMs in the future, since the BWAM code should
   be independent of the document format tested.
   """
   if ruleset == None:
      ruleset = ["ALL"]

   # Import all BWAM test modules specified.
   if not bwamModulesLoaded:
      for module in testModuleList:
          m = __import__(module, globals(), locals(), [''])
          sys.modules[module] = m

   # Create and EARL report object
   report = a_report.Report()

   # Set assertor
   report.assertor(version.wamid,
                   version.wamname,
                   version.description,
                   version.version)
   if resultMap:
      # AWAM results exist
      # Bind the A wam results to the B wams
      # and create a list of WAM rules, as
      # specified by ruleset. (default is all rules.)
      rules=AbstractWAM.WamRules(resultMap,ruleset,codeExtracts=codeExtracts, content=content)
      asserts = 0
      
      # Iterate through the BWAM rules
      for wam in rules.wamRules:
         try:
             for res in wam:
                 # Perform BWAM test and return next test 
                 # result for the given BWAM.

                 if res.type==BWAM:
                     # Report BWAM results as EARL assertions
                     report.assertion(res,codeExtracts=codeExtracts)
                     asserts += 1
                 else:
                     # Report MWAM meta data
                     report.metaData(res)
         except KeyError:
            # report.assertion(BWAM_Results(wam,NOTAPPLICABLE))
            # Do not send NotApplicable. This adds no value for the DW.
            pass

         except IndexError, e:
             pass
         except Exception, e:
            logger.error(str(e))
      
   else:
      # If null resultMap object is passed in, then
      # return EARL:cannotTell telling this is invalid.
      report.assertion(WAM_Results("EIAO.B.10.0.0.2.EXCEPTION.DEF.1",
                       "Relaxed validation failed",
                       "NULL resultMap object was returned",
                       CANNOTTELL))

   # Save the assertion ID number
   saveAssertionId()

   # Return the report
   return report.getReport()
