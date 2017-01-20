# -- coding: utf-8

#      Copyright 2008-2012 eGovMon
#      This program is distributed under the terms of the GNU General
#      Public License.
#
#  This file is part of the eGovernment Monitoring
#  (eGovMon)
#
#  eGovMon is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  eGovMon is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with eGovMon; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
#  MA 02110-1301 USA

"""Benchmark time taken for PDF-WAM SOAP end-points to return data """

import bench
import suds
import SOAPpy
import sys

__author__ = "Anand B Pillai"
__maintainer__ = "Anand B Pillai"
__version__ = "0.1"

# URLs that can be used
# http://unpan1.un.org/intradoc/groups/public/documents/un/unpan048065.pdf for large PDF
# http://www.arendal.kommune.no/Documents/Skjemaoversikt/Hjemmelserkaering_arv_skifte_uskifte.pdf
# for medium file

def benchmark_wam1(url):
    """ Benchmark PDF WAM implementation 1 for the time
    it takes to perform the operation """

    print "Benchmarking PDF-WAM1 (SOAPpy) using",url
    proxy = SOAPpy.SOAPProxy('http://loft2492.serverloft.com:8893','eGovMon')
    with bench.bench('getPDFContent'):
        proxy.getPDFContent(url)

    with bench.bench('checkacc'):
        proxy.checkacc(url)

def benchmark_wam2(url):
    """ Benchmark PDF WAM implementation 2 for the time
    it takes to perform the operation """

    print "Benchmarking PDF-WAM2 (tornado) using",url
    proxy = suds.client.Client('http://loft2492.serverloft.com:8894/PdfContentService?wsdl')
    with bench.bench('getPDFContent'):
        proxy.service.getPDFContent(url)

    proxy = suds.client.Client('http://loft2492.serverloft.com:8894/PdfWamService?wsdl')
    with bench.bench('checkacc'):
        print proxy.service.checkacc(url)

if __name__ == "__main__":
    if len(sys.argv)<2:
        sys.exit("Usage: %s <url> (pass -2 to test pdfwam2)" % sys.argv[0])

    url = sys.argv[1].strip()
    if "-2" in sys.argv:
        benchmark_wam2(url)
    else:
        benchmark_wam1(url)
