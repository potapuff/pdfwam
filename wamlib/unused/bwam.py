# -- coding: utf-8
#
#
# Copyright (C) Tingtun AS 2013.
#

"""
bwam.py implements BWAM classes that cannot be automatically generated
by the BWAM parser (d123.py)

All BWAM classes inherits from AbstractB, which defines the list of WAMs.
"""

__author__ = "Annika Nietzio, Nils Ulltveit-Moe"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

from AbstractWAM import AppendKlass, AbstractB
import re
import string

# Default pass value
DEFAULT_PASS=(0,0,0)

# Default fail value
DEFAULT_FAIL=(0,0,1)

# BWAM implementation

class UWEM_B_10_1_1_3_HTML_DEF_6_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.1.1.3.HTML.DEF.6.1 - <embed> used

      History
      Update for UWEM 1.2
      FTB
      2008-01-08

      WCAG 1.0 reference: Checkpoint 1.1: Provide a text equivalent for every non-text element (e.g., via "alt", "longdesc", or in element content). This includes: images, graphical representations of text (including symbols), image map regions, animations (e.g., animated GIFs), applets and programmatic objects, ascii art, frames, scripts, images used as list bullets, spacers, graphical buttons, sounds (played with or without user interaction), stand-alone audio files, audio tracks of video, and video. [Priority 1]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.1.1.3.HTML.DEF.6.1",[
          'EIAO.A.10.1.1.2.HTML.2.1',
      ],default=DEFAULT_PASS, **args)
      # If no <embed>. tjen the default test result is pass.
      self.title = 'The <embed> element is used.'
      self.description = """Checkpoint 1.1: Provide a text equivalent for every non-text element (e.g., via "alt", "longdesc", or in element content). This includes: images, graphical representations of text (including symbols), image map regions, animations (e.g., animated GIFs), applets and programmatic objects, ascii art, frames, scripts, images used as list bullets, spacers, graphical buttons, sounds (played with or without user interaction), stand-alone audio files, audio tracks of video, and video. [Priority 1]"""

   def result(self,s):
      return  int(self.aWAM("EIAO.A.10.1.1.2.HTML.2.1",s))

AppendKlass(UWEM_B_10_1_1_3_HTML_DEF_6_1)



class UWEM_B_10_3_2_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult,**args):
      """
      UWEM.B.10.3.2.3.HTML.DEF.1.1 - Invalid DOCTYPE

      History
      Initial version
      FTB
      2006-09-26

      Checkpoint 3.2: Create documents that validate to published formal grammars. 
      [Priority 2]

      Mode: Fully automatable.

      Is EIAO.A.10.11.1.1.HTML.1.1(s) contained in "Recommended DTDs to use in your Web 
      document" available at http://www.w3.org/QA/2002/04/valid-dtd-list.html ?
        0 if true.
        1 if false.
      """
      AbstractB.__init__(self,awamresult,'UWEM.B.10.3.2.3.HTML.DEF.1.1',["EIAO.A.10.11.1.1.HTML.1.1"])
      self.title = 'The inspected resource does not contain a valid document type declaration.'
      self.description = """Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]"""
      self.r=re.compile(r"(X?HTML)\s+(\d\.\d+)")

   def result(self,s):
      awam=self.aWAM("EIAO.A.10.11.1.1.HTML.1.1",s)
      srch=self.r.search(awam.upper())
      if srch==None:
          return 1
      g=srch.groups()
      if g==None:
          return 1
      else:
          htmlver=" ".join(g)
          if string.find(htmlver,"HTML") >=0:
              return 0
          else:
              return 1


AppendKlass(UWEM_B_10_3_2_3_HTML_DEF_1_1)

class UWEM_B_10_3_6_3_HTML_DEF_3_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.3.6.3.HTML.DEF.3.1 - Simulation of numbered list

      History
      Initial version
      FTB
      2006-09-27

      WCAG 1.0 reference: Checkpoint 3.6: Mark up lists and list items properly. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.3.6.3.HTML.DEF.3.1",[
          'EIAO.A.10.3.6.2.HTML.1.1',
      ],default=DEFAULT_PASS, **args)
      self.title = 'The inspected (X)HTML resource contains texts that simulates a numbered list.'
      self.description = """Checkpoint 3.6: Mark up lists and list items properly. [Priority 2]"""

   def result(self,s):
      return  int(self.aWAM("EIAO.A.10.3.6.2.HTML.1.1",s))

