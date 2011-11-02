#!/usr/bin/python
 
import urllib2, BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from pprint import pprint

BRAINZ_API='http://musicbrainz.org/ws/2/'


def build_url(type,mbid,inc):
    return "%s%s/%s?inc=%s" % (BRAINZ_API,type,mbid,inc)

def opensoup (url):
        """
        returns (page, actualurl)
        sets user_agent and resolves possible redirection
        realurl maybe different than url in the case of a redirect
        """
        request = urllib2.Request(url)
        user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080418 Ubuntu/7.10 (gutsy) Firefox/2.0.0.14"
        request.add_header("User-Agent", user_agent)
        pagefile=urllib2.urlopen(request)
        soup=BeautifulSoup.BeautifulSoup(pagefile, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        realurl = pagefile.geturl()
        pagefile.close()
        return (soup, realurl)

def artist_request(mbid):
    url = build_url('artist',mbid,'aliases')
    soup,rlurl = opensoup(url)
    return soup

def get_contents(tags):
    contents = list()
    #tags = entity.findAll(tagname)
    for tag in tags:
        contents.append(tag.contents[0])
        #print value.encode("UTF-8",'ignore')
    ucontents = u'[%s]' % u','.join(unicode(x) for x in contents)
    return ucontents


def test():

    radiohead='a74b1b7f-71a5-4011-9441-d0b5e4122711'

    entity = artist_request(radiohead)
    print entity.prettify()

    aliases = entity.findAll('alias')
    contents = get_contents(aliases)
    print contents


test()




