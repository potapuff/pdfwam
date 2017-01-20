import xmlrpclib
import sys
import os

outcomes={0: 'Failed',
          1: 'Success',
          2: 'Not Applicable'
          }

def run(filename):
    proxy = xmlrpclib.ServerProxy("http://localhost:8080")
    results = eval(proxy.runAllTests(os.path.abspath(filename)))
    # print results
    
    count = 1
    for key, val in results.iteritems():
        if key.startswith('EIAO.A.') and type(val) is dict:
            try:
                result = val[(0,1)]
                if result==1:
                    print 'Test #%d: %s, result: pass' % (count, key)
                else:
                    print 'Test #%d: %s, result: fail' % (count, key)
            except KeyError:
                continue

        count+=1
                
if __name__ == "__main__":
    if len(sys.argv)<2:
        sys.exit("Usage: %s <pdf-file>\n" % sys.argv[0])
    else:
        run(sys.argv[1])
        
