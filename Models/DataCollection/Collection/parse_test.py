
import pymongo
import parser

mongo = pymongo.MongoClient(utils.get_parameter('mongopath',True,True))
database = mongo['uspto']

batchsize=100

validated=0

for d in database['raw'].find({},{},batchsize):
    sample = parser.parse(d['id'],d['html'])
    if parser.validate(sample):
        validated = validated + 1
    print(parser.to_string(sample))

print('Validated: '+str(validated/batchsize))



#
# sample = parser.parse('169',parser.getrawtext('test/sample.html'))
# print(parser.validate(sample))
# print(parser.to_string(sample))
#
# sample1 = parser.parse('170',parser.getrawtext('test/sample1.html'))
# print(parser.validate(sample1))
# print(parser.to_string(sample1))
#
# samplechem = parser.parse('7608600',parser.getrawtext('test/samplechemistry.html'))
# print(parser.validate(samplechem))
# print(parser.to_string(samplechem))
#
# sampleshoe = parser.parse('8230618',parser.getrawtext('test/sampleshoe.html'))
# print(parser.validate(sampleshoe))
# print(parser.to_string(sampleshoe))
