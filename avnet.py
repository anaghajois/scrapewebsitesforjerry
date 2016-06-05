from bs4 import BeautifulSoup
import urllib2

headers = {'User-Agent': "Anagha Browser",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
url = 'http://products.avnet.com/webapp/wcs/stores/servlet/SearchDisplay?categoryId=&storeId=715839035&catalogId=10001&langId=-1&sType=SimpleSearch&resultCatEntryType=2&searchSource=Q&searchType=100&avnSearchType=all&searchTerm=A1101R04C'
request = urllib2.Request(url, headers= headers)
response = urllib2.urlopen(request)
page = response.read()
page_soup = BeautifulSoup(page, 'html.parser')

allitem_soup = page_soup.find_all('div', class_ = 'table-colLeft')
items = []
for item in allitem_soup:
    if 'upper_case_txt' not in item['class']:
        items.append(item)

for item in items:
    print item.find('span', class_= 'blue_clr').a.string

allitem_soup = page_soup.find_all('div', class_ = 'gs_colPrice')
items = []
for item in allitem_soup:
    if 'upper_case_txt' not in item['class']:
        items.append(item)

for item in items:
    print item#.find('div', class_= 'rightContentCell')

allitem_soup = page_soup.find_all('div', class_ = 'gs_colAvail Cell')
items = []
for item in allitem_soup:
    if 'upper_case_txt' not in item['class']:
        items.append(item)

for item in items:
    print item#.find('div', class_= 'rightContentCell')
