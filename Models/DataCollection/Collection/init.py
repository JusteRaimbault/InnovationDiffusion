import pymongo,utils

DATABASE='uspto'
#DATABASE='test'

# first phase
#MINID=150
#MAXID=4200000

# on 2018/12/13, latest id is 10149420
MINID=4200001
MAXID=10149420
drop=False

# testing
#MINID=9000
#MAXID=10000


mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

#if drop :
#    database['tocollect'].drop()

# fill id coll with id to collect
ids = [{'id':i,'attempts':0} for i in list(range(MINID,MAXID))]

database['tocollect'].insert_many(ids)



