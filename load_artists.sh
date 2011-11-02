#!/bin/bash

REMOTE_HOST=bailey@sadie.int.sto.spotify.net
TMPFILE=/tmp/artists.log

DB_CMD='psql -h content-db.int.sto.spotify.net -U spotify-content-merger-read -d metadata -c "COPY(select name,gid from artist) TO STDOUT WITH CSV HEADER;"' 

echo retrieving artists from database...
#ssh $REMOTE_HOST $DB_CMD '| gzip -c >' $TMPFILE
#scp $REMOTE_HOST:$TMPFILE $TMPFILE
ssh -C $REMOTE_HOST $DB_CMD > $TMPFILE

echo cleanup...
#ssh $REMOTE_HOST rm -f $TMPFILE

echo "done"

