
from lxml import html,etree

rawtext = open('test/sample.html').readlines()
text=''
for l in rawtext:
    text=text+l.replace('\n','')

tree = html.fromstring(text)

# grant
grantDate = tree.xpath("//time[@itemprop='grantDate']")[0].text
print(grantDate)

# description
description=''
for e in tree.xpath("//section[@itemprop='description']")[0].getchildren() :
    description=description+' '+str(e.text)
print(description)

for kw in tree.xpath("//dd[@itemprop='priorArtKeywords']"):
    print(kw.text)
