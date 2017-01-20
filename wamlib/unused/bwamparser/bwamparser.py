import re

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


__author__ = "$Author$"
__version__ = "$Revision$"
__updated__ = "$LastChangedDate$"

AWAMID=1
BWAMID=2
NR=3
WORD=4
DOT=5
LPAREN=6
RPAREN=7
EQUALTO=8
ASSIGNEDTO=9
MINUS=10
PLUS=11
OTHER=12
WS=13


class st:
   INITIAL=0
   AWAMId=1
   BWAMId=2
   EXPRESSION=3

class BWAMParseError(Exception):
   """ Report parse errors """

operatorDict={
"and":"and",
"AND":"and",
"or":"or",
"OR":"or",
"not":"not",
"NOT":"not"}

class BwamParser:
   def __init__(self):
      self.tokStack=[]
      self.valStack=[]
      self.awams=[]
      self.regexp=re.compile(r"""
        (\w+\.\w+\.\d+\.\d+\.\d+\.\d+\.\w+\.\d+\.\d+\(\w\)) |      # 1) AWAMId
        (\w+\.\w+\.\d+\.\d+\.\d+\.\d+\.\w+\.\w+\.\d+\.\d+\(\w\)) | # 2) BWAMId
        (\d+)| # 3) Match digits
        (\w+)| # 4) Match words
        ([.])| # 5) Match period
        ([(])| # 6) Match start paren
        ([)])| # 7) Match end paren
        (==) | # 8) Match equality
        (=)  | # 9) Match equal sign
        ([-])| # 10) Match minus sign
        ([+])| # 11) Match plus sign
        (.)  | # 12) Match  other character
        (\s)   # 13) Match  whitespace
        """,re.VERBOSE) # Use verbose, readable re syntax

   def next(self):
      # Return next match
      m = self.scanner.match()
      if not m:
         return (None,None)
      """Branch based on regexp. group match number"""
      self.valStack.append(m.group())
      self.tokStack.append(m.lastindex)
      return m.lastindex,m.group()

   def match(self,pattern):
      if pattern == self.tokStack[-len(pattern):]:
         # Found matching pattern
         result=self.valStack[-len(pattern):]
         # Pop result from stack
         self.tokStack[-len(pattern):]=[]
         self.valStack[-len(pattern):]=[]
         return result
      else:
         return None 

   def pop(self):
      return self.tokStack.pop(),self.valStack.pop() 

   def parse(self,bwamexpr):
      self.scanner=self.regexp.scanner(bwamexpr)
      state=[st.INITIAL]
      expression=[]
      self.awamcount=0
      self.awams=[]
      while 1:
         (token,value)=self.next()
         if state[-1] == st.EXPRESSION and token==None:
            return " ".join(expression)
         if token in (WS,OTHER):
            # Ignore whitespace
            self.pop()
            continue

         if token==BWAMID:
            if state[-1] == st.INITIAL:
               self.bwamid=value[:-3]
               state.append(st.BWAMId)
               self.pop()
               continue
            else:
                raise BWAMParseError("Parse error at or near "+"".join(bwamId))
         if token==ASSIGNEDTO:
            if state[-1] == st.BWAMId:
               #print "Got ="
               state = [st.EXPRESSION]
               continue
            else:
               raise BWAMParseError("Parse error at or near =")
         # Not yet very thorough syntax checking of expressions
         if token==AWAMID:
            if state[-1] == st.EXPRESSION:
               expression.append('int(self.aWAM("%s",s))'%value[:-3])
               self.awamcount+=1
               self.awams.append(value[:-3])
               self.pop()
               continue
            else:
               raise BWAMParseError("Parse error at or near "+value[:-3])
         if token==LPAREN:
            if state[-1] == st.EXPRESSION:
               expression.append("(") 
            continue
         if token==RPAREN: 
            if state[-1] == st.EXPRESSION:
               expression.append(")") 
            else:
               state.pop()
            continue
         if token==EQUALTO:
            if state[-1] == st.EXPRESSION:
               expression.append("==") 
            else:
               raise BWAMParseError("Parse error at or near ==")
            continue
         if token==WORD:
            if state[-1] == st.EXPRESSION:
               try:
                  expression.append(operatorDict[value])
                  self.pop()
               except KeyError:
                  pass
         if token in (NR,MINUS,PLUS):
            # Handle numbers
            if state[-1] == st.EXPRESSION:
               expression.append(value)
               self.pop()

if __name__ == "__main__":
   p=BwamParser()
   res=p.parse("""
UWEM.B.10.6.4.2.HTML.DEF.1.1(s) = 1 -
NOT (EIAO.A.10.6.4.2.HTML.1.1(s) and
     EIAO.A.10.6.4.2.HTML.2.1(s) ==
     EIAO.A.10.6.4.2.HTML.3.1(s) and
     EIAO.A.10.6.4.2.HTML.4.1(s) and
     EIAO.A.10.6.4.2.HTML.5.1(s))""") 
   print "#AWAMs: ",p.awamcount
   print "class %s(AbstractB):" % "_".join(p.bwamid.split("."))
   print "   def result(self,s):"
   print "      return ",res
   print
   print 'wamrules.append(%s("%s"))' % ("_".join(p.bwamid.split(".")),p.bwamid)

