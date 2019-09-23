

#####
# tor ip rotation ?
#  https://stem.torproject.org/api/process.html
#  https://github.com/erdiaker/torrequest/blob/master/torrequest.py
#  https://tor.stackexchange.com/questions/9934/tor-is-only-assigning-circuits-from-a-very-limited-subset-of-exit-nodes




import selenium_get
from lxml import html,etree

url=open('urls/url').readline()

portrange=range(9055,9095)

success=0

for port in portrange:
    print(port)
    page=selenium_get.get_page(url,port,False,2)
    tree = html.fromstring(page)
    if len(tree.find_class('printTableText')):
        success=success+1
        print(tree.find_class('printTableText')[0].text)

print('rate : '+str(success/len(portrange)))
