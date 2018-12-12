
import pymongo
import utils
import requests
from manager import TorPoolManager
from lxml import html,etree

#DATABASE='uspto'
DATABASE='test'
BULKSIZE = int(utils.get_parameter('bulksize',False,False))
print('bulksize : '+str(BULKSIZE))

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

url = open('url','r').readlines()[0].replace('\n','')


pool = TorPoolManager()
pool.switchPort(True)

for i in range(0,BULKSIZE):
    id = database['tocollect'].find_one_and_delete({})['id']
    print(id)
    try:
        pdata = requests.get(url+str(id),proxies=pool.proxies(), timeout=10)
        tree = html.fromstring(pdata.content)
        print(pdata.content)
        #if len(tree.find('title'))>0:
        if len(tree.find_class('description'))>0:
            # insert raw html in db
            print(tree.find_class('description')[0].text)
            database['raw'].insert_one({'id':id,'html':str(pdata.content)})
        else :
            # put again id in tocollect
            database['tocollect'].insert_one({'id':id})
    except Exception as e:
        print('exception : '+str(e))
        database['tocollect'].insert_one({'id':id})
