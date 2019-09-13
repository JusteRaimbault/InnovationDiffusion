
import selenium_get
from lxml import html,etree

url=open('urls/url').readline()

portrange=range(9055,9095)

for port in portrange:
    print(port)
    page=selenium_get.get_page(url,port,False,1)
    tree = html.fromstring(page)
    if len(tree.find_class('printTableText')):
        attempts=1
        success=1
        for i in range(100):
            page=selenium_get.get_page(url,port,False,1)
            tree = html.fromstring(page)
            attempts=attempts+1
            if len(tree.find_class('printTableText')):
                success=success+1
            print('i='+str(i)+" ; rate = "+str(100*success/attempts))  



