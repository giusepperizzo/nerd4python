"""
    nerd4python -   A python library which provides an interface to NERD
                    http://nerd.eurecom.fr

    Copyright 2012 

    Authors:
        Giuseppe Rizzo <giuseppe.rizzo@eurecom.fr>
        Pierre-Antoine Champin <pierre-antoine.champin@liris.cnrs.fr>

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License published by
    the Free Software Foundation, either version 3 of the License, or (at 
    your option) any later version. See the file Documentation/GPL3 in the
    original distribution for details. There is ABSOLUTELY NO warranty.    
"""

from httplib import HTTPConnection
from urllib import urlencode
from warnings import warn

try:
    from json import loads as json_loads
except ImportError:
    # fall back to poor man's JSON; this is fragile and unsafe, so we warn:
    warn("No JSON support - using 'eval' instead")
    json_loads = eval # bad name #pylint: disable=C0103

class NERD(object):
    """Connection to the NERD service.
    """
    def __init__(self, api_key, user_agent=None):
        self.api_key = api_key
        self.http = HTTPConnection("nerd.eurecom.fr")

        if user_agent is None:
            user_agent = "NERD python library 0.2"
        self._headers = {
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json",
            "user-agent": user_agent,
            }


    def extract(self, text, language, service):
        """Extract named entities from document with 'service'.        
        'service' can be any of the constants defined in this module.
        """

        """ submit document """
        self.http.request("POST", "/api/document",
                          urlencode({"text": text, 
                                     "key": self.api_key}),
                          self._headers,
                          )
        response = self.http.getresponse()
        if response.status / 100 != 2:
            raise Exception("%s %s" % (response.status, response.reason))
        json = response.read()
        _debug(response, json)
        data = json_loads(json)
        id_document = data["idDocument"]


        """ annotate document """
        self.http.request("POST", "/api/annotation/%s" % service,
                          urlencode({"idDocument": id_document,
                                     "language": language,
                                     "key": self.api_key}),
                          self._headers,
                          )
        
        response = self.http.getresponse()
        if response.status / 100 != 2:
            raise Exception("%s %s" % (response.status, response.reason))
        json = response.read()
        _debug(response, json)
        data = json_loads(json)
        id_extraction = data["idExtraction"]


        """ get extraction from the annotation """
        self.http.request("GET", "/api/extraction/%s" % id_extraction + "?key=%s" % self.api_key,
                          headers = self._headers,
                          )
        response = self.http.getresponse()
        if response.status / 100 != 2:
            raise Exception("%s %s" % (response.status, response.reason))
        json = response.read()
        _debug(response, json)
        data = json_loads(json)
        return data

def _debug(response, body):
    """Print response headers and body for debug.
    """
    print ">>>", response.status, response.reason,
    for h in response.getheaders():
        print h
    print
    print body, "<<<"

ALCHEMYAPI = "alchemyapi"
DBPEDIA_SPOTLIGHT = "spotlight"
EVRI = "evri"
EXTRACTIV = "extractiv"
ONTOTEXT_LUPEDIA = "ontotext"
OPENCALAIS = "opencalais"
SAPLO = "saplo"
WIKIMETA = "wikimeta"
YAHOO = "yahoo"
ZEMANTA = "zemanta"
