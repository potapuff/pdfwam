"""
mwam.py implements all MWAM classes, and binds instances of MWAMS to the AWAMs.

All MWAM classes inherits from AbstractWAM, which defines the list of WAMs.
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


__author__ = "Nils Ulltveit-Moe"
__updated__ = "$LastChangedDate$"
__version__ = "$Id$"

import new
from AbstractWAM import *
import re
import mimetypes
import urllib
import sys
from WAM_Results import eiaoMwamId

# Class name iterator
classNameIterator=1

# Default MWAM function
class MWAM(AbstractM):
   def result(self,s):
       return self.aWAM(self.awams[0],s)

class MWAMLower(AbstractM):
   def result(self,s):
       return self.aWAM(self.awams[0],s).lower()

# Mime type guessing MWAM
class MimeTypeMWAM(AbstractM):
   def result(self,s):
       t=mimetypes.guess_type(self.aWAM(self.awams[0],s))[0]
       if t==None:
          # No file extension, cannot deduct type
          return "Unknown"
       else:
          return t.lower()
          
class ClassIDMimeTypeMWAM(AbstractM):
   def result(self,s):
       classID=self.aWAM(self.awams[0],s)
       try:
           classID=classID.lower()
       except:
           pass
       if classID.startswith("java:"):
           return "application/x-java-applet"
       elif classID.startswith("clsid:"):
           #decode clsid here, if it is not possible to decide the mimetype
           #from the clsid, the plugin name or the id-string itself is returned
           if classID.startswith("clsid:CAFEEFAC".lower()):
               return "application/x-java-applet"
           elif classID == "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000".lower():
               return "application/x-shockwave-flash"
           elif classID == "clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B".lower():
               #Quicktime plugin
               return 'video/quicktime'
           elif classID == "clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA".lower():
               #Realplayer plugin, could be audio or video
               #return 'application/x-pn-realaudio'
               return "Realplayer-plugin"
           elif classID == "clsid:6BF52A52-394A-11D3-B153-00C04F79FAA6".lower() or classID == "clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95".lower():
               #Windows media player plugin
               return "Windows-media-player-plugin"
           else: 
               return classID
       else:
           t=mimetypes.guess_type(classID)[0]
       if t==None:
          # No file extension, cannot deduct type
          return "Unknown"
       else:
          return t.lower()

# Mime type for JavaScript event handlers
# NOTE: Assumes all event handlers are JavaScript.
# other script types may also be possible. (E.g. VBscript)
# However ignore that for now. Fix it if it proves to be a
# significant problem.
class JavaScriptEventMimeTypeMWAM(AbstractM):
   def result(self,s):
       return "text/javascript"
       
       
class JavaScriptLinkMimeTypeMWAM(AbstractM):
   def result(self,s):
       return "text/javascript"


# Mime type for applet element
class AppletMimeTypeMWAM(AbstractM):
   def result(self,s):
       return "application/x-java-applet"

# Link direction and mime type guessing MWAM
class MimeTypeLinkDirectionMWAM(AbstractM):
   def result(self,s):
       testSubject=self.aWAM("EIAO.A.10.7.4.2.HTML.2.1",(0,0))
       host=urllib.splithost(urllib.splittype(testSubject)[1])[0]
       linkURL=self.aWAM(self.awams[0],s)
       #sys.stderr.write("URL: "+linkURL)
       try:
           linkTo=urllib.splithost(urllib.splittype(linkURL)[1])[0]
       except:
           # Saw one occurrence of an url that were "-1"
           # which caused an exception in utllib
           return "Unknown"


       # If host part exists, or no host part, indicating
       # site internal link
       if linkTo==host or linkTo==None:
          self.type=MWAM.INTLINK
       else:
          self.type=MWAM.EXTLINK
       self.wamid=WAM_Results.eiaoMwamId[self.type]
       t=mimetypes.guess_type(linkURL)[0]
       if t==None:
          # No file extension, cannot deduct type
          return "Unknown"
       else:
          return t.lower()

# Class factory to generate MWAM classes
def addMWAM(parentKlass,awamId,mType):
    global classNameIterator
    name=".".join([eiaoMwamId[mType],str(classNameIterator)])
    nameSpace=eval("""{"__init__":lambda self,awamresult,**args: %s.__init__(self,awamresult,%s,%d,**args)}""" % (str(parentKlass).split(".")[-1],awamId,int(mType)))
    # WAMClasses.append(new.classobj(name,(parentKlass,),nameSpace))
    AppendKlass(new.classobj(name,(parentKlass,),nameSpace))    

# Add M-WAMs
# Technologies within a web page

addMWAM(MWAMLower,["EIAO.A.0.0.0.2.HTML.2.1"],MWAM.TECHNOLOGY)

addMWAM(MWAMLower,["EIAO.A.0.0.0.2.HTML.3.1"],MWAM.TECHNOLOGY)

addMWAM(ClassIDMimeTypeMWAM,["EIAO.A.0.0.0.2.HTML.4.1"],MWAM.TECHNOLOGY)

addMWAM(AppletMimeTypeMWAM,["EIAO.A.0.0.0.2.HTML.5.1"],MWAM.TECHNOLOGY)

addMWAM(JavaScriptEventMimeTypeMWAM,["EIAO.A.0.0.0.2.HTML.6.1"],MWAM.TECHNOLOGY)

addMWAM(JavaScriptLinkMimeTypeMWAM,["EIAO.A.0.0.0.2.HTML.7.1"],MWAM.TECHNOLOGY)

addMWAM(MWAMLower,["EIAO.A.0.0.0.2.HTML.8.1"],MWAM.TECHNOLOGY)

addMWAM(MimeTypeMWAM,["EIAO.A.0.0.0.2.HTML.9.1"],MWAM.TECHNOLOGY)

addMWAM(MimeTypeMWAM,["EIAO.A.0.0.0.2.HTML.10.1"],MWAM.TECHNOLOGY)

addMWAM(MWAMLower,["EIAO.A.10.11.1.2.HTTP.1.1"],MWAM.TECHNOLOGY)

# Technologies a web page links to
# Determins type (INTLINK or EXTLINK) itself.
addMWAM(MimeTypeLinkDirectionMWAM,["EIAO.A.0.0.0.2.HTML.11.1"],MWAM.INTLINK)

# Language M-WAMs
addMWAM(MWAM,["EIAO.A.10.4.3.1.HTML.2.1"],MWAM.LANGUAGE)

addMWAM(MWAM,["EIAO.A.0.0.0.2.HTML.1.1"],MWAM.LANGUAGE)

addMWAM(MWAM,["EIAO.A.10.4.3.1.HTTP.1.1"],MWAM.LANGUAGE)

# CSS media types
addMWAM(MWAM,["EIAO.A.0.0.0.2.CSS.1.1"],MWAM.MEDIATYPE)

addMWAM(MWAM,["EIAO.A.0.0.0.2.HTML.12.1"],MWAM.MEDIATYPE)

