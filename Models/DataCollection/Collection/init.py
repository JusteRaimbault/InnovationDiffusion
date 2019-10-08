import pymongo,utils

#DATABASE='uspto'
DATABASE='test'



# GB
MINID=100001
MAXID=101001 # test
# MAXID=1605470

# US
# first phase
#
#MINID=150
#MAXID=4200000

#MINID=4200001
# on 2018/12/13, latest id is 10149420
#MAXID=10149420
#on 2019/09/12, latest id is 10368470 (granted 07/30)
#MAXID=10368470
#drop=False

# testing
#MINID=9000
#MAXID=10000

# drop to update with existing raw
#drop = True
drop = False

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

if drop :
    database['tocollect'].drop()

existing = set([e['id'] for e in list(database['raw'].find({},{'id':1}))])
tocollect = list(set(range(MINID,MAXID)).difference(existing))
print('Missing ids: '+str(len(tocollect)))

# fill id coll with id to collect
ids = [{'id':i,'attempts':0} for i in tocollect]

database['tocollect'].insert_many(ids)
