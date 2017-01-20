# -- coding: utf-8
#! /usr/bin/env python
#
# Copyright (C) Tingtun AS 2013.
#

""" Abstract class for WAMs."""

# B wam (barrier composing)
# This is another way of importing that works with filenames with hyphen..
# Fixed ticket #165 - Anand 02/08/06
# Optimization for ticket #380 for WAM memory usage - Anand 28/02/07

__author__     = "Morten Goodwin, Nils Ulltveit-Moe"
__updated__ = "$LastChangedDate$"
__version__    = "2.0"

import WAM_Results

class WAMError(Exception):
    """Basic class for reporting Alternative texts errors
    """

class NotEnoughParametersSetError(WAMError):
    """Exception when not enough parameters are set
    """

    def __init__(self,parameterlist,comment):
        """Throws a NotEnoughParametersSetError exception.

        Keyword argumenst:
        parameterlist -- list of parameters
        comment -- comment
        """
        comment = comment + ','.join([str(p) for p in parameterlist])
        WAMError.__init__(self,'Not enough parameters set ' + comment)


class UnrecognisedWAM(WAMError):
    """Exception when a WAM is not recognised
    """

    def __init__(self,WAMName):
        """Throws a UnrecognisedWAM exception.

        Keyword argumenst:
        WAMName -- Name of WAM
        """
        WAMError.__init__(self,' '.join([WAMName,'is not recognisable']))


class NotImplemented(WAMError):
    """Exception when a WAM has not yet been implemented
    """
    
    def __init__(self,WAMName):
        """Throws a NotImplemented exception.
       
        Keyword argumenst:
        WAMName -- Name of WAM
        """
        WAMError.__init__(self,' '.join([WAMName,'not implemented yet']))
 
class WAMClasses:
   
   def __init__(self):
      self._l = []

   def append(self, obj):
      self._l.append(obj)

   def getKlasses(self):
      return self._l
   
d = {}
d['instance'] = WAMClasses()

def AppendKlass(klass):

   d['instance'].append(klass)
      
class WamRules:
   """
   Bind and manage WAM rules
   """
   def __init__(self,awams,ruleset,**args):
      # Each thread needs its own awam instance
      self.awams=awams
      self.wamRules=[]
      self.awamtoiterate=None
      self.ruleset=ruleset
      # Handle EIAO.EXT.1.2 vs EIAO.INT.1.2
      # (One WAM registered as EIAO.INT.1.2 performs both)
      # If needed, a more general solution for polymorph
      # wams may be added in the future.
      if "EIAO.EXT.1.2" in ruleset:
         ruleset.remove("EIAO.EXT.1.2")
         if not "EIAO.INT.1.2" in ruleset:
            ruleset.append("EIAO.INT.1.2")
      # Need to instantiate WAM classes...
      for c in d['instance'].getKlasses():
         #s=str(c).split(".")[1]
         if "ALL" in ruleset: 
            # Enable all rules
            self.wamRules.append(c(awams, **args))
         else:
            # Enable only the rules enabled in ruleset.
            rule=c(awams, **args)
            # Weird syntax with array wrapped in dict in SOAPpy...
            if rule.wamid in ruleset:
               self.wamRules.append(rule)


class AbstractWAMException(Exception):
    pass

# Abstract class for B-WAMs
# Problem: assumes 1-1 binding. Which awam to choose if several 
# are available?
# I.e. how to calculate the index "S"? How do you know
# which assertions that belongs to which elements?
# posisjon S
#09:33 <@Goodwin> annika: If I understand the s-handling correct, you want the possibility to have more than one awam-result in AbstractB.py. Currently, the awam results are bind to an object in the bwam-class, which holds the results with a line and column. However, you need the possibility to store more than on awam-result and retrieve the result based on (line,column) resulting in a structure like this {(line,column):{AWAM1:result, AWAM2:result....},(line,column):{...}}. (In addition to the existing structure)?
#09:40 < annika> Morten: yes.

