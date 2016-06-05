from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sanitizer
import urllib

def ProductFromTTI(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )
    driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path='C:\\Users\\AB\\AppData\\Roaming\\npm\\node_modules\\phantomjs\\lib\\phantom\\bin\\phantomjs.exe') # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    driver.get(url)

    delay = 15 # seconds
    driver.implicitly_wait(10) # seconds
    main_content = driver.find_element_by_id("main-content")
    print "Page is ready!"

    table_columns_text_list = []
    result_table = main_content.find_element_by_class_name("results")
    table_rows = result_table.find_elements_by_tag_name('tr')
    row_index = 1
    dict_lst = []
    while(row_index < len(table_rows)):
        table_columns = table_rows[row_index].find_elements_by_tag_name('td')
        wanted_column_data = [{'index': 2, 'name': 'part'},{'index':3, 'name': 'product_discription'},{'index':6, 'name': 'availability'},{'index':9, 'name':'Capacitence'},
        {'index':10, 'name':'case_code_in'},{'index':12, 'name': 'Dielectric'}]
        wanted_columns = []
        row_data = {}

        for wanted_column in wanted_column_data:
            column_text = sanitizer.sanitize_item(table_columns[wanted_column['index']])
            row_data[wanted_column['name']] = column_text
        try:
            images = table_columns[1].find_element_by_tag_name("img")
            src = images.get_attribute('src')
            file_name =  row_data['part'].split()[0]
            file_name = file_name.replace('\\', '')
            file_name = file_name.replace(':', '')
            urllib.urlretrieve(src, 'images\\tti\\' + file_name + '.png')
        except:
            print "No image found"
        dict_lst.append(row_data)
        row_index += 1
    driver.close()
    return dict_lst
url = "http://www.ttiinc.com/page/search_results.html?searchTerms=CDR32BX103BKUS&searchType=s&systemsCatalog=&autoComplete=false&x=14&y=7"
print ProductFromTTI(url)
