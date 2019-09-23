
import pymongo
import parser


# sample = parser.parse('169',parser.getrawtext('test/sample.html'))
# print(sample)
# print(parser.validate(sample))
#
# sample1 = parser.parse('170',parser.getrawtext('test/sample1.html'))
# #print(sample1)
# print(parser.validate(sample1))

samplechem = parser.parse('7608600',parser.getrawtext('test/samplechemistry.html'))
#print(samplechem)
print(parser.validate(samplechem))

sampleshoe = parser.parse('8230618',parser.getrawtext('test/sampleshoe.html'))
#print(samplechem)
print(parser.validate(sampleshoe))
