
from spotify.content_common import strings

import csv,sys
import pprint

_cache = dict()

if __debug__:
    def debug(values): print(values)
else:
    def debug(*values): pass

def print_header(str,len=35):
    print("%s %s %s" % ("-"*len,str,"-"*len) )

def artist_name(artist): # from db
    return artist['name'].title()

def artist_gid(artist): 
    return artist['gid'].title()

def cache_similarity(key1,key2,s):
    str1 = key1.encode('ascii','ignore')
    str2 = key2.encode('ascii','ignore')
    _cache[(str1,str2)] = s
    _cache[(str2,str1)] = s        

def get_similarity(str1,str2,threshhold):
    if (str1,str2) in _cache:
        debug("cache hit")
        s = _cache[(str1,str2)]
    else:
        debug("cache miss")
        s = round(strings.similarity(str1,str2),1)
        cache_similarity(str1,str2,s)        
    return s

def similar(str1,str2,threshhold):
    # !caching: only saves 3s of exec time!
    s = round(strings.similarity(str1,str2),1) 
    similar= (s>=threshhold)
    debug("(%s,%s): %s - %s" % (similar,s,str1,str2))
    return s if similar else False


def find_duplicates(artists,threshhold):
    print("sorting names...")
    keys = artists.keys()
    keys.sort()
    print("finding duplicates...")
    last,dups = keys[-1], list()
    for i in range(len(keys)-2, -1, -1):
        if last != keys[i]:  #order(N*log2(N)?)
            #if similar(last,keys[i],threshhold):
	    name = artist_name(artists[last])
	    tmpname = artist_name(artists[keys[i]])
 	    if similar(name,tmpname,threshhold):
                dups.append(artists[last])
                dups.append(artists[keys[i]])
            else:
                last = keys[i]
    return dups

def load_csv(filename): 
    artists = dict()
    with open(filename,'rt') as f:
        print("loading artists...")
        for row in csv.DictReader(f):
            gid = artist_gid(row)
            artists[gid]=row
    return artists 

def main():
    artists = load_csv(sys.argv[1])
    dups = find_duplicates(artists,.8)
    pp = pprint.PrettyPrinter(width='150')
    pp.pprint(dups)
    print("count: %s" % len(dups))

def test():
    similar("Smashing Pumpkins","The Smashing Pumpkins",1)
    similar("Smashing Pumpkins","Smushing Pumpkins",1)
    similar("Smashing Pumpkins","The Smashing Pumpkins featuring Handjob",1)
    similar("Smashing Pumpkins","Compilation: Smashing Pumpkins",1)
    similar("Smashing Pumpkins","Aerosmith featuring The Smashing Pumpkins",1)

main()
