import pymongo
import utils
import time
import parser

DATABASE='uspto'
#DATABASE='test'
BULKSIZE = int(utils.get_parameter('bulksize',False,False))
print('bulksize : '+str(BULKSIZE))

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

successnum=0
start=time.time()

for i in range(0,BULKSIZE):
    rec = database['raw'].find_one_and_delete({})
    if rec is not None:
        try:
            parsed = parser.parse(rec['id'],rec['html'])
            if parser.validate(parsed):
                successnum = successnum + 1
                print(parser.to_string(parsed))
                database['patents'].insert_one(parsed)
            else :
                # put again id in tocollect
                database['raw'].insert_one(rec)
        except Exception as e:
            print('exception : '+str(e))
            database['raw'].insert_one(rec)
    else:
        print('Nothing to do (no records left)')


print('Success rate = '+str(successnum/BULKSIZE))
print('Ellapsed time = '+str((time.time()-start))+'s')
