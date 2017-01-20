# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
# 

"""
pdfbwam_wcag.py implements BWAM classes for PDF tests based on WCAG 2.0
techniques.

All BWAM classes inherits from AbstractB, which defines the list of WAMs.
"""

__author__ = "Anand B Pillai"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

from AbstractWAM import AppendKlass, AbstractB
import re
import string

# Default pass value
DEFAULT_PASS=(0,0,0)

# Default fail value
DEFAULT_FAIL=(0,0,1)

# PDF BWAM implementation

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

class EGOVMON_PDF_12(AbstractB):
   def __init__(self,awamresult, **args):
      """
      EGOVMON.PDF.12 - PDF document uses an obsolete, inaccessible encoding
      
      History
      Initial version
      Tingtun
      2010-05-22

      WCAG 1.0 reference: No direct WCAG 1.0 reference
      WCAG 2.0 reference: No direct WCAG 2.0 reference 
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"EGOVMON.PDF.12",[
          'EIAO.A.15.4.1.4.PDF.1.1'
      ], **args)
      self.title = 'The inspected PDF document uses obsolete or inaccessible encoding'
      self.description = """EIAO checkpoint 15.4: Wherever possible images or other content embedded in PDF documents should try and use open/accessible encoding techniques. Use of an obsolete, closed and less accessibl encoding such as LZW encoding for images is not preferred"""

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.15.4.1.4.PDF.1.1",s))

class WCAG_PDF_01(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.01 - Non-text content without Alt or ActualText attribute

      History
      Initial version
      Tingtun
      2011-11-27

      WCAG 1.0 reference: Checkpoint 1.1: Provide a text equivalent for every non-text element (e.g., via "Alt", "ActualText", or in element content). This includes: images, graphical representations of text (including symbols), image map regions, animations (e.g., animated GIFs), applets and programmatic objects, ascii art, frames, scripts, images used as list bullets, spacers, graphical buttons, sounds (played with or without user interaction), stand-alone audio files, audio tracks of video, and video. [Priority 1]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.01",[
          'EIAO.A.10.1.1.4.PDF.1.1','EIAO.A.10.1.1.4.PDF.2.1'
      ], **args)
      self.title = 'Applying text alternatives to images with the Alt entry in PDF documents'
      self.description = """The objective of this technique is to provide text alternatives for images via an /Alt entry in the property list for a Tag. This is normally accomplished using a tool for authoring PDF.

PDF documents may be enhanced by providing alternative descriptions for images, formulas, and other items that do not translate naturally into text. In fact, such text alternatives are required for accessibility: alternate descriptions are human-readable text that can be vocalized by text-to-speech technology for the benefit of users with vision disabilities.

When an image contains words that are important to understanding the content, the text alternative should include those words. This will allow the alternative to accurately represent the image. Note that it does not necessarily describe the visual characteristics of the image itself but must convey the same meaning as the image. """

   def result(self,s):
      return  not (int(self.aWAM("EIAO.A.10.1.1.4.PDF.1.1",s)) or 
                   int(self.aWAM("EIAO.A.10.1.1.4.PDF.2.1",s)))

class WCAG_PDF_03(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.03 - Correct tab and reading-order 

      History
      Initial version
      Tingtun
      2012-08-27

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.03",[
          'EGOVMON.A.WCAG.PDF.03'
      ], **args)
      self.title = 'Correct tab and reading order in PDF documents'
      self.description = """
      The intent of this technique is to ensure that users can navigate through content in a logical order that is consistent with the meaning of the content. Correct tab and reading order is typically accomplished using a tool for authoring PDF.

      For sighted users, the logical order of PDF content is also the visual order on the screen. For keyboard and assistive technology users, the tab order through content, including interactive elements (form fields and links), determines the order in which these users can navigate the content. The tab order must reflect the logical order of the document.

      Logical structure is created when a document is saved as tagged PDF. The reading order of a PDF document is the tag order of document elements, including interactive elements.

      If the reading order is not correct, keyboard and assistive technology users may not be able to understand the content. For example, some documents use multiple columns, and the reading order is clear visually to sighted users as flowing from the top to the bottom of the first column, then to the top of the next column. But if the document is not properly tagged, a screen reader may read the document from top to bottom, across both columns, interpreting them as one column. 
      """

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.03",s))      

class WCAG_PDF_16(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.16 - PDF document does not specify natural language.

      History
      Initial version
      Tingtun
      2011-11-27

      WCAG 1.0 reference: Checkpoint 4.1: Clearly identify changes in the natural language of a document's text and any text equivalents (e.g., captions). 
[Priority 1]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.16",[
          'EIAO.A.10.4.1.4.PDF.1.1'
      ], **args)
      self.title = 'Setting the default language using the /Lang entry in the document catalog of a PDF document'
      self.description = """The objective of this technique is to specify a document's default language by setting the /Lang entry in the document catalog. This is normally accomplished using a tool for authoring PDF.

