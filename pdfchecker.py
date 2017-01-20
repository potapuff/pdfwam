#! /usr/bin/env python

# -- coding: utf-8
#
# Copyright (C) Tingtun AS 2013.
# 


""" Command-line PDF accessibility checker using PDF-WAM """

__author__ = "Anand B Pillai"
__maintainer__ = "Anand B Pillai"
__version__ = "0.1"
__updated__ = "$LastChangedDate$"

import pdfAWAM
import sys, os
import optparse
import time
import config
import requests
import cStringIO

USAGE="""%s [options] pdffile - Check PDF documents for accessibility"""

def checkAcc(pdffile_or_url, passwd='', verbose=True, report=False, developer=False, loglevel='info'):

    config.pdfwamloglevel = loglevel

    if pdffile_or_url.startswith('http://') or pdffile_or_url.startswith('https://'):
        data = requests.get(pdffile_or_url).content
        stream = cStringIO.StringIO(data)
    else:
        stream = open(pdffile_or_url, 'rb')
        
    ret = pdfAWAM.extractAWAMIndicators(stream, passwd, verbose, report, developer, console=True)
    if developer:
        print ret

def setupOptions():
    if len(sys.argv)==1:
        sys.argv.append('-h')
        
    o = optparse.OptionParser(usage=USAGE % sys.argv[0] )
    o.add_option('-p','--password',
                 dest='password',help='Optional password for encrypted PDF',default='')
    o.add_option('-q','--quiet',
                 dest='quiet',help="Be quiet, won't print debug/informational messages",action="store_true",
                 default=False)
    o.add_option('-d','--developer',
                 dest='developer',help="Print a dictionary of information for the developer (please note that this turns off reporting and debug messages automatically)",action="store_true",
                 default=False)    
    o.add_option('-r','--report',
                 dest='report',help="Print a report of test results at the end",action="store_true",
                 default=False)
    o.add_option('-l','--loglevel',
                 dest='loglevel',help="Set logging level (default: info)",
                 default='info')

    options, args = o.parse_args()
    return (args[0], options.__dict__)

def main():
    pdffile, options = setupOptions()

    password = options.get('password','')
    quiet = options.get('quiet')
    report = options.get('report')
    developer = options.get('developer')
    loglevel = options.get('loglevel','info')

    if developer:
        print 'Developer option turned on, reporting and messages will be disabled.'
        
    verbose = (not quiet)
    checkAcc(pdffile, password, verbose, report, developer, loglevel)

if __name__ == "__main__":
    main()
