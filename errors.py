""" PDF-WAM custom exceptions module """


class PdfInitException(Exception):
    """ Errors initializing the PDF file """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class DecryptionFailedException(Exception):
    """ Errors in decrypting an encrypted PDF file """
    pass

class PdfWamProcessingError(Exception):
    """ Class summarizing all PDF-WAM processing exceptions """
    pass