AppendKlass(UWEM_B_10_3_6_3_HTML_DEF_3_1)

class UWEM_B_10_11_1_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.11.1.3.HTML.DEF.1.1 - Non-Use of latest W3C technologies

      History
      Initial version
      FTB
      2006-09-28

      WCAG 1.0 reference: Checkpoint 11.1: Use W3C technologies when they are available and appropriate for a task and use the latest versions when supported.[Priority 2]


      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,'UWEM.B.10.11.1.3.HTML.DEF.1.1',
                         ["EIAO.A.10.11.1.1.HTML.1.1",
                          "EIAO.A.10.11.1.2.HTTP.1.1"], **args)
      self.title = 'The inspected (X)HTML resource does not use the latest W3C technologies.'
      self.description = """Checkpoint 11.1: Use W3C technologies when they are available and appropriate for a task and use the latest versions when supported.[Priority 2]"""

   def result(self,s):
      awam=self.aWAM("EIAO.A.10.11.1.1.HTML.1.1",s)
      if type(awam)==type(""):
         if(self.aWAM("EIAO.A.10.11.1.2.HTTP.1.1",s) == 'text/html'):
            if (string.find(awam,"HTML 4.01") >=0 or string.find(awam,"XHTML 1.0") >=0):
               return 0
            else:
               return 1
         elif (self.aWAM("EIAO.A.10.11.1.2.HTTP.1.1",s) == 'application/xhtml+xml'):
            if (string.find(awam,"XHTML 1.1") >=0):
               return 0
            else:
               return 1
         else:
               return 1
      else:
         return 1

AppendKlass(UWEM_B_10_11_1_3_HTML_DEF_1_1)

class UWEM_B_10_3_2_3_CSS_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.3.2.3.CSS.DEF.1.1 - Formal schema violations

      History
      Initial version based on D3.3.2
      2008-01-31

      WCAG 1.0 reference: Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.3.2.3.CSS.DEF.1.1",[
          'EIAO.A.10.3.2.2.CSS.1.1'],default=DEFAULT_PASS, **args)
      self.title = 'The inspected (X)HTML file contains at least one violation of the formal schema of HTML (or XHTML resp.).'
      self.description = """Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]"""

   def result(self,s):
      awam=self.aWAM("EIAO.A.10.3.2.2.CSS.1.1",s)
       
      if type(awam) == type(""):
         if awam=="":
            self.title="Validation OK"
            return 0
         else:
            self.title=awam
            return 1
      elif type(awam) == type(1):
         return awam

AppendKlass(UWEM_B_10_3_2_3_CSS_DEF_1_1)


class UWEM_B_10_3_2_3_HTML_DEF_2_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.3.2.3.HTML.DEF.2.1 - Formal schema violations

      History
      Initial version
      FTB
      2006-09-25

      WCAG 1.0 reference: Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.3.2.3.HTML.DEF.2.1",[
          'EIAO.A.10.3.2.2.HTML.2.1'],default=DEFAULT_PASS, **args
      )
      self.title = 'The inspected (X)HTML file contains at least one violation of the formal schema of HTML (or XHTML resp.).'
      self.description = """Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]"""

   def result(self,s):
      awam=self.aWAM("EIAO.A.10.3.2.2.HTML.2.1",s)
      
      if type(awam) == type(""):
         if awam=="":
            self.title="Validation OK"
            return 0
         else:
            self.title=awam
            return 1
      elif type(awam) == type(1):
         return awam

AppendKlass(UWEM_B_10_3_2_3_HTML_DEF_2_1)

class UWEM_B_10_7_2_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.7.2.3.HTML.DEF.1.1 - <blink> used

      History
      Version based on D3.1.1.
      FTB
      2006-09-27

      WCAG 1.0 reference: Checkpoint 7.2: Until user agents allow users to control blinking, avoid causing content to blink (i.e., change presentation at a regular rate, such as turning on and off). [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.7.2.3.HTML.DEF.1.1",[
          'EIAO.A.10.7.2.1.HTML.1.1',
      ],default=DEFAULT_PASS, **args)
      # Pass if no <blink> is found
      self.title = 'The <blink> element is used.'
      self.description = """Checkpoint 7.2: Until user agents allow users to control blinking, avoid causing content to blink (i.e., change presentation at a regular rate, such as turning on and off). [Priority 2]"""

   def result(self,s):
      return  int(self.aWAM("EIAO.A.10.7.2.1.HTML.1.1",s))

AppendKlass(UWEM_B_10_7_2_3_HTML_DEF_1_1)


