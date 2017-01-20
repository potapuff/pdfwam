# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
#

"""
pdfbwam.py implements BWAM classes for PDF tests.

All BWAM classes inherits from AbstractB, which defines the list of WAMs.
"""

__author__ = "Nils Ulltveit-Moe"
__updated__ = "$LastChangedDate$"
__version__ = "$Id$"

from AbstractWAM import AppendKlass, AbstractB
import re
import string

# Default pass value
DEFAULT_PASS=(0,0,0)

# Default fail value
DEFAULT_FAIL=(0,0,1)

# PDF BWAM implementation

class EGOVMON_PDF_01(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.01 - Non-text content without Alt or ActualText attribute

      History
      Initial version
      UIA
      2008-10-07

      WCAG 1.0 reference: Checkpoint 1.1: Provide a text equivalent for every non-text element (e.g., via "Alt", "ActualText", or in element content). This includes: images, graphical representations of text (including symbols), image map regions, animations (e.g., animated GIFs), applets and programmatic objects, ascii art, frames, scripts, images used as list bullets, spacers, graphical buttons, sounds (played with or without user interaction), stand-alone audio files, audio tracks of video, and video. [Priority 1]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.01",[
          'EIAO.A.10.1.1.4.PDF.1.1','EIAO.A.10.1.1.4.PDF.2.1'
      ], **args)
      self.title = 'Non-text content without Alt or ActualText attribute'
      self.description = """Checkpoint 1.1: Provide a text equivalent for every no n-text element (e.g., via "Alt", "ActualText", or in element content). This incl udes: images, graphical representations of text (including symbols), image map r egions, animations (e.g., animated GIFs), applets and programmatic objects, asci i art, frames, scripts, images used as list bullets, spacers, graphical buttons, sounds (played with or without user interaction), stand-alone audio files, audi o tracks of video, and video. [Priority 1]"""

   def result(self,s):
      return  not (int(self.aWAM("EIAO.A.10.1.1.4.PDF.1.1",s)) or 
                   int(self.aWAM("EIAO.A.10.1.1.4.PDF.2.1",s)))

AppendKlass(EGOVMON_PDF_01)
   
class EGOVMON_PDF_08(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.08 - PDF document represents a scanned image.

      History
      Initial version
      Tingtun
      2009-12-31

      WCAG 1.0 reference: Checkpoint 3.1: When an appropriate markup language exists, use markup rather than images to convey information [Priority 2].

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.08",[
          'EIAO.A.10.3.1.4.PDF.1.1'
      ], **args)
      self.title = 'PDF document represents a scanned image.'
      self.description = """Checkpoint 3.1: When an appropriate markup language exists, use markup rather than images to convey information [Priority 2]."""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.3.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_08)

class EGOVMON_PDF_09(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.09 - PDF document contains columns or other side-by-side text content
      such as tables.

      History
      Initial version
      Tingtun
      2010-04-21

      WCAG 1.0 reference: Checkpoint 10.3: Until user agents (including assistive technologies) render side-by-side text correctly, provide a linear text alternative (on the current page or some other) for all tables that lay out text in parallel, word-wrapped columns. [Priority 3]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.09",[
          'EIAO.A.10.10.3.4.PDF.1.1'
      ], **args)
      self.title = 'PDF document contains columns or other side-by-side text content such as tables'
      self.description = """ Checkpoint 10.3: Until user agents (including assistive technologies) render side-by-side text correctly, provide a linear text alternative (on the current page or some other) for all tables that lay out text in parallel, word-wrapped columns. [Priority 3]"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.10.3.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_09)

class EGOVMON_PDF_03(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.03 - PDF document does not contain structure elements.

      History
      Initial version
      UIA
      2008-10-07

      WCAG 1.0 reference: Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.03",[
          'EIAO.A.10.3.2.4.PDF.1.1'
      ], **args)
      self.title = 'PDF document does not contain structure elements.'
      self.description = """Checkpoint 3.2: Create documents that validate to published formal grammars. [Priority 2]"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.3.2.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_03)

