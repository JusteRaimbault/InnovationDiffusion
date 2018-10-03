import pymongo,sys,os
import parser,utils

MONGOPATH = open('.mongopath').readlines()[0]
DATABASE = get_parameter("databaseraw",as_string=True)

COLLECTION = 'patents'

# Specific data import with caracs / text in separate repos
# generic with any number of directories
# consolidate with an unique id
def import_data(dirs):
    print('importing file '+str(f))
    mongo = pymongo.MongoClient(MONGOPATH)
    database = mongo[DATABASE]

    database[COLLECTION].create_index('id')

    dicos = {}
    # load all dicos
    for dir in dirs:
        currentdic = {}
        for f in os.listdir(dir):
            currentdata = parser.parse_csv(f,',','appln_id')
            currentdic.update(currentdata)
        dicos[str(dir)]=currentdic

    # consolidate dicos
    data = {}
    for dir in dicos.keys():
        for id in dicos[dir].keys():
            print(id)
            if id in data:
                data[id].update(dicos[dir][id])
            else :
                data[id] = dicos[dir][id]

    # insert the data
    database[COLLECTION].insert_many(data)

import_data(['../../../Data/Data/tls/tls201','../../../Data/Data/tls/tls203'])
