# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
# 
#

"""
pdfmwam.py implements all PDF MWAM classes, and binds instances of MWAMS to the AWAMs.

All MWAM classes inherits from AbstractWAM, which defines the list of WAMs.
"""

__author__ = "Nils Ulltveit-Moe"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

import new
from AbstractWAM import *
import re
import urllib
import sys
from WAM_Results import egovmonMwamId

# Class name iterator
classNameIterator=1

# Default MWAM function
class MWAM(AbstractM):
   def result(self,s):
       return self.aWAM(self.awams[0],s)

# Class factory to generate MWAM classes
def addMWAM(parentKlass,awamId,mType):
    global classNameIterator
    name=".".join([egovmonMwamId[mType],str(classNameIterator)])
    nameSpace=eval("""{"__init__":lambda self,awamresult,**args: %s.__init__(self,awamresult,%s,%d, **args)}""" % (str(parentKlass).split(".")[-1],awamId,int(mType)))
    # WAMClasses.append(new.classobj(name,(parentKlass,),nameSpace))
    AppendKlass(new.classobj(name,(parentKlass,),nameSpace))    

# Add M-WAMs


addMWAM(MWAM,["EGOVMON.PDF.PROP.01"],MWAM.TITLE)
addMWAM(MWAM,["EGOVMON.PDF.PROP.02"],MWAM.AUTHOR)
addMWAM(MWAM,["EGOVMON.PDF.PROP.03"],MWAM.VERSION)
addMWAM(MWAM,["EGOVMON.PDF.PROP.04"],MWAM.CREATION_TIME)
addMWAM(MWAM,["EGOVMON.PDF.PROP.05"],MWAM.MODIFICATION_TIME)
addMWAM(MWAM,["EGOVMON.PDF.PROP.06"],MWAM.PRODUCER)
addMWAM(MWAM,["EGOVMON.PDF.PROP.07"],MWAM.CREATOR)
# Is this correct ?
addMWAM(MWAM,["EGOVMON.A.0.0.0.4.PDF.4.1"],MWAM.LANGUAGE)

#
