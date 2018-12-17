

# auth params
USER=`cat user`
PWD=`cat psswd`
AUTHDB=`cat authdb`
PORT=`cat port`

DB='uspto'
COLLECTION='raw'

#QUERYFILE=$1
#FIELDS='{"abstract":1,"title":1,"id":1,"year":1,"grant_date":1}'
#FIELDS="abstract,title,id,year"
FIELDS="id"

#mongoexport -u $USER -p $PWD --authenticationDatabase $AUTHDB --port $PORT --db $DB --collection $COLLECTION -f $FIELDS --queryFile $QUERYFILE --limit 2
mongoexport -u $USER -p $PWD --authenticationDatabase $AUTHDB --port $PORT --db $DB --collection $COLLECTION -f $FIELDS --type=csv -o $1


