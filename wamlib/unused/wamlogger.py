# Logging class for WamServer and assoc. modules

import os, sys
import time


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


__author__ = "Anand B Pillai"
__updated__ = "$LastChangedDate$"
__version__ = "$Id: wamlogger.py Mon Jun 19 14:19:16 IST 2006 abp $"


class WAMLoggerException(Exception):
    """ Exception class for WAM logger """
    pass

class WAMLoggerFactory:
    """ Factory class for WAM logger """
    
    d = {}

    def getWamLogger(self, severity=1,logfile="wamserver.log"):
        try:
            return self.d[severity]
        except KeyError:
            logger = WAMLogger(severity,logfile)
            self.d[severity] = logger
            return logger
        
class WAMLogger:
    """ Logging class for WamServer """
    
    # Useful macros for setting
    # the log level.
    
    DISABLE = 0
    DEBUG = 1
    INFO  = 2
    WARNING = 3
    ERROR   = 4
    CRITICAL = 5

    # Severity maps to the following
    # 0 -> Shuts down logging.
    # 1 -> Logs all messages at and above the
    #      DEBUG level.
    # 2 -> Logs all messages at and above the
    #      INFO level.
    # 3 -> Logs all messages at and above the
    #      WARNING level.
    # 4 -> Logs all messages at and above the
    #      ERROR level.
    # 5 -> Logs all messages at and above the
    #      CRITICAL level.

    # Dictionary for the above mappings
    __logmap = { 0 : None,
                 1 : DEBUG,
                 2 : INFO,
                 3 : WARNING,
                 4 : ERROR,
                 5 : CRITICAL }

    # Dictionary from levels to level names
    __namemap = { 0: 'DISABLE',
                  1: 'DEBUG',
                  2: 'INFO',
                  3: 'WARNING',
                  4: 'ERROR',
                  5: 'CRITICAL' }
   
    def __init__(self, severity=1, logfile='wamserver.log'):
        """ Initialize the logger class with severity and logfile.
        The severity is 1 and logfile is 'wamserver.log' by default. """
        
        self._lvl = self.__getLogLevel(severity)
        
        if self._lvl:
            # Create file
            if os.path.isfile(logfile):
                self._f = open(logfile, 'a')
            else:
                self._f = open(logfile, 'w')

            self._f.write("\n")
            self.info("### WAM Log started ###\n")
        else:
            pass

    def __getLevelName(self, level):
       return WAMLogger.__namemap.get(level, '')
           
    def __getLogLevel(self, severity):
        return WAMLogger.__logmap.get(severity, None)

    def __getMessage(self, arg, *args):
        return ''.join((str(arg),' ',' '.join([str(item) for item in args])))

    def __getTimeStamp(self):
        return time.strftime('%b %d %Y %H:%M:%S %Z', time.localtime())
        
    def _log(self, message, severity):
        #NUM: Changed reference to __logmap and __namemap from
        # instance variable to class variable in the WAMLogger class, which 
        # might be the reason to #367. Since this was a Heisenberg bug, 
        # we just have to see if this solves the problem.
        # (It was clearly a bug that an instance variable was used here.)
        try:
            self._f.write(''.join((self.__getTimeStamp(),' ', self.__getLevelName(severity),' - ',message,'\n')))
            self._f.flush()
        except Exception, e:
            raise WAMLoggerException, str(e)

    def _trace(self, message, severity):
        sys.stderr.write(''.join((self.__getTimeStamp(),' ', self.__getLevelName(severity),' - ',message,'\n')))

    def _logntrace(self, message, severity):
        self._log(message, severity)
        #self._trace(message, severity)
        
    def debug(self, msg, *args):

        if self._lvl==1:
            self._logntrace(self.__getMessage(msg, *args), 1)

    def info(self, msg, *args):
        if self._lvl<=2:
            self._logntrace(self.__getMessage(msg, *args), 2)

    def warning(self, msg, *args):
        if self._lvl <=3:
            self._logntrace(self.__getMessage(msg, *args), 3)        

    def error(self, msg, *args):
        if self._lvl <=4:
            self._logntrace(self.__getMessage(msg, *args), 4)        

    def critical(self, msg, *args):
        if self._lvl <=5:
            self._logntrace(self.__getMessage(msg, *args), 5)        

    def shutdown(self):
        self._f.flush()
        self._f.close()

if __name__ == "__main__":
    p = 'eGovMon'
    
    mylogger = WAMLoggerFactory().getWamLogger()
    
    mylogger.debug("Test message 1",p)
    mylogger.info("Test message 2",p)
    mylogger.warning("Test message 3",p)
    mylogger.error("Test message 4",p)
    mylogger.critical("Test message 5",p)

                            
