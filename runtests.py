# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
# 
#

""" Unit-test suite for PDF-AWAM. Run this suite against the set of
test files and verify all tests pass before checking in any major
changes to the code """

__author__ = "Anand B Pillai"
__updated__ = "$LastChangedDate$"
__maintainer__ = "Anand B Pillai"
__version__ = "0.1"
__lastmodified__ = "Wed Apr  4 13:10:49 IST 2012"

import unittest
import pdfAWAM
import sys

class TestAllWCAGTechniques(unittest.TestCase):
    """ Run unit tests for all WCAG 2.0 techniques """

    def setUp(self):
        self.verbose = False
        sys.stdout=open('/dev/null','w')
        pass

    def openPdf(self, pdffile, process=True):
        pdf = pdfAWAM.MyPdfFileReader(open(pdffile, 'rb'), '')
        pdf.read()
        pdf.initAWAM()
        if process:
            pdf.processAWAM()
            if self.verbose: print pdf.awamHandler.resultMap
            
        return pdf

    def assertAwamKeyValue(self, result, key, value=1, pgnum=0, expectedCount=1):
        """ Assert the value of an AWAM key """

        # The key definitely has to exist
        self.assertTrue(result.has_key(key))
        entry = result[key]
        
        matches = [entryKey for entryKey, entryVal in entry.iteritems() if (entryKey[0] == pgnum) and (entryVal == value)]
        # If strict checkin is required
        if expectedCount != -1:
            self.assertEqual(len(matches), expectedCount)
        # check if item contains anything
        else:
            self.assertTrue(any(matches))

    def test_cases_WCAG_PDF_01(self):
        
        pdf = self.openPdf('testfiles/wcag.pdf.01/images-with-and-without-ALT.pdf')
        self.assertEqual(len(pdf.awamHandler.figureEls), 2)
        # No images match this, so we should have 2 failures in page #1 if everything is correct
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.1.1', 0, 1, 2)
        # One image doesn't match this in page 1, so it should be 1 failure
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.2.1', 0, 1, 1)
        # One image match this in page 1, so it should be 1 pass
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.2.1', 1, 1, 1)

        pdf = self.openPdf('testfiles/wcag.pdf.01/images-with-and-without-ALT_multipage.pdf')
        self.assertEqual(len(pdf.awamHandler.figureEls), 4)
        # Both images in both pages fail this
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.1.1', 0, 2, 2)
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.1.1', 0, 1, 2)        
        # One image in page 2 fails this
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.2.1', 0, 2, 1)
        # One image in page 2 passes this        
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.2.1', 1, 2, 1)
        # Two images in page 1 passes this                
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.1.1.4.PDF.2.1', 1, 1, 2)

    def test_cases_WCAG_PDF_02(self):
        
        pdf = self.openPdf('testfiles/wcag.pdf.02/doc_with_bookmarks.pdf')
        # This is a pass for page 0 - one occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.13.3.4.PDF.1.1')
        pdf = self.openPdf('testfiles/wcag.pdf.02/doc_without_bookmarks.pdf')
        # This is a fail for page 0 - one occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.13.3.4.PDF.1.1', 0)                

    def test_cases_WCAG_PDF_04(self):

        pdf = self.openPdf('testfiles/wcag.pdf.04/decorative-image.pdf')
        # Run test wcag 04
        pdf.runSelectedTest('WCAG.PDF.04', pdf.awamHandler.resultMap)
        self.assertEqual(pdf.getNumArtifactImgs(), 1)
        # Pass for page 1 - 1 occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 1, 1)

        pdf = self.openPdf('testfiles/wcag.pdf.04/decorative_image_multiple.pdf')
        # Run test wcag 04
        pdf.runSelectedTest('WCAG.PDF.04', pdf.awamHandler.resultMap)
        self.assertEqual(pdf.getNumArtifactImgs(), 8)
        # Pass for pages 9, 11, 12, 14, 22, 32 and 33
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 9, 1)
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 11, 1)
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 12, 1)
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 14, 1) 
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 22, 1)
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 32, 1)
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.04', 1, 33, 1)       

        pdf = self.openPdf('testfiles/wcag.pdf.04/no_decorative_image.pdf')
        # Run test wcag 04
        pdf.runSelectedTest('WCAG.PDF.04', pdf.awamHandler.resultMap)
        self.assertEqual(pdf.getNumArtifactImgs(), 0)        
        # Since this document has no artifact images, this key won't exist
        self.assertFalse(pdf.awamHandler.resultMap.has_key('EGOVMON.A.WCAG.PDF.04'))

    def test_cases_WCAG_PDF_06(self):

        pdf = self.openPdf('testfiles/wcag.pdf.06/single_table_tagged.pdf')
        # Run test wcag 06
        pdf.runSelectedTest('WCAG.PDF.06', pdf.awamHandler.resultMap)
        self.assertEqual(pdf.getNumTables(), 1)
        # Pass for page 1 - 1 occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.06', 1, 1, 1)        

        pdf = self.openPdf('testfiles/wcag.pdf.06/many_tables_tagged.pdf')
        # Run test wcag 06
        pdf.runSelectedTest('WCAG.PDF.06', pdf.awamHandler.resultMap)
        self.assertEqual(pdf.getNumTables(), 59)

        # Tables in page numbers 1...110
        pgnums = (1, 3, 11, 12, 13, 24, 27, 27, 30, 30, 40, 40, 42, 43, 44, 44, 47, 47, 49, 49, 50, 56, 58, 59, 60, 64, 66, 69, 71, 74, 75, 78, 79, 82, 82, 83, 84, 85, 86, 86, 87, 87, 87, 88, 88, 88, 88, 89, 89, 100, 101, 103, 103, 106, 108, 109, 109, 110, 110)
        for pg in pgnums:
            self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.06', 1, pg, -1)

        # Fail test case - this PDF has tables but no structure tree,
        # hence tables are not reported.
        pdf = self.openPdf('testfiles/wcag.pdf.06/single_table_untagged.pdf')
        # Run test wcag 06
        pdf.runSelectedTest('WCAG.PDF.06', pdf.awamHandler.resultMap)
        self.assertEqual(pdf.getNumTables(), 0)
        # Since this document has notables, this key won't exist
        self.assertFalse(pdf.awamHandler.resultMap.has_key('EGOVMON.A.WCAG.PDF.06'))

    def test_cases_WCAG_PDF_09(self):

        pdf = self.openPdf('testfiles/wcag.pdf.09/single_page_header_pass.pdf')
        # This is a pass for page 0 - one occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.3.5.4.PDF.1.1')

        # This doesn't have tags so header key itself should not be present
        # that is a non-applicable test.
        pdf = self.openPdf('testfiles/wcag.pdf.09/header_fail_no_tag.pdf')
        self.assertFalse(pdf.awamHandler.resultMap.has_key('EIAO.A.10.3.5.4.PDF.1.1'))

        # This is an actual fail in pg # 1
        pdf = self.openPdf('testfiles/wcag.pdf.09/single_page_header_fail.pdf')
        # This is a fail for page 1 - one occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.3.5.4.PDF.1.1', 0, 1)        

        # This is an actual fail in pg # 8
        pdf = self.openPdf('testfiles/wcag.pdf.09/multiple_pages_header_fail.pdf')
        # This is a fail for page 8 - one occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.3.5.4.PDF.1.1', 0, 8)        

    def test_cases_WCAG_PDF_11(self):

        pdf = self.openPdf('testfiles/wcag.pdf.11/single_link_pass.pdf')        
        # Run test wcag 11
        pdf.runSelectedTest('WCAG.PDF.11.13', pdf.awamHandler.resultMap)        
        # This is a pass for page 1 - one occurence
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.11', 1, 1)

        pdf = self.openPdf('testfiles/wcag.pdf.11/multiple_links_pass.pdf')        
        # Run test wcag 11
        pdf.runSelectedTest('WCAG.PDF.11.13', pdf.awamHandler.resultMap)        

        # This is a full pass test
        pgpasses = [(7, 1), (8, 2), (9, 4), (10, 2), (18, 2), (21, 3), (45, 3), (54, 4), (55, 8), (56, 14)]
        
        for pg,cnt in pgpasses:
            self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.11', 1, pg, cnt)

    def test_cases_WCAG_PDF_12(self):

        pdf = self.openPdf('testfiles/wcag.pdf.12/test_pass.pdf')        
        # Run test wcag 12
        pdf.runSelectedTest('WCAG.PDF.12', pdf.awamHandler.resultMap)                
        # This is a pass
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.12')

        pdf = self.openPdf('testfiles/wcag.pdf.12/test_fail.pdf')        
        # Run test wcag 12
        pdf.runSelectedTest('WCAG.PDF.12', pdf.awamHandler.resultMap)                
        # This is a fail
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.12', 0)        

    
    def test_cases_WCAG_PDF_13(self):

        # All the links in this document fail for this test actually
        pdf = self.openPdf('testfiles/wcag.pdf.13/multiple_links_pass_fail.pdf')        
        # Run test wcag 13
        pdf.runSelectedTest('WCAG.PDF.11.13', pdf.awamHandler.resultMap)        
        pgfails = ((7, 1), (8, 2), (9, 4), (10, 2), (18, 2), (21, 3), (45, 3), (54, 4), (55, 8), (56, 14))
        for pg, cnt in pgfails:
            self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.13', 0, pg, cnt)

        # No links pass - so this test should pass
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.13', 1, 0, 0)            

        pdf = self.openPdf('testfiles/wcag.pdf.13/multiple_links_fail.pdf')        
        # Run test wcag 13
        pdf.runSelectedTest('WCAG.PDF.11.13', pdf.awamHandler.resultMap)
        
        pgfails = ((1, 2), (2, 1))
        for pg, cnt in pgfails:
            self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.13', 0, pg, cnt)

        # No links pass - so this test should pass 
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.13', 1, 0, 0)            

    def test_cases_WCAG_PDF_14(self):

        pdf = self.openPdf('testfiles/wcag.pdf.14/header_footer_pass.pdf')        
        # Run test wcag 14
        pdf.runSelectedTest('WCAG.PDF.14', pdf.awamHandler.resultMap)
        pgpass = (2,3,4,5)
        for pg in pgpass:
            self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.14', 1, pg, -1)

        pdf = self.openPdf('testfiles/wcag.pdf.14/no_header_footer.pdf')        
        # Run test wcag 14
        pdf.runSelectedTest('WCAG.PDF.14', pdf.awamHandler.resultMap)
        # This is a failure since the document has no header/footer
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.14', 0)

        # This is a document having header footer created in OOo. However it
        # doesn't have the structures as defined by this test in PDF WCAG 2.0
        # so it fails. Once the test is modified to consider files like this
        # also, this should be a pass. Right now hence this is a false negative.
        
        pdf = self.openPdf('testfiles/wcag.pdf.14/header_footer_false_negative.pdf')        
        # Run test wcag 14
        pdf.runSelectedTest('WCAG.PDF.14', pdf.awamHandler.resultMap)
        # This is a failure since the document has no header/footer
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.14', 0)        

    def test_cases_WCAG_PDF_15(self):

        # All are pass cases since it is very difficult to find PDFs with
        # submit forms and even among them to find PDFs with submit forms
        # that actuall fail in their submit buttons.
        pdf = self.openPdf('testfiles/wcag.pdf.15/form_complete.pdf')        
        # Run test wcag 15
        pdf.runSelectedTest('WCAG.PDF.15', pdf.awamHandler.resultMap)                
        # This is a pass
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.15')

        pdf = self.openPdf('testfiles/wcag.pdf.15/submit-button-js.pdf')        
        # Run test wcag 15
        pdf.runSelectedTest('WCAG.PDF.15', pdf.awamHandler.resultMap)                
        # This is a pass
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.15')        

        pdf = self.openPdf('testfiles/wcag.pdf.15/Einladung_10_Jahre_end.pdf')        
        # Run test wcag 15
        pdf.runSelectedTest('WCAG.PDF.15', pdf.awamHandler.resultMap)                
        # This is a pass
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.15')        
        pass

    def test_cases_WCAG_PDF_16(self):
        
        # Document specifying language in tags
        pdf = self.openPdf('testfiles/wcag.pdf.16/lang_has_tags_pass.pdf')
        # This is a pass - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.4.1.4.PDF.1.1')
        # Assert lang value
        self.assertEqual(pdf.awamHandler.resultMap['EIAO.A.0.0.0.0.4.PDF.4.1'], u'en-US')

        # Document without tags specifying language
        pdf = self.openPdf('testfiles/wcag.pdf.16/lang_no_tags_pass.pdf')
        # This is a pass - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.4.1.4.PDF.1.1')
        # Assert lang value
        self.assertEqual(pdf.awamHandler.resultMap['EIAO.A.0.0.0.0.4.PDF.4.1'], u'en-US')

        # Fail case - Document without tags not specifying language
        pdf = self.openPdf('testfiles/wcag.pdf.16/lang_no_tags_fail.pdf')
        # This is a fail 
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.4.1.4.PDF.1.1', 0)

    def test_cases_WCAG_PDF_17(self):

        pdf = self.openPdf('testfiles/wcag.pdf.17/page_numbers_pass.pdf')
        # Run test wcag 17
        pdf.runSelectedTest('WCAG.PDF.17', pdf.awamHandler.resultMap)        
        # This is a pass - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.17')

        pdf = self.openPdf('testfiles/wcag.pdf.17/page_numbers_pass2.pdf')
        # Run test wcag 17
        pdf.runSelectedTest('WCAG.PDF.17', pdf.awamHandler.resultMap)                
        # This is a pass - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EGOVMON.A.WCAG.PDF.17')        

        pdf = self.openPdf('testfiles/wcag.pdf.17/page_labels_not_applicable.pdf')
        # Run test wcag 17
        pdf.runSelectedTest('WCAG.PDF.17', pdf.awamHandler.resultMap)
        # Test not applicable - key shouldn't exist
        self.assertFalse(pdf.awamHandler.resultMap.has_key('EGOVMON.A.WCAG.PDF.17'))        

    def test_cases_WCAG_PDF_18(self):

        pdf = self.openPdf('testfiles/wcag.pdf.18/title_pass.pdf')
        # This is a pass - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.15.1.1.4.PDF.1.1')
        pdf = self.openPdf('testfiles/wcag.pdf.18/title_fail.pdf')
        # This is a fail - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.15.1.1.4.PDF.1.1', 0)

    def test_cases_EGOVMON_PDF_08(self):        

        pdf = self.openPdf('testfiles/egovmon.pdf.08/scanned_producer.pdf')
        # This is a fail for scanned test  - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.3.1.4.PDF.1.1', 0)

        pdf = self.openPdf('testfiles/egovmon.pdf.08/scanned_other.pdf')
        # This is a fail for scanned test  - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.3.1.4.PDF.1.1', 0)

        # Appears like a scanned document, but it is not and our
        # checker detects it well.
        pdf = self.openPdf('testfiles/egovmon.pdf.08/not_scanned.pdf')
        # This is a pass for scanned test  - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.3.1.4.PDF.1.1')

    def test_cases_EGOVMON_PDF_05(self):        

        pdf = self.openPdf('testfiles/egovmon.pdf.05/failure1.pdf')
        # This is a fail for encryption test  - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.8.1.4.PDF.1.1', 0)

        pdf = self.openPdf('testfiles/egovmon.pdf.05/failure2.pdf')
        # This is a fail for encryption test  - 0 page, 1 instance
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.8.1.4.PDF.1.1', 0)

        pdf = self.openPdf('testfiles/egovmon.pdf.05/encrypted_but_pass.pdf')
        # This is a pass - though encrypted the permissions allow content accessibility
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.8.1.4.PDF.1.1')

        pdf = self.openPdf('testfiles/egovmon.pdf.05/encrypted_but_pass2.pdf')
        # This is a pass - though encrypted the permissions allow content accessibility
        self.assertAwamKeyValue(pdf.awamHandler.resultMap, 'EIAO.A.10.8.1.4.PDF.1.1')                        


        
        
if __name__ == '__main__':
    unittest.main()