Both assistive technologies and conventional user agents can render text more accurately when the language of the document is identified. Screen readers can load the correct pronunciation rules. Visual browsers can display characters and scripts correctly. Media players can show captions correctly. As a result, users with disabilities are better able to understand the content."""

   def result(self,s):
      return 1-int(self.aWAM("EIAO.A.10.4.1.4.PDF.1.1",s))


class WCAG_PDF_09(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.09 - PDF document uses headers inconsistently, against proper document structure.

      History
      Initial version
      Tingtun
      2011-11-27

      WCAG 1.0 reference: Checkpoint 3.5: Use header elements to convey document structure and use
      them according to specification. [Priority 2]

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.09",[
          'EIAO.A.10.3.5.4.PDF.1.1'
      ], **args)
      self.title = 'Providing headings by marking content with heading tags in PDF documents'
      self.description = """The purpose of this technique is to show how headings in PDF documents can be marked so that they are recognized by assistive technologies. This is typically accomplished by using a tool for authoring PDF.

Heading markup can be used:

    to indicate start of main content

    to mark up section headings within the main content area

    to demarcate different navigational sections, such as top or main navigation, left or secondary navigation, and footer navigation

    to mark up images (containing text) which have the appearance of headings visually. 

In some technologies, headings are designed to convey logical hierarchy. Skipping levels in the sequence of headings may create the impression that the structure of the document has not been properly thought through or that specific headings have been chosen for their visual rendering rather than their meaning. Authors are encouraged to nest headings hierarchically.

Because headings indicate the start of important sections of content, it is possible for assistive technology users to access the list of headings and to jump directly to the appropriate heading and begin reading the content. This ability to "skim" the content through the headings and go directly to content of interest significantly speeds interaction for users who would otherwise access the content slowly."""
      
   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.3.5.4.PDF.1.1",s))

class WCAG_PDF_02(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.02 - PDF document doesn't have bookmarks
      
      History
      Initial version
      Tingtun
      2011-11-27

      WCAG 1.0 reference: Checkpoint 13.3 Provide information about the general layout of a site (e.g., a site map or table of contents). (Closest match)
      WCAG 2.0 reference: Checkpoint 2.4.6 (Closest match)
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.02",[
          'EIAO.A.10.13.3.4.PDF.1.1'
      ], **args)
      self.title = "Creating bookmarks in PDF documents"
      self.description = """The intent of this technique is to make it possible for users to locate content using bookmarks (outline entries in an Outline dictionary) in long documents.

A person with cognitive disabilities may prefer a hierarchical outline that provides an overview of the document rather than reading and traversing through many pages. This is also a conventional means of navigating a document that benefits all users. """

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.10.13.3.4.PDF.1.1",s))


class WCAG_PDF_18(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.18 - PDF document doesn't provide a title

      History
      Initial version
      Tingtun
      2011-11-27

      WCAG 1.0 reference: No direct WCAG 1.0 reference
      WCAG 2.0 reference: Checkpoint 2.4.2
      
      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.18",[
          'EIAO.A.15.1.1.4.PDF.1.1'
      ], **args)
      self.title = 'Specifying the document title using the Title entry in the document information dictionary of a PDF document'
      self.description = """The intent of this technique is to show how a descriptive title for a PDF document can be specified for assistive technology by using the /Title entry in the document information dictionary and by setting the DisplayDocTitle flag to True in a viewer preferences dictionary. This is typically accomplished by using a tool for authoring PDF.

