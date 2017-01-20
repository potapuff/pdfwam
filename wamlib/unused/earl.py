"""
earl.py is the module for EARL generation. It takes WAM_Result objects from the BWAM assessments,
and wraps them in to EARL/XML.
"""


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


# Generate EARL
# Changes: Jan 22 2006 by Anand
# 1. Copied Nils changes here
# 2. Fixed invalid XML in <rdf:description> tag
# 3. XML must close with </rdf:RDF> not </rdf>
# 4. Replaced rdf:ID with rdf:about.
#
# NUM:
# Reintroduced rdf:id (It is supposed to be used for non-URL RDF references)
# Anand: Changes: Jul 5 06
#
# Performance enhancement in producing EARL chunks
# by using ''.join() and using a list object to
# manage intermediate chunks. 

__author__ = "Nils Ulltveit-Moe, Anand B. Pillai"
__updated__ = "$LastChangedDate$"
__version__ = "$Id: earl.py 2371 2006-07-21 12:15:19Z anand $"


from WAM_Results import *
import version

import urllib

class Earl:
   """
   Class for generating EARL from WAM_Results objects.
   """
   def __init__(self):
      self.report=u""
      self.reports = []
      self.requirementWritten={}

   def context(self):
      """
      EARL context (not used)
      """
      pass


   def testSubject(self,subject,title,date,resultMap,parsingresults=1):
      """
      Bind default subject to WAM_Results module
      """
      defaultTestSubject(subject)

      self.reports.append(u"""
<earl:TestSubject rdf:about="%s">
  <dc:title xml:lang="en">%s</dc:title> 
  <dc:date rdf:datatype="http://www.w3.org/2001/XMLSchema#gDate">%s</dc:date>""" % (urllib.quote(subject),
             title,
             date))
      if parsingresults:
          #Presenting parsing results does not make sence for all WAMs. 
          # See if web page has been filtered through Tidy
          try:
              resultMap['EIAO.A.0.0.0.2.HTML.13.1']
              self.reports.append(u"""
                  <eiao:tidy>1</eiao:tidy>""")
          except KeyError:
              self.reports.append(u"""
                   <eiao:tidy>0</eiao:tidy>""")
          # See if parsing of the HTML failed
          try:
              resultMap['EIAO.A.0.0.0.2.HTML.14.1']
              self.reports.append(u"""
                  <eiao:parsingFailed>1</eiao:parsingFailed>""")
          except KeyError:
              self.reports.append(u"""
                 <eiao:parsingFailed>0</eiao:parsingFailed>""")
      self.reports.append(u"""
          </earl:TestSubject>

      """)

   def earl(self):
      """
      Return the generated EARL
      """
      return u"""
<rdf:RDF xmlns:earl="http://www.w3.org/WAI/ER/EARL/nmg-strawman#"
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:foaf="http://xmlns.com/foaf/0.1/"
 xmlns:eiao="http://www.eiao.net/rdf/2.0#"
 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dct="http://purl.org/dc/terms/"
 xml:base="%s">

   %s
</rdf:RDF>
      """ % (XMLBASE, u"".join(self.reports))

   def assertor(self,wamid,wamname,description,version):
      """
      Set EARL assertor <earl:Software>).
      """
      self.reports.append(u"""
<earl:Software rdf:about="%s">
  <dc:title xml:lang="en">%s</dc:title>
  <dc:description xml:lang="en">%s</dc:description>
  <dct:hasVersion>%s</dct:hasVersion>
</earl:Software>
      """ % (wamid,
             wamname,
             description,
             version))             

   def requirement(self,bresult):
      """
      Set EARL test requirement <earl:TestRequirement>
      """
      self.reports.append(u"""
<earl:TestRequirement rdf:ID="%s">
  <dc:title xml:lang="en">%s</dc:title>
  <dc:description xml:lang="en">%s</dc:description>
</earl:TestRequirement>
      """ % (bresult.earlRequirementId(),
             bresult.earlTestcaseTitle(),
             bresult.earlDescription()))


   def assertion(self,bresult):
      """
      Set EARL assertion <earl:assertion>
      """
      # Make sure the assertor is printed once
      try:
         self.requirementWritten[bresult.earlRequirementId()]
      except KeyError:
         self.requirementWritten[bresult.earlRequirementId()]=1
         self.requirement(bresult)

      self.location(bresult)
      self.result(bresult)

      if bresult.message:
          self.reports.append(u"""
<earl:Assertion rdf:ID="%s">
        <earl:assertedBy rdf:resource="%s"/>
        <earl:subject rdf:resource="%s"/>
        <earl:requirement rdf:resource="#%s"/>
        <earl:mode rdf:resource="%s"/>
        <earl:result rdf:resource="#%s"/>
        <eiao:singleLocation rdf:resource="#%s"/>
        <earl:message>%s</earl:message>
</earl:Assertion>
          """ % (bresult.earlAssertionId(),
             bresult.earlAssertedBy(),
             bresult.earlSubject(),
             bresult.earlRequirementId(),
             bresult.earlMode(),
             bresult.earlValidityId(),
             bresult.eiaoSingleLocationId(),
             bresult.earlMessage()))
      else:
          self.reports.append(u"""
<earl:Assertion rdf:ID="%s">
        <earl:assertedBy rdf:resource="%s"/>
        <earl:subject rdf:resource="%s"/>
        <earl:requirement rdf:resource="#%s"/>
        <earl:mode rdf:resource="%s"/>
        <earl:result rdf:resource="#%s"/>
        <eiao:singleLocation rdf:resource="#%s"/>
</earl:Assertion>
          """ % (bresult.earlAssertionId(),
             bresult.earlAssertedBy(),
             bresult.earlSubject(),
             bresult.earlRequirementId(),
             bresult.earlMode(),
             bresult.earlValidityId(),
             bresult.eiaoSingleLocationId()))

   def result(self,bresult):
      """
      Set EARL result <earl:result>
      """
      if bresult.mode == HEURISTIC:
          self.reports.append("""
              <earl:result rdf:ID="%s">
                  <earl:validity rdf:resource="%s"/>
                  <eiao:barrierIndicator>%g</eiao:barrierIndicator>
                  <eiao:probability>%f</eiao:probability>
              </earl:result>
          """ % (bresult.earlValidityId(),
                 bresult.earlResult(),
                 float(bresult.result),
                 float(bresult.prob)))
      else:
          self.reports.append("""
          <earl:result rdf:ID="%s">
              <earl:validity rdf:resource="%s"/>
              <eiao:barrierIndicator>%g</eiao:barrierIndicator>
          </earl:result>
          """ % (bresult.earlValidityId(),
                 bresult.earlResult(),
                 float(bresult.result)))

   def location(self,bresult):
      """
      Set EARL location <earl:location>
      """
      self.reports.append(u"""
<eiao:SingleLocation rdf:ID="%s">
        <eiao:line>%d</eiao:line>
        <eiao:column>%d</eiao:column>
</eiao:SingleLocation>
      """ % (bresult.eiaoSingleLocationId(),
             bresult.eiaoLine(),
             bresult.eiaoColumn()))

   def metaData(self,result):
      """
      Set EIAO MetaData <eiao:MetaData>
      """
      self.location(result)

      self.reports.append(u"""
<eiao:MetaData rdf:ID="%s">
        <earl:subject rdf:resource="%s"/>
        <eiao:type rdf:resource="%s"/>
        <eiao:value>%s</eiao:value>
        <eiao:singleLocation rdf:resource="#%s"/>
</eiao:MetaData>
      """ % (result.eiaoMetaDataId(),
             result.earlSubject(),
             result.eiaoType(),
             result.eiaoValue(),
             result.eiaoSingleLocationId()))