class UWEM_B_10_7_2_3_CSS_DEF_2_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.7.2.3.CSS.DEF.2.1 - <blink> used

      History
      Version based on D3.3.2.
      2008-01-31

      WCAG 1.0 reference: Checkpoint 7.2: Until user agents allow users to control blinking, avoid causing content to blink (i.e., change presentation at a regular rate, such as turning on and off). [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.7.2.3.CSS.DEF.2.1",[
          'EIAO.A.10.7.2.2.CSS.1.1',
      ],default=DEFAULT_PASS, **args)
      # Pass if no <blink> is found
      self.title = 'The <blink> element is used in CSS.'
      self.description = """Checkpoint 7.2: Until user agents allow users to control blinking, avoid causing content to blink (i.e., change presentation at a regular rate, such as turning on and off). [Priority 2]"""

   def result(self,s):
      return  int(self.aWAM("EIAO.A.10.7.2.2.CSS.1.1",s))

AppendKlass(UWEM_B_10_7_2_3_CSS_DEF_2_1)

class UWEM_B_10_7_3_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.7.3.3.HTML.DEF.1.1 - <marquee> used

      History
      Version based on D3.1.1.
      FTB
      2006-07-18

      WCAG 1.0 reference: Checkpoint 7.3: Until user agents allow users to freeze moving content, avoid movement in pages. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.7.3.3.HTML.DEF.1.1",[
          'EIAO.A.10.7.3.2.HTML.1.1',
      ],default=DEFAULT_PASS, **args)
      self.title = 'The <marquee> element is used.'
      self.description = """Checkpoint 7.3: Until user agents allow users to freeze moving content, avoid movement in pages. [Priority 2]"""

   def result(self,s):
      return  int(self.aWAM("EIAO.A.10.7.3.2.HTML.1.1",s))

AppendKlass(UWEM_B_10_7_3_3_HTML_DEF_1_1)


class UWEM_B_10_7_4_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.7.4.3.HTML.DEF.1.1 - Page refreshing

      History
      Initial version
      FTB
      2006-09-28

      WCAG 1.0 reference: Checkpoint 7.4: Until user agents provide the ability to stop the refresh, do not create periodically auto-refreshing pages. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.7.4.3.HTML.DEF.1.1",[
          'EIAO.A.10.7.4.2.HTML.1.2',
      ], **args)
      self.title = 'The inspected (X)HTML resource uses <meta http-equiv="refresh"> to create page refreshing.'
      self.description = """Checkpoint 7.4: Until user agents provide the ability to stop the refresh, do not create periodically auto-refreshing pages. [Priority 2]"""

   def result(self,s):
      return  string.find(self.aWAM("EIAO.A.10.7.4.2.HTML.2.1",(0,0)),
                          self.aWAM("EIAO.A.10.7.4.2.HTML.1.2",s)) >=0

AppendKlass(UWEM_B_10_7_4_3_HTML_DEF_1_1)

class UWEM_B_10_7_5_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.7.5.3.HTML.DEF.1.1 - Page redirecting

      History
      Initial version
      FTB
      2006-09-28

      WCAG 1.0 reference: Checkpoint 7.5: Until user agents provide the ability to stop auto-redirect, do not use markup to redirect pages automatically. Instead, configure the server to perform redirects. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.7.5.3.HTML.DEF.1.1",[
          'EIAO.A.10.7.4.2.HTML.1.2',
      ], **args)
      self.title = 'The inspected (X)HTML resource uses <meta http-equiv="refresh"> to create page redirecting.'
      self.description = """Checkpoint 7.5: Until user agents provide the ability to stop auto-redirect, do not use markup to redirect pages automatically. Instead, configure the server to perform redirects. [Priority 2]"""

   def result(self,s):
      return  not ( string.find(self.aWAM("EIAO.A.10.7.4.2.HTML.2.1",(0,0)),
                                self.aWAM("EIAO.A.10.7.4.2.HTML.1.2",s)) >=0)

AppendKlass(UWEM_B_10_7_5_3_HTML_DEF_1_1)

