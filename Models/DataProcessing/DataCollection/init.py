import pymongo,utils

#DATABASE='uspto'
DATABASE='test'
MINID=150
#MAXID=4200000
MAXID=10000


mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

# fill id coll with id to collect
ids = [{'id':i} for i in list(range(MINID,MAXID))]

database['tocollect'].insert_many(ids)



