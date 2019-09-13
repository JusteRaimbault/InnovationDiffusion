
import requests
from io import BytesIO

url = open('url1').readline().replace(' ','')
print('url : '+url)

#headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

#r = requests.get(url,headers = headers)
r = requests.get(url)
print('Cookies : '+str(r.cookies))

url2 = open('url2').readline()
r2 = requests.get(url2)

with open('test/pdfpy.pdf','wb') as out:
    out.write(BytesIO(r2.content).read())
