#! /usr/bin/env python

# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
#

"""
Takes WAM_Result objects from the BWAM assessments and wraps them in a pretty data-structure.
"""
__author__ = "Christian Amble"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

from WAM_Results import *
import version

import urllib

class Report:
    """ Class for generating datastructure from WAM_Results objects. """
    def __init__(self):
        self.reports = {}
    def testSubject(self, *args, **kargs):
        pass
    def assertor(self, wamid, wamname, description, version):
        pass
    def assertion(self, bresult,codeExtracts=0):
        id = bresult.earlRequirementId()
        try:
            self.reports[id]
        except:
            self.reports[id] = []
        struc = {}
        struc["type"] = "assertion"
        struc["line"] = bresult.eiaoLine()
        struc["column"] = bresult.eiaoColumn()
        struc["mode"]   = bresult.earlMode().split("#")[1]
        struc["result"] = float(bresult.result)
        if codeExtracts:
            struc["xhtml"]  = bresult.xhtml
        if bresult.mode == HEURISTIC:
            struc["resultProb"] = float(bresult.prob)
        if bresult.message:
            struc["message"] = bresult.earlMessage()
        
        self.reports[id].append(struc)
    def metaData(self, bresult):
        id = bresult.earlRequirementId()
        try:
            self.reports[id]
        except:
            self.reports[id] = []
        struc = {}
        struc["type"] = "metadata"
        struc["line"] = bresult.eiaoLine()
        struc["column"] = bresult.eiaoColumn()
        struc["what"] = bresult.eiaoType().split("#")[1]
        struc["value"] = bresult.eiaoValue()
        self.reports[id].append(struc)
    def getReport(self):
        return self.reports
