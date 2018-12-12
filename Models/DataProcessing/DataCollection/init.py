import pymongo,utils

DATABASE='uspto'
#DATABASE='test'
MINID=150
MAXID=4200000
#MINID=9000
#MAXID=10000


mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

database['tocollect'].drop()

# fill id coll with id to collect
ids = [{'id':i,'attempts':0} for i in list(range(MINID,MAXID))]

database['tocollect'].insert_many(ids)