class AbstractWAM:
    """
    AbstractWAM is an abstract class that provides a framework for iterating through the
    WAMs, and perform the checks on the AWAM indicators.
    """
    # WAM types
    BWAM=WAM_Results.BWAM
    LANGUAGE=WAM_Results.LANGUAGE
    INTLINK=WAM_Results.INTLINK
    EXTLINK=WAM_Results.EXTLINK
    TECHNOLOGY=WAM_Results.TECHNOLOGY
    MEDIATYPE=WAM_Results.MEDIATYPE
    VERSION=WAM_Results.VERSION
    CREATOR=WAM_Results.CREATOR
    PRODUCER=WAM_Results.PRODUCER
    # New properties
    TITLE = WAM_Results.TITLE
    AUTHOR = WAM_Results.AUTHOR
    VERSION = WAM_Results.VERSION
    CREATION_TIME = WAM_Results.CREATION_TIME
    MODIFICATION_TIME = WAM_Results.MODIFICATION_TIME
    
 
    awam=None
 
    def __init__(self,awamresult,wamid=None,awams=None,type=None,default=None,codeExtracts=0, content=""):
        self.codeExtracts = codeExtracts
        self.content=content
        self.wamid=wamid
        self.awams=awams
        self.type = type
        self.xhtml = ""
        self.title=""
        self.description=""
        self.index=0            # Generator index
        self.locations=[]       # List of locations used by this WAM
        self.awamresult=awamresult # AWAM result structure reference
        locationSet={}          # Set not supported by Jython, so useing dict keys instead
        for awamid in self.awams:
            try:
               for location in awamresult[awamid].keys():
                   locationSet[location]=1
            except KeyError:
               continue
        self.locations=locationSet.keys()
        self.locations.sort()
        # If no locations are registered, register the default location
        # This is to return a negated result for WAM tests that can only provide
        # either only a positive or negative indicator, but not both.
        # E.g. to indicate that <embed> has not been found.
        if default!=None and len(self.locations)==0:
            self.locations.append(default)

    def __iter__(self):
        """
        WAM iterator
        """
        return self

    def next(self):
        """
        Return the next WAM_Results object from the WAM iterator.
        """
        if self.index >= len(self.locations):
            self.index = 0
            raise StopIteration

        currentresult = self.locations[self.index]

        try:
            if type(self.content) == type("") and self.content != "" and\
                    self.codeExtracts:
                self.xhtml = self.getCorrectTag(int(currentresult[0]),\
                                                int(currentresult[1]))
            res=self.result(currentresult)
            result = WAM_Results.WAM_Results(self.wamid,self.title,
                                               self.description,self.type,
                                               res,line=currentresult[0],
                                               column=currentresult[1],
                                               xhtml=self.xhtml)
        except AttributeError, e:
            raise AbstractWAMException, str(e)
          
        self.index = self.index+1
        return result

    def getCorrectTag(self, line, column):
        if not line:
            line = 1
        line -= 1
        content = self.content.split('\n')
        contentbefore = ''.join(content[:line]).strip()
        contentafter = ''.join(content[line+1:]).strip()
        try:
            retval = content[line]
        except IndexError:
            return 'An error occured accessing the code. No code extraction is available.'
        if column==0 and self.wamid.find('CSS')>-1:
            return 'We are sorry, but the code of style declarations can not be extracted in this version of the eAccessibility Checker.'
        minlength = 50
        contentbefore = contentbefore[-minlength:]
        contentafter = contentafter[:minlength]
        retval = contentbefore + retval + contentafter
        if len(retval)>1000:
            retval = retval[:1000]
        return retval


    def result(self,s):
        """
        Keyword arguments:

        s is the unique identifier tuple for the element involved.
        The identifier tuple contains the (line,col) of the element being assessed.
        """
        # Always overloaded
        pass

    def aWAM(self,awamid,index):
        """Retrieve the result of a given awam for a given index
        Keyword arguments:
        awamid -- ID of the Awam.
        index -- Index as (line,column) tuple 
        """
        try:
            return self.awamresult[awamid][index]
        except IndexError:
            return 0
        except KeyError:
            return 0

# Define abstract classes that does the footwork.
# Define methods for returning awam results, that also
# updates BWAM id's etc.

class AbstractB(AbstractWAM):
   # Abstract class for BWAM instances

   def __init__(self,awamresults,bwamid,awams,default=None, **args):
      """
      Abstract class for BWAMs
      """
      AbstractWAM.__init__(self,awamresults,bwamid,awams,AbstractB.BWAM,default=default,**args)

# Abstract class for M-WAMs
class AbstractM(AbstractWAM):

   def __init__(self,awamresults,awams,type,default=None, **args):
       AbstractWAM.__init__(self,awamresults,
                            WAM_Results.egovmonMwamId[type],
                            awams,type,default, **args)