class EGOVMON_PDF_04(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.04 - PDF document does not specify natural language.

      History
      Initial version
      UIA
      2008-10-07

      WCAG 1.0 reference: Checkpoint 4.1: Clearly identify changes in the natural language of a document's text and any text equivalents (e.g., captions). 
[Priority 1]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.04",[
          'EIAO.A.10.4.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document does not specify natural language for the document.'
      self.description = """Checkpoint 4.1: Clearly identify changes in the natural language of a document's text and any text equivalents (e.g., captions).
[Priority 1]"""

   def result(self,s):
      return 1-int(self.aWAM("EIAO.A.10.4.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_04)

class EGOVMON_PDF_05(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.05 - PDF document does not allow assistive technologies access to extract content.

      History
      Initial version
      UIA
      2008-10-07

      WCAG 1.0 reference: Checkpoint 8.1 Make programmatic elements such as scripts and applets directly accessible or compatible with assistive technologies [Priority 1 if functionality is important and not presented elsewhere, otherwise Priority 2.]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.05",[
          'EIAO.A.10.8.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document does not allow assistive technologies access to extract content.'
      self.description = """Checkpoint 8.1 Make programmatic elements such as scripts and applets directly accessible or compatible with assistive technologies [Priority 1 if functionality is important and not presented elsewhere, otherwise Priority 2.]"""

   def result(self,s):
      return  not int(self.aWAM("EIAO.A.10.8.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_05)

class EGOVMON_PDF_07(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.07 - PDF document uses headers inconsistently, against proper document structure.

      History
      Initial version
      Tingtun
      2010-05-15

      WCAG 1.0 reference: Checkpoint 3.5: Use header elements to convey document structure and use
      them according to specification. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.07",[
          'EIAO.A.10.3.5.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document uses document headers inconsistently.'
      self.description = """Checkpoint 3.5: Use header elements to convey document structure and use them according to specification. [Priority 2]"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.3.5.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_07)

class EGOVMON_PDF_06(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.06 - PDF document doesn't have bookmarks
      
      History
      Initial version
      Tingtun
      2010-07-24

      WCAG 1.0 reference: Checkpoint 13.3 Provide information about the general layout of a site (e.g., a site map or table of contents). (Closest match)
      WCAG 2.0 reference: Checkpoint 2.4.6 (Closest match)
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.06",[
          'EIAO.A.10.13.3.4.PDF.1.1'
      ], **args)
      self.title = "The inspected PDF document doesn't have bookmarks for easy navigation"
      self.description = """Checkpoint 13.3: Provide information about the general layout of a site (e.g., a site map or table of contents)"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.13.3.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_06)


class EGOVMON_PDF_02(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.02 - PDF document doesn't provide a title

      History
      Initial version
      Tingtun
      2010-05-22

      WCAG 1.0 reference: No direct WCAG 1.0 reference
      WCAG 2.0 reference: Checkpoint 2.4.2
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.02",[
          'EIAO.A.15.1.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document does not provide a title'
      self.description = """EIAO checkpoint 15.1: Provide a document title which describes the topic or purpose of the document"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.15.1.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_02)

class EGOVMON_PDF_10(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.10 - PDF document contains a form object which is not accessible
      
      History
      Initial version
      Tingtun
      2010-05-22

      WCAG 1.0 reference: No direct WCAG 1.0 reference
      WCAG 2.0 reference: Checkpoint 4.1.2
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.10",[
          'EIAO.A.15.2.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document contains a form object which is not accessible'
      self.description = """EIAO checkpoint 15.2: Interactive form objects render a PDF document inaccessible. If a form object is embedded in a PDF document, make sure that it provides a textual representation for every input field which can be processed by accessibility technologies such as screen readers """

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.15.2.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_10)

class EGOVMON_PDF_11(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.11 - PDF document contains embedded multimedia
      
      History
      Initial version
      Tingtun
      2010-05-22

      WCAG 1.0 reference: No direct WCAG 1.0 reference
      WCAG 2.0 reference: No direct WCAG 2.0 reference 
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.11",[
          'EIAO.A.15.3.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document contains embedded multimedia files or attachments'
      self.description = """EIAO checkpoint 15.3: PDF documents containing embedded multimedia files or attachments are very difficult to process by accessibile technologies. Since embedding a multmedia file or attachment overwhelms the text content with binary content, the PDF document becomes very inaccessible """

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.15.3.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_11)

class EGOVMON_PDF_11(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.11 - PDF document uses an obsolete, inaccessible encoding
      
      History
      Initial version
      Tingtun
      2010-05-22

      WCAG 1.0 reference: No direct WCAG 1.0 reference
      WCAG 2.0 reference: No direct WCAG 2.0 reference 
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.11",[
          'EIAO.A.15.4.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document uses obsolete or inaccessible encoding'
      self.description = """EIAO checkpoint 15.4: Wherever possible images or other content embedded in PDF documents should try and use open/accessible encoding techniques. Use of an obsolete, closed and less accessibl encoding such as LZW encoding for images is not preferred"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.15.4.1.4.PDF.1.1",s))

AppendKlass(EGOVMON_PDF_11)

