import pymongo,sys
import parser

MONGOPATH = open('.mongopath').readlines()[0]
# 'mongodb://root:root@127.0.0.1:29019'

def import_file(f,db,collection):
    print('importing file '+str(f))
    mongo = pymongo.MongoClient(MONGOPATH)
    database = mongo['db']

    database[collection].create_index('id')

    data = parser.parse_csv(f)
    #year = f.split('/')[1].split('.')[0].split('_')[0]
    #data = parser.parse_file(f,year)

    database[collection].insert_many(data)


#import_file(sys.argv[1])
