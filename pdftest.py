# Perform a call to the PDF WAM server

#      Copyright 2008-2010 eGovMon
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


import sys
import SOAPpy

__author__ = "Nils Ulltveit-Moe"
__maintainer__ = "Nils Ulltveit-Moe, Anand B Pillai"
__version__ = "$Id: wam_container.py 1974 2006-04-24 18:35:47Z num $"
__modified__ = 'Thu Jun  8 12:37:05 IST 2006'
__updated__ = "$LastChangedDate$"

def test_check(server, url, ipaddress='10.10.10.10',useragent='PDF_Checker_Test_Client',
               referrer='http://www.tingtun.no',forwarded_for=None):
   return server.checkacc(url, referrer, ipaddress, forwarded_for, useragent)

def test_getPDFContent(server, url):
   return server.getPDFContent(url)

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Use: %s <PDF URL> [option method name] (check/get) " % sys.argv[0]
      sys.exit(1)

   method='check'
   if len(sys.argv)>=3:
      method = sys.argv[2]
      
   # server = SOAPpy.SOAPProxy("http://tt2.s.tingtun.no:8893",'eGovMon')
   server = SOAPpy.SOAPProxy("http://localhost:8893", namespace='eGovMon')
   url = sys.argv[1]
   
   # Use URLlibs own url, which might have been redirected...
   if method=='check':
      result=test_check(server, url)
   elif method=='get':
      result=test_getPDFContent(server, url)
      
   print result
   



