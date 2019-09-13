
import selenium_get
from lxml import html,etree

url=open('urls/url').readline()

portrange=range(9055,9095)

success=0

for port in portrange:
    print(port)
    page=selenium_get.get_page(url,port,False)
    tree = html.fromstring(page)
    if len(tree.find_class('printTableText')):
        success=success+1
        print(tree.find_class('printTableText')[0].text)

print('rate : '+str(success/len(portrange)))



