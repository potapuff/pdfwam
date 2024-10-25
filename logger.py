# -- coding: utf-8

""" Generic logger module which can be used by any application
for logging. Wraps up Python's logging object in a convenient
LoggerWrapper class which provides wrapper functions for logging
at various levels using variable arguments.

"""

import logging
import functools
import re
import sys

from idioms import ignore

___author__ = "Anand B Pillai"
__maintainer__ = "Anand B Pillai"
__version__ = "0.2"
__lastmodified__ = "2013-03-30 18:32:00 IST"

# List of current loggers
__loggers__ = {}

class LoggerWrapper(object):
    """ Wrapper class on logging object which provides
    convenience functions for logging at different levels """

    def __init__(self, log, console=False):
        self._log = log
        # Debug flag - if set, can be used to trace the
        # source of the caller stack frame
        self._sdebug = False
        # Overridden functions
        self._supported = ('info','warning','error','critical','debug')
        # Preceding and trailing single quptes
        self.squote_re = re.compile("^'|^u'|'$")
        # Create function wrappers for these
        for name in self._supported:
            # Creating convenient wrappers by using functools
            func = functools.partial(self._dolog, name)
            setattr(self, name, func)

        self.__console = False
        # Prepare console logging handlers
        self._prepareConsoleHandlers()
        # Add console logging if specified
        if console:
            self._addConsoleHandlers()
        self.__console = console

    def myrepr(self, string):
        return self.squote_re.sub('',repr(string))

    def _prepareConsoleHandlers(self):
        """ Prepare console (stdout/stderr) logging handlers """
        
        self.shout = logging.StreamHandler(sys.stderr)
        self.sherr = logging.StreamHandler(sys.stderr)       
        # Formatter - skip debugging for console formatter
        formatter2 = logging.Formatter('%(asctime)s :%(levelname)-8s - %(message)s',
                                       datefmt='%Y-%m-%d %H:%M:%S')
        self.shout.setFormatter(formatter2)
        self.sherr.setFormatter(formatter2)      
        # shout should filter all log records >= ERROR
        self.shout.addFilter(ReverseErrorFilter())
        # sherr should filter all log records < ERROR
        self.sherr.addFilter(ErrorFilter())

    def _addConsoleHandlers(self):
        """ Add console logging handlers to the logger """

        # If already set, do nothing
        if self.__console:
            return False
        
        self._log.addHandler(self.shout)
        self._log.addHandler(self.sherr)

    def _removeConsoleHandlers(self):
        """ Remove console logging handlers """

        if not self.__console:
            return False

        # Remove handlers
        try:
            self._log.handlers.remove(self.shout)
            self._log.handlers.remove(self.sherr)
            return True
        except ValueError:
            return False
        
    def _getMessage(self, msg, *args, **kwargs):
        """ Return message with variable arguments """

        try:
            return ' '.join([str(msg)] + map(lambda x: str(x), args))
        except (UnicodeEncodeError, UnicodeDecodeError), e:
            return ' '.join([self.myrepr(msg)] + map(lambda x: self.myrepr(x), args))           

    def _dolog(self, levelname, msg, *args, **kwargs):
        """ Generic function for logging with variable arguments """

        # Check specific keywordargs filename and function
        filename, function = kwargs.get('sourcename',''), kwargs.get('function')
        # Check for None
        filename = filename or ''
        function = function or ''
        
        filename = filename.split('/')[-1]
        
        # Remove .py from the filename
        with ignore():
            filename = filename[:filename.rindex('.')]
            
        logfunc = getattr(self._log, levelname)
        return logfunc(self._getMessage(msg, *args), extra={'sourcename':filename,'function':function})

    def logsimple(self, msg, *args):
        """ Send a log line to the log file with no formatting """

        # Save current formatting - for the time being all formatting
        # is the same so we save just the first one.
        formatter = self._log.handlers[0].formatter
        plain_formatter = logging.Formatter("%(message)s")
        for handler in self._log.handlers:
            handler.setFormatter(plain_formatter)

        # Log the message at info level
        self._log.info(self._getMessage(msg, *args))

        # Reset formatter
        for handler in self._log.handlers:
            handler.setFormatter(formatter)        
        
    # Set debug flag
    def setDebug(self, val = True):
        """ Set the debug flag which allows to trace source code
        location for log emitters """

        # Note that this has nothing to do with the log level DEBUG
        self._sdebug = val

    def getDebug(self):
        """ Return the debug flag """
        
        return self._sdebug

    def setLevel(self, level):
        """ Set the logging level for the logger """

        # Allow clients to pass in levels as strings
        if type(level) is str:
            level = eval('logging.' + level.upper())
            
        self._log.setLevel(level)
    
    def setFormat(self, format):
        """ Set format for log lines """

        for handler in self._log.handlers:
            handler.setFormatter(logging.Formatter(format))

    def setConsole(self, val=True):
        """ Toggle console logging settings """

        if val:
            self._addConsoleHandlers()
        else:
            self._removeConsoleHandlers()

        self.__console = val
    
