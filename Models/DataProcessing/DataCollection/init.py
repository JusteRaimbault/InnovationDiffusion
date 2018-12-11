import pymongo,utils

DATABASE='uspto'
MINID=150
MAXID=4200000


mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

# fill id coll with id to collect
database['tocollect'].insert_many(range(MINID,MAXID))