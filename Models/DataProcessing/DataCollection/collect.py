
import pymongo

BULKSIZE = utils.get_parameter('bulksize',True,True)


db.collection.findOneAndDelete(