class ErrorFilter(object):
    """ Logging filter class that filters out all
    log records at levels < ERROR """

    def filter(self, record):
        return int(record.levelno >= logging.ERROR)

class ReverseErrorFilter(object):
    """ Logging filter class that filters out all
    log records at levels >= ERROR """

    def filter(self, record):
        return int(record.levelno < logging.ERROR)

def getLogger(app, logfile, level=logging.INFO, console=False):
    """ Return a logger for the given app. Accepts a logfile
    and optional log level which defaults to INFO """

    # If a logger exists for the same app and logfile, return it
    key = (app, logfile)
    if key in __loggers__:
        return __loggers__.get(key)
    
    log = logging.getLogger(app)
    # Allow clients to pass in levels as strings
    if type(level) is str:
        level = eval('logging.' + level.upper())
        
    log.setLevel(level)
    fh = logging.FileHandler(logfile)
 
    formatter = logging.Formatter('%(asctime)s [%(sourcename)s/%(function)s]:%(levelname)-8s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
 
    # add handler to logger object
    log.addHandler(fh)
    logobject = LoggerWrapper(log, console=console)
    
    # Make entry for the logging object in the logger dictionary
    __loggers__[key] = logobject

    return logobject

def getMultiLogger(app, logfile, errlogfile, level=logging.INFO, console=False):
    """ Return a logger for the given app in such a way that normal logging (levels
    of DEBUG, INFO, WARNING gets logged to the file 'logfile' and ERROR and above gets
    logged to the 'errlogfile'. This allows more fine-grained control over logging.

    Note that if both files are same, this function behaves same as getLogger.
    """

    if logfile==errlogfile:
        return getLogger(app, logfile, level, console=console)

    # If a logger exists for the same app and logfile, return it
    key = (app, logfile, errlogfile)
    if key in __loggers__:
        return __loggers__.get(key)
    
    log = logging.getLogger(app)

    # Allow clients to pass in levels as strings
    if type(level) is str:
        level = eval('logging.' + level.upper())
        
    log.setLevel(level)

    # Create two file handlers
    fhout = logging.FileHandler(logfile)
    fherr = logging.FileHandler(errlogfile) 

    formatter = logging.Formatter('%(asctime)s [%(sourcename)s/%(function)s]:%(levelname)-8s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S') 

    fhout.setFormatter(formatter)
    fherr.setFormatter(formatter)

    # fhout should filter all log records >= ERROR
    fhout.addFilter(ReverseErrorFilter())
    # fherr should filter all log records < ERROR
    fherr.addFilter(ErrorFilter())
    
    # add handler to logger object
    log.addHandler(fhout)
    log.addHandler(fherr)

    logobject = LoggerWrapper(log, console=console)

    # Make entry for the logging object in the logger dictionary
    __loggers__[key] = logobject

    return logobject
    
if __name__ == "__main__":
    pass

