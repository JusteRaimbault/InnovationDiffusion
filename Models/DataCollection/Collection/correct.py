import pymongo
import utils

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo['uspto']

#BULKSIZE=5000
BULKSIZE=2

for i in range(0,BULKSIZE):
    #rec = database['patents'].find_one_and_delete({})
    rec = database['patents_correct'].find_one_and_delete({})
    #rec = database['patents_correct'].find_one({})
    if rec is not None:
        try:
            #rec['text']=rec['text']
            rec['text']=rec['text'][1:].replace('"','')
            database['patents'].insert_one(rec)
        except Exception as e:
            print('exception : '+str(e))
            database['patents_correct'].insert_one(rec)

#database['patents_correct'].rename('patents')
