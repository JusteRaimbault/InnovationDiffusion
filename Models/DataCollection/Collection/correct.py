import pymongo

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo['uspto']

#BULKSIZE=5000
BULKSIZE=10

for i in range(0,BULKSIZE):
    rec = database['patents'].find_one_and_delete()
    if rec is not None:
        try:
            rec['text']=str(rec['text'])
            print(rec)
            database['patents_correct'].insert_one(rec)
        except Exception as e:
            print('exception : '+str(e))
            database['patents'].insert_one(rec)

#database['patents_correct'].rename('patents')
