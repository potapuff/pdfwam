# -- coding: utf-8
# 
# Copyright (C) Tingtun AS 2013.
#

__author__ = "Anand B. Pillai"
__updated__ = "$LastChangedDate$"
__version__ = "2.0"

""" A PDF accessibility checking WAM.

Creation: Anand B Pillai <abpillai at gmail dot com> April 27 2007

Modification History

Anand April 27 07   Added more exception handling. Fixed a
                    problem in pyPdf which was not reading
                    certain encrypted PDF docs.
Anand May 24 2009   Added method to determine scanned PDF.
                    Added method to determine # of Images.

"""


from pyPdf import PdfFileReader
from pyPdf.utils import PdfReadError
from pdfAWAMHandler import PdfAWAMHandler
from pdfStructureMixin import PdfStructureMixin
from errors import DecryptionFailedException, PdfInitException, PdfWamProcessingError

import pdfwcag

# For logging
import logger as loggermodule
import config

import sys 
import time
import cStringIO
import traceback

# The main pdf-wam class containing most of the checking logic
pdfklass = pdfwcag.PdfWCAG

__author__ = "Anand B Pillai"
__maintainer__ = "Anand B Pillai"
__version__ = "2.0"

class MyPdfFileReader(PdfFileReader, pdfklass):
    """ Our own customized Pdf file reader class
    which inherits from the pyPdf one """
    
    def __init__(self, stream, password='', logger=None):
        pdfklass.__init__(self)
        self.flattenedPages = None
        self.resolvedObjects = {}
        # In pdf.py the read happens before the following
        # 2 initializations. But we need to switch the order.
        self.stream = stream
        self._override_encryption = False
        self.passwd = password
        # If logger is not passed, make one
        if logger==None:
            logger =  loggermodule.getLogger('pdfwam', config.pdfwamlogfile, level=config.pdfwamloglevel)
        self.setLogger(logger)

    def read(self):
        """ Function which overrides 'read' of PdfFileReader class """

        # PdfFileReader.read2(self, stream)
        PdfFileReader.read(self, self.stream)
        PdfStructureMixin.read(self, self.stream)
        # Decrypt automatically with password
        if self.getIsEncrypted():
            self.logger.info('Document is encrypted. Trying to decrypt')
            ret = self.decrypt(self.passwd)
            if ret:
                self.logger.info('Document decryption success.')
            else:
                self.logger.error('Document decryption failed.')
                raise DecryptionFailedException

        # Fill in document information
        self.fillInfo()
        # Set the root object
        self.root =  self.trailer['/Root'].getObject()
    
def extractAWAMIndicators(pdf,
                          password='',
                          verbose=True,
                          report=False,
                          developer=False,
                          console=False,
                          logger=None):
    """ Check whether the given PDF document is accessible """

    t = time.time()

    if logger == None:
        logger = loggermodule.getLogger('pdfwam', config.pdfwamlogfile, level=config.pdfwamloglevel)
        logger.setConsole(console)
    
    # Takes an optional password which can be used to
    # unlock the document for encrypted documents.
    try:
        pdfobj = MyPdfFileReader(pdf, password, logger)
        pdfobj.verbose = verbose
        
        pdfobj.read()
        pdfobj.fixIndirectObjectXref()

        # If developer, just print a dictionary containing
        # meta info, scanned, forms, tagged, permissions
        # and an accessibility score.
        if developer:
            pdfobj.initAWAM()
            pdfobj.processAWAM()            
            devdict = { 'title': pdfobj.title,
                        'creator': pdfobj.creator,
                        'producer': pdfobj.producer,
                        'author': pdfobj.author,
                        'subject': pdfobj.subject,
                        'created': pdfobj.ctime,
                        'scanned': pdfobj.isScanned,
                        'tagged': (pdfobj.structTree != None),
                        'form': pdfobj.hasValidForms(),
                        'permissions': pdfobj.awamHandler.resultMap['EIAO.A.10.8.1.4.PDF.1.1'].get((0,1),0),
                        'lang': pdfobj.awamHandler.resultMap.get('EIAO.A.0.0.0.0.4.PDF.4.1',''),
                        'numpages': pdfobj.numPages
                        }
            
            return devdict
        
        if verbose:
            # NOTE - These are supposed to be printed to STDOUT
            # so don't wrap them in logging !
            
            print "***PDF Summary: Start***"
            print 'Version:',pdfobj.version
            print '#Pages:',pdfobj.numPages
            print 'Producer:',pdfobj.producer
            print 'Creator:',pdfobj.creator
            if pdfobj.title:
                print 'Title=>',pdfobj.title
            else:
                print 'Title: (None)'

            print 'Has structure tree:',(pdfobj.structTree != None)
            has_forms = pdfobj.hasForms()
            print 'Has forms:',has_forms
            print 'Has bookmarks:',pdfobj.hasBookmarks()
            print 'Scanned:',pdfobj.isScanned
            print 'Num Images:',pdfobj.getNumImages()

            print '***PDF Summary: End ****\n'

        pdfobj.runAllTests()
    except DecryptionFailedException:
        # We are unable to decrypt document.
        # We have got no parsed pdfobj, and cannot do much more,
        # unfortunately... 
        # Tell that the document was not accessible due to encryption, at least
        errmsg="Document Decryption failed"
        logger.error(errmsg)
        # Ticket 127 fix
        # return {}
        raise PdfWamProcessingError, errmsg
    except NotImplementedError:
        # pyPdf only supports algorithm version 1 and 2. 
        # Version 3 and 4 are not yet supported.
        errmsg="Unsupported decryption algorithm."
        logger.error(errmsg)
        # Ticket 127 fix        
        raise PdfWamProcessingError, errmsg 
    except PdfReadError, e:
        errmsg='Error, cannot read PDF file: ' + str(e)
        logger.error(errmsg)
        # Not a PDF file
        # return {}
        raise PdfWamProcessingError, errmsg
    except Exception, e:
        # Final global catch-all handler
        # Prepare error message
        message = "%s : %s" % (e.__class__.__name__, str(e))

        # Save traceback
        capture = cStringIO.StringIO()
        traceback.print_exc(file=capture)
        logger.error(message)
        logger.error("Traceback")
        logger.error(capture.getvalue())

        raise PdfWamProcessingError, "Unguarded error => [" + message + " ] <=. Please send feedback to developers."
    
    ## except PdfInitException, e:
    ##     errmsg = str(e)
    ##     logger.error(errmsg)
    ##     # return {}
    ##     raise PdfWamProcessingError, errmsg 
    
    logger.info('Processed in %.2f seconds' % (time.time() - t))
    rmap = pdfobj.awamHandler.resultMap
    logger.debug('\n***AWAM Dictionary***')
    logger.debug(rmap)

    if verbose:
        for id in rmap.keys():
            value = rmap[id]
            if type(value) is dict:
                for location in value.keys():
                    print 'AWAM-ID:',id,' location:',location,' value:',value[location]
            else:
                print 'AWAM-ID:',id,'value:',value
            
    if report:
        pdfobj.print_report()

    return rmap
        

    

