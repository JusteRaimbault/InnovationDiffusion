
import requests
from io import BytesIO

headers_1 = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'none',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}

headers_2 = {
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Connection': 'keep-alive',
}


url = open('urls/url1').readline().replace(' ','')
print('url : '+url)

#headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

#r = requests.get(url,headers = headers)
r = requests.get(url,headers = headers_1,proxies={'http':'socks5://127.0.0.1:9050'})
print('Cookies : '+str(r.cookies))

#url2 = open('urls/url2').readline()
#r2 = requests.get(url2,headers = headers_2,cookies = r.cookies,proxies={'http':'socks5://127.0.0.1:9050'})
url2 = open('urls/urldirect').readline().replace('\n','')
r2 = requests.get(url2,headers = headers_2,cookies = r.cookies)

print(url2)
print(r2.headers)
print(r2.content)

#with open('test/pdfpy.pdf','wb') as out:
#    out.write(BytesIO(r2.content).read())

rip = requests.get("http://api.ipify.org",proxies={'http':'socks5://127.0.0.1:9050'})
print(rip.headers)
print(rip.content)
