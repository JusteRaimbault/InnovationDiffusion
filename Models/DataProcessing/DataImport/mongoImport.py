import pymongo,sys,os
import parser,utils

MONGOPATH = open('.mongopath').readlines()[0]
DATABASE = utils.get_parameter("databaseraw",as_string=True)
#DATABASE='test'

COLLECTION = 'patents'
#COLLECTION='test'

#print(MONGOPATH)

# Specific data import with caracs / text in separate repos
# generic with any number of directories
# consolidate with an unique id
def import_data(dirs):
    mongo = pymongo.MongoClient(MONGOPATH,29019)
    database = mongo[DATABASE]

    database[COLLECTION].create_index('id')

    dicos = {}
    # load all dicos
    for dir in dirs:
        currentdic = {}
        for f in os.listdir(dir):
            currentdata = parser.parse_csv(dir+'/'+f,',','"','appln_id')
            currentdic.update(currentdata)
        dicos[str(dir)]=currentdic

    # consolidate dicos
    data = {}
    for dir in dicos.keys():
        for id in dicos[dir].keys():
            #print(id)
            if id in data:
                data[id].update(dicos[dir][id])
            else :
                data[id] = dicos[dir][id]

    # filter
    filtdata=[]
    for id in data.keys():
        currentrec=data[id]
        if int(currentrec['appln_filing_year'])>=1985 and currentrec['appln_auth'] in ['EP','US','JP'] and 'appln_abstract' in currentrec.keys():
            filtdata.append(currentrec)

    # insert the data
    #print(data)
    #print(type(data.values()))
    #print(type(data[data.keys()[0]]))
    database[COLLECTION].insert_many(filtdata)

import_data(['../../../Data/Data/tls/tls201','../../../Data/Data/tls/tls203'])
#import_data(['../../../Data/Data/test/list','../../../Data/Data/test/text'])