Document titles identify the current location without requiring users to read or interpret page content. User agents make the title of the page easily available to the user for identifying the page. For instance, a user agent may display the page title in the window title bar or as the name of the tab containing the page. """

   def result(self,s):
      return  1 - int(self.aWAM("EIAO.A.15.1.1.4.PDF.1.1",s))

# New WCAG 2.0 based tests
class WCAG_PDF_04(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.04 - Hiding decorative images with the Artifact tag in PDF documents

      History
      Initial version
      Tingtun
      2011-11-27

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.04",[
          'EGOVMON.A.WCAG.PDF.04'
      ], **args)
      self.title = 'Hiding decorative images with the Artifact tag in PDF documents'
      self.description = """The purpose of this technique is to show how purely decorative images in PDF documents can be marked so that they can be ignored by Assistive Technology by using the /Artifact tag. This is typically accomplished by using a tool for authoring PDF.

In PDF, artifacts are generally graphics objects or other markings that are not part of the authored content. Examples of artifacts include page header or footer information, lines or other graphics separating sections of the page, or decorative images. """

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.04",s))

class WCAG_PDF_06(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.06 - Using table elements for table markup in PDF Documents

      History
      Initial version
      Tingtun
      2011-11-27

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.06",[
          'EGOVMON.A.WCAG.PDF.06'
      ], **args)
      self.title = 'Using table elements for table markup in PDF Documents'
      self.description = """The purpose of this technique is to show how tables in PDF documents can be marked up so that they are recognized by assistive technology. This is typically accomplished by using a tool for authoring PDF.

Tabular information must be presented in a way that preserves relationships within the information even when users cannot see the table or the presentation format is changed. Information is considered tabular when logical relationships among text, numbers, images, or other data exist in two dimensions (vertical and horizontal). These relationships are represented in columns and rows, and the columns and rows must be recognizable in order for the logical relationships to be perceived. """

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.06",s))
   
class WCAG_PDF_12(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.12 - Providing name, role, value information for form fields in PDF documents

      History
      Initial version
      Tingtun
      2011-11-27

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.12",[
          'EGOVMON.A.WCAG.PDF.12'
      ], **args)
      self.title = 'Providing name, role, value information for form fields in PDF documents'
      self.description = """The objective of this technique is to ensure that assistive technologies can gather information about and interact with form controls in PDF content.

The types of PDF form controls are: text input field, check box, radio button, combo box, list box, and button.

Providing name, role, state, and value information for all form components enables compatibility with assistive technology, such as screen readers, screen magnifiers, and speech recognition software used by people with disabilities. """

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.12",s))

class WCAG_PDF_SC244(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.SC244 - Information about purpose of external link is available.

      History
      Initial version
      Tingtun
      2012-03-30

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.SC244",[
          'EGOVMON.A.WCAG.PDF.11', 'EGOVMON.A.WCAG.PDF.13'
      ], **args)
      self.title = 'Information about purpose of external link is not available.'
      self.description = """

      Check that all external links in the PDF document have their link text marked up using Link
      annotations in the document tags structure or that the document provides an alternate text
      with additional information about the link.
   
      The purpose of the external link can be recognised by assistive technology (such as screen readers)
      because the link text is marked up correctly and/or the document provides an alternate text
      for the link.
