from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sanitizer

def ProductFromArrow(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )
    driver = webdriver.Firefox()
    #driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path='C:\\Users\\AB\\AppData\\Roaming\\npm\\node_modules\\phantomjs\\lib\\phantom\\bin\\phantomjs.exe') # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    driver.get(url)

    delay = 15 # seconds
    driver.implicitly_wait(10) # seconds
    search_list_view = driver.find_element_by_id("searchListView")
    print "Page is ready!"

    table_rows = search_list_view.find_elements_by_xpath('//table/tbody/tr[starts-with(@id,"item")]')
    row_index = 0
    dict_lst = []
    while(row_index < 5):
        table_columns = table_rows[row_index].find_elements_by_tag_name('td')
        wanted_column_data = [{'index': 0, 'name': 'part number'},{'index':1, 'name': 'price'},{'index':2, 'name': 'stock'},{'index':3, 'name':'Manufacture'},
        {'index':4, 'name': 'Type'},{'index':6, 'name': 'Discription'}]
        wanted_columns = []
        row_data = {}
        for wanted_column in wanted_column_data:
            column_text = sanitizer.sanitize_item(table_columns[wanted_column['index']])
            row_data[wanted_column['name']] = column_text

        #print row_data
        dict_lst.append(row_data)
        row_index += 1

    driver.close()
    return dict_lst
url = "https://www.arrow.com/en/products/search?q=CDR32BX103BKUS"
print ProductFromArrow(url)
