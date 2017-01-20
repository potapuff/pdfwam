import SimpleXMLRPCServer
import pdfAWAM
# import inspect
import sys
import os
import StringIO

class PdfWcagTest(object):
    """ Class for testing WCAG 2.0 PDF tests """

    def runAllTests(self, pdffile, password=''):
        self.reader = pdfAWAM.MyPdfFileReader(open(pdffile,'rb'), password)
        self.reader.fixIndirectObjectXref()
        results = self.reader.runAllTests()
        
        return str(results)

def runServer():
    """ Run as an XML-RPC server in port 8080 """
    # Create server
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8080),
                                requestHandler=SimpleXMLRPCServer.SimpleXMLRPCRequestHandler)
    server.register_introspection_functions()
    server.register_instance(PdfWcagTest())
    server.serve_forever()
                
if __name__ == "__main__":
    if len(sys.argv)>=2:
        obj = PdfWcagTest()
        print obj.runAllTests(sys.argv[1])
    else:
        runServer()
        