class UWEM_B_10_6_4_3_HTML_DEF_1_1(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.6.4.3.HTML.DEF.1.1 - Mouse-specific event handler

      History
      Updated for UWEM 1.2
      FTB
      2008-01-09

      WCAG 1.0 reference: Checkpoint 6.4: For scripts and applets, ensure that event handlers are input device-independent. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.6.4.3.HTML.DEF.1.1",[
          'EIAO.A.10.6.4.2.HTML.1.2',
          'EIAO.A.10.6.4.2.HTML.2.2',
          'EIAO.A.10.6.4.3.HTML.3.1',
          'EIAO.A.10.6.4.2.HTML.4.2',
          'EIAO.A.10.6.4.2.HTML.5.2',
      ], **args)
      self.title = 'The inspected element used a mouse-specific event handler but does not provide a keyboard-specific or device-independent even handler with that triggers the same functionality.'
      self.description = """Checkpoint 6.4: For scripts and applets, ensure that event handlers are input device-independent. [Priority 2]"""

   def result(self,s):
      return (int(self.aWAM("EIAO.A.10.6.4.2.HTML.1.2",s)) or 
              int(self.aWAM("EIAO.A.10.6.4.2.HTML.2.2",s)) or 
              int(self.aWAM("EIAO.A.10.6.4.3.HTML.3.1",s)) or 
              int(self.aWAM("EIAO.A.10.6.4.2.HTML.4.2",s)) or 
              int(self.aWAM("EIAO.A.10.6.4.2.HTML.5.2",s)) )

AppendKlass(UWEM_B_10_6_4_3_HTML_DEF_1_1)

class UWEM_B_10_13_1_3_HTML_DEF_1_1_a(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.13.1.3.HTML.DEF.1.1 - Different link targets for <a>

      History
      Bug fix for #127
      FTB
      2006-12-08

      WCAG 1.0 reference: Checkpoint 13.1: Clearly identify the target of each link. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.13.1.3.HTML.DEF.1.1",[
          'EIAO.A.10.13.1.2.HTML.1.1', # (Link text, <a>)
      ], **args)
      self.title = 'The inspected <a> element has the same element text and the same title as another <a> element in the (X)HTML resource but a different link target (href attribute).'
      self.description = """Checkpoint 13.1: Clearly identify the target of each link. [Priority 2]"""

   def result(self,s):
      # A is all locations except s
      A=self.locations[:]
      A.remove(s)
      for a in A:
         if (self.aWAM("EIAO.A.10.13.1.2.HTML.1.1",s) == self.aWAM("EIAO.A.10.13.1.2.HTML.1.1",a) 
            and self.aWAM("EIAO.A.10.13.1.2.HTML.2.1",s) == self.aWAM("EIAO.A.10.13.1.2.HTML.2.1",a)
            and self.aWAM("EIAO.A.10.13.1.2.HTML.4.1",s) == self.aWAM("EIAO.A.10.13.1.2.HTML.4.1",a)
            and self.aWAM("EIAO.A.0.0.0.2.HTML.11.1",s) != self.aWAM("EIAO.A.0.0.0.2.HTML.11.1",a)):
            return 1
      return 0

AppendKlass(UWEM_B_10_13_1_3_HTML_DEF_1_1_a)

class UWEM_B_10_13_1_3_HTML_DEF_1_1_area(AbstractB):
   def __init__(self,awamresult, **args):
      """
      UWEM.B.10.13.1.3.HTML.DEF.1.1 - Different link targets for <area>

      History
      Bug fix for #127
      FTB
      2006-12-08
      
      WCAG 1.0 reference: Checkpoint 13.1: Clearly identify the target of each link. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"UWEM.B.10.13.1.3.HTML.DEF.1.1",[
          'EIAO.A.10.13.1.2.HTML.3.1', # (<area> alt text, <area>)
      ], **args)
      self.title = 'The inspected <a> element has the same element text and the same title as another <a> element in the (X)HTML resource but a different link target (href attribute).'
      self.description = """Checkpoint 13.1: Clearly identify the target of each link. [Priority 2]"""

   def result(self,s):
      # A is all locations except s
      A=self.locations[:]
      A.remove(s)
      for a in A:
         if (self.aWAM("EIAO.A.10.13.1.2.HTML.3.1",s) == self.aWAM("EIAO.A.10.13.1.2.HTML.3.1",a) 
            and self.aWAM("EIAO.A.10.13.1.2.HTML.2.1",s) == self.aWAM("EIAO.A.10.13.1.2.HTML.2.1",a)
            and self.aWAM("EIAO.A.0.0.0.2.HTML.11.1",s) != self.aWAM("EIAO.A.0.0.0.2.HTML.11.1",a)):
            return 1
      return 0

AppendKlass(UWEM_B_10_13_1_3_HTML_DEF_1_1_area)