"""
   def result(self,s):
      return  not (int(self.aWAM("EGOVMON.A.WCAG.PDF.11",s)) or 
                   int(self.aWAM("EGOVMON.A.WCAG.PDF.13",s)))
   
   
class WCAG_PDF_15(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.15 - Providing submit buttons with the submit-form action in PDF forms

      History
      Initial version
      Tingtun
      2011-11-27

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.15",[
          'EGOVMON.A.WCAG.PDF.15'
      ], **args)
      self.title = 'Providing submit buttons with the submit-form action in PDF forms'
      self.description = """The objective of this technique is to provide a mechanism that allows users to explicitly request a change of context using the submit-form action in a PDF form. The intended use of a submit button is to generate an HTTP request that submits data entered in a form, so it is an appropriate control to use for causing a change of context. In PDF documents, submit buttons are normally implemented using a tool for authoring PDF. """

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.15",s))
   
class WCAG_PDF_17(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.17 - Specifying consistent page numbering for PDF documents

      History
      Initial version
      Tingtun
      2011-11-27

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.17",[
          'EGOVMON.A.WCAG.PDF.17'
      ], **args)
      self.title = 'Specifying consistent page numbering for PDF documents'
      self.description = """The objective of this technique is to help users locate themselves in a document by ensuring that the page numbering displayed in the PDF viewer page controls has the same page numbering as the document. For example, Adobe Acrobat Pro and Reader display page numbers in the Page Navigation toolbar. The page number format is specified by the /PageLabels entry in the Document Catalog.

Many documents use specific page number formats within a document. Commonly, front matter is numbered with lowercase Roman numerals. The main content, starting on the page numbered 1, may actually be the fifth or sixth page in the document. Similarly, appendices may begin with page number 1 plus a prefix of the appendix letter (e.g., "A-1").

Authors should make sure that the page numbering of their converted documents is reflected in any page number displays in their user agent. Consistency in presenting the document's page numbers will help make navigating the document more predictable and understandable."""

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.17",s))

class WCAG_PDF_14(AbstractB):
   def __init__(self,awamresult, **args):
      """
      WCAG.PDF.14 - Providing running headers and footers in PDF documents

      History
      Initial version
      Tingtun
      2012-03-20

      Mode: Fully automatable.
      """
      AbstractB.__init__(self,awamresult,"WCAG.PDF.14",[
          'EGOVMON.A.WCAG.PDF.14'
      ], **args)
      self.title = 'Providing running headers and footers in PDF documents'
      self.description = """The objective of this technique is to help users locate themselves in a document by providing running headers and footers via pagination artifacts. This is normally accomplished using a tool for authoring PDF.

Running headers and footers help make content easier to use and understandable by providing repeated information in a consistent and predictable way. The content of headers and footers will vary widely depending on the document scope and content, the audience, and design decisions. Some examples of location information that may be used in headers and footers are listed below. Whether the information appears in a header or a footer is often a design decision; page numbers often appear in footers but they may alternatively appear in headers.

    Document title

    Current chapter and/or section in the document

    Page numbers with location information such as, "Page 3-4" or "Page 9 of 15."

    Author and/or date information. 

Consistency helps users with cognitive limitations, screen-reader users and low-vision magnifier users, and users with intellectual disabilities understand content more readily.
"""

   def result(self,s):
      return  1 - int(self.aWAM("EGOVMON.A.WCAG.PDF.14",s))         

# Egovmon tests
AppendKlass(EGOVMON_PDF_08)
AppendKlass(EGOVMON_PDF_03)
AppendKlass(EGOVMON_PDF_05)

# Earlier Egovmon tests - converted
# to their WCAG 2.0 counterparts
AppendKlass(WCAG_PDF_16)
AppendKlass(WCAG_PDF_01)
AppendKlass(WCAG_PDF_09)
AppendKlass(WCAG_PDF_02)
AppendKlass(WCAG_PDF_18)

# New WCAG 2.0 techniques
AppendKlass(WCAG_PDF_04)
AppendKlass(WCAG_PDF_06)
AppendKlass(WCAG_PDF_12)
AppendKlass(WCAG_PDF_SC244)      
AppendKlass(WCAG_PDF_14)
AppendKlass(WCAG_PDF_15)
AppendKlass(WCAG_PDF_17)
AppendKlass(WCAG_PDF_03)      
