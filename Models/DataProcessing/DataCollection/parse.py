
from lxml import html,etree

rawtext = open('test/sample.html').readlines()
text=''
for l in rawtext:
    text=text+l.replace('\n','')

tree = html.fromstring(text)

grantDate = tree.xpath("//time[@itemprop='grantDate']")[0].text
print(grantDate)

for kw in tree.xpath("//dd[@itemprop='priorArtKeywords']"):
    print(kw.text)
