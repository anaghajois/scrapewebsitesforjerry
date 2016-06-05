from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import re

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def sanitize(lst):
    sanitized_lst = []
    for item in lst:
        item_text = item.get_attribute("textContent")
        item_text = re.sub('\s+', ' ', item_text)
        sanitized_lst.append(item_text)
    print sanitized_lst
    return sanitized_lst
#user_agent = (
#    "Firefox Browser"
#)
def ProductFromAvnet(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )
    productDict = {'Products':[],'price':[]}

    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = user_agent
    headers = {'User-Agent': "Anagha Browser",
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


    #desired_capabilities=dcap,
    #driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path='C:\\Users\\AB\\AppData\\Roaming\\npm\\node_modules\\phantomjs\\lib\\phantom\\bin\\phantomjs.exe') # or add to your PATH
    driver = webdriver.Firefox()
    driver.set_window_size(1024, 768) # optional
    driver.get(url)

    delay = 15 # seconds
    driver.implicitly_wait(10) # seconds
    prod_results = driver.find_element_by_id("prod_results")
    print "Page is ready!"

    product_name_list=[]
    product_names = prod_results.find_elements_by_xpath("//span[@class='blue_clr upper_case_txt bold_txt']/a")
    product_name_list = sanitize(product_names)

    price_list=[]
    price_items = prod_results.find_elements_by_css_selector(".gs_colPrice.Cell")
    price_list = sanitize(price_items)

    lead_time_list =[]
    other_stocks = prod_results.find_elements_by_css_selector("a.blue_clr.posRelOS")
    #print other_stocks
    for other_stock in other_stocks:
        other_stock.click();

    driver.implicitly_wait(10) # seconds
    lead_days = prod_results.find_elements_by_css_selector("li.pdpRightList")
    #print lead_days
    lead_time_list = sanitize(lead_days)

    length_list = [len(product_name_list),len(price_list),len(lead_time_list)]


    product_list = [{'product_name':product_name_list[k],'price':price_list[k],'lead_time':lead_time_list[k]} for k in range(0,min(length_list))]
    print product_list
    driver.close()

    return product_list

url = 'http://products.avnet.com/webapp/wcs/stores/servlet/SearchDisplay?categoryId=&storeId=715839035&catalogId=10001&langId=-1&sType=SimpleSearch&resultCatEntryType=2&searchSource=Q&searchType=100&avnSearchType=all&searchTerm=A1101R04C'
print ProductFromAvnet(url)
