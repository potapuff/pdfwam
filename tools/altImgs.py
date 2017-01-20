"""
Find the number of images in the PDF document
which failed the alt-images test
"""

import sys
sys.path.append('..')

import optparse
import pdfAWAM
import pdfchecker
from pyPdf.utils import PdfReadError

def checkImgs(pdf, password=''):
    """ Check the PDF document for the number
    of images without Alt text """
    
    try:
        pdfobj = pdfAWAM.MyPdfFileReader(pdf, password)
        pdfobj.initAWAM()

        if (pdfobj.structroot==None) or (len(pdfobj.structroot)==0):
            print 'Error, no structure tree found!'
            return -1

        tree = pdfobj.structroot
        kids = tree['/K']

        # Search the /K kids of the structure tree root
        if type(kids) is list:
            pdfobj.search(kids)
        else:
            pdfobj.search(kids.getObject())

        failedImgs, pgs = 0, []
        
        for key, values in pdfobj.awamHandler.failedImgs.iteritems():
            failedImgs += len(values)
            pgs.append(str(key))

        if failedImgs:
            print 'Pdf file has',failedImgs,'images without Alt text in pages ' + ','.join(pgs)
        else:
            print 'Pdf file has no failed images'
            
    except pdfAWAM.DecryptionFailedException:
        # We are unable to decrypt document.
        # We have got no parsed pdfobj, and cannot do much more,
        # unfortunately... 
        # Tell that the document was not accessible due to encryption, at least
        errmsg="Document Decryption failed"
        print errmsg
    except NotImplementedError:
        # pyPdf only supports algorithm version 1 and 2. 
        # Version 3 and 4 are not yet supported.
        errmsg="Unsupported decryption algorithm."
        print errmsg
    except PdfReadError, e:
        errmsg='Error, cannot read PDF file: ' + str(e)
        print errmsg

def main():
    pdffile, password = pdfchecker.setupOptions()
    checkImgs(open(pdffile,'rb'), password)

if __name__ == "__main__":
    main()
