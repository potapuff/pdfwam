# -- coding: utf-8

""" Caching of PDF wam results in memory using Redis. """

import redis
import time
import datetime
import cPickle
import hashlib

# Comment
from TingtunUtils.patterns import SingletonMeta

def getInstance():
    """ Return the single instance """

    return ResultsCache()

class ResultsCache(object):
    """ Cache for search results """

    __metaclass__ = SingletonMeta
    
    def __init__(self):
        self._server = redis.StrictRedis(host='localhost',port=6379)
        # Key sep
        self._keysep = '@@'
        # Namespace sep
        self._nsep = ':'
        # Salt for hashes
        self.__salt = 'Tingtun_Pdfwam'
        
    def _flatten(self, key, namespace=''):
        """ Flatten a given key. Produces a string out of it
        if the input is list or tuple """
        
        # Flatten the key out
        if type(key) in (list, tuple):
            mykey = self._keysep.join(map(lambda x:str(x), key))
        else:
            mykey = key

        if namespace:
            # Prefix namespace
            return self._nsep.join((namespace, mykey))
        else:
            return mykey

    def _unflatten(self, key):
        """ Unflatten a given key """

        # Split according to namespace separator if any
        namespace, rest = key.split(self._nsep, 1)
        # Split further if any
        if rest:
            rest, hashspace = rest.split(self._keysep, 1)
            return namespace, hashspace, rest

        return namespace, '', rest
        
    def _setSimpleCache(self, namespace, key, value, ttl=0):
        """ Set simple cache for redis using a namespace. No hashes are used. """

        # Flattened key
        fkey = self._flatten(key, namespace)
        ret = self._server.set(fkey, cPickle.dumps(value))
        
        if ttl>0:
            self._server.expire(fkey, ttl)

        return ret

    def _getSimpleCache(self, namespace, key):
        """ Get simple cache for redis using a namespace. No hashes are used. """

        # Flattened key
        fkey = self._flatten(key, namespace)
        try:
            return cPickle.loads(self._server.get(fkey))
        except TypeError:
            pass
        
    def getResultsCache(self, url):
        """ Get cache for WAM results, given a key """

        # Key is a hash of URL + a salt
        key = hashlib.sha1(url + self.__salt).hexdigest()
        return self._getSimpleCache('__pdfwam__', key)

    def setResultsCache(self, url, value, ttl=2592000):
        """ Set cache for WAM results """

        key = hashlib.sha1(url + self.__salt).hexdigest()
        # PDF-WAM results have a max cache life of 1 month.
        result = self._setSimpleCache('__pdfwam__', key, value, ttl=ttl)
        return result
    
    def clear(self):
        """ Flush all keys from DB """

        self._server.flushall()

if __name__ == "__main__":
    pass

        
