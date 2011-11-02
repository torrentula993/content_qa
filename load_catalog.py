import urllib
import json
from pprint import pprint 

LOOKUP_WSURL = 'http://ws.spotify.com/lookup/1/.json?uri='


if __debug__:
    def debug(values): 
	print(values)
	#ucontents = u'(%s)' % u','.join(unicode(x) for x in values)
	#print(ucontents)
else:
    def debug(*values): pass

def build_url(uri,type):
    return "%s%s&extras=%s" % (LOOKUP_WSURL,uri,type)

# json data selectors
def mock_selector(x): pass

def album_selector(json):
    return json['artist']['albums']

def track_selector(json):
    return json['album']['tracks']

def release_selector(json):
    al = json['album']
    return al['name'],al['released']

# actions
def releases_action(json,action=debug):
    data = release_selector(json)
    action(data)

def tracks_action(json,action=debug):
    album_href = json['album']['href']
    url = build_url(album_href,'trackdetail')
    parse_json(url,action,track_selector)

def albums_action(uri,action=tracks_action):
    url = build_url(uri,'albumdetail')
    parse_json(url,action,album_selector)

def results_action(item):
    rels = list()
    action = lambda j: rels.append(item)
    return rels

# methods
def list_releases(uri):
    rels = list()
    action = lambda j: rels.append(release_selector(j))
    albums_action(uri,action)
    rels.sort()
    return rels

# helper
def parse_json(url,action,selector):   
    for line in urllib.urlopen(url):
        js = json.loads(line)
        for item in selector(js):
            action(item)


radiohead='spotify:artist:4Z8W4fKeB5YxbusRsdQVPb'
#list_albums(radiohead)
rels = list_releases(radiohead)
pprint(rels)
#albums_action(radiohead,releases_action)


