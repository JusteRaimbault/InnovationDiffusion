
import pymongo
import utils
from manager import TorPoolManager
from lxml import html,etree

DATABASE='uspto'
BULKSIZE = utils.get_parameter('bulksize',True,True)

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo[DATABASE]

url = open('url','r').readlines()[0].replace('\n','')


pool = TorPoolManager()
pool.switchPort(True)

for i in range(0,BULKSIZE):
    id = db['tocollect'].findOneAndDelete()['id']
    print(id)
    try:
        pdata = requests.get(url+str(id),proxies=pool.proxies(), timeout=10)
        tree = html.fromstring(pdata.content)
        if len(tree.find_id('title'))>0:
            # insert raw html in db
            print(tree.find_id('title')[0].text)
            db['raw'].insert_one({'id':id,'html':pdata.content})
        else :
            # put again id in tocollect
            db['tocollect'].insert_one({'id':id})
    except Exception as e:
        db['raw'].insert_one({'id':id})
