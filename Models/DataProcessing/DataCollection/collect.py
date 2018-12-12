
import pymongo
import utils
import requests
import time
from manager import TorPoolManager
from lxml import html,etree

DATABASE='uspto'
#DATABASE='test'
BULKSIZE = int(utils.get_parameter('bulksize',False,False))
print('bulksize : '+str(BULKSIZE))

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

url = open('url','r').readlines()[0].replace('\n','')


pool = TorPoolManager()
pool.switchPort(True)

successnum=0
start=time.time()

for i in range(0,BULKSIZE):
    rec = database['tocollect'].find_one_and_delete({'attempts':{"$lt":100}})
    if rec is not None:
        id = rec['id']
        attempts = 0
        if 'attempts' in rec : attempts = rec['attempts']
        print(str(id)+" ; "+str(attempts))
        try:
            pdata = requests.get(url+str(id),proxies=pool.proxies(), timeout=10)
            tree = html.fromstring(pdata.content)
            #print(pdata.content)
            #if len(tree.find('title'))>0:
            if len(tree.find_class('description'))>0:
                # insert raw html in db
                #print(tree.find_class('description')[0].text)
                print('ok')
                successnum=successnum+1
                text=str(pdata.content)
                database['raw'].insert_one({'id':id,'html':text,'size':len(text)})
            else :
                # put again id in tocollect
                database['tocollect'].insert_one({'id':id,'attempts':attempts+1})
        except Exception as e:
            print('exception : '+str(e))
            database['tocollect'].insert_one({'id':id,'attempts':attempts+1})
    else:
        print('Nothing to do (no records left)')


pool.releasePort()

print('Success rate = '+str(successnum/BULKSIZE))
print('Ellapsed time = '+str((time.time()-start))+'s')

