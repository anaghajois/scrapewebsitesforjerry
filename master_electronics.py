from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sanitizer
#user_agent = (
#    "Firefox Browser"
#)
def ProductFromMasterElectronics(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )


    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = user_agent


    #desired_capabilities=dcap,
    driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path='C:\\Users\\AB\\AppData\\Roaming\\npm\\node_modules\\phantomjs\\lib\\phantom\\bin\\phantomjs.exe') # or add to your PATH
    #driver = webdriver.Firefox()
    driver.set_window_size(1024, 768) # optional
    driver.get(url)

    delay = 15 # seconds
    driver.implicitly_wait(10) # seconds
    content = driver.find_element_by_id("ctl00_UpdatePanel1")
    print "Page is ready!"

    table_columns_text_list = []
    result_table = content.find_element_by_id("myTable")
    table_body = result_table.find_element_by_tag_name('tbody')
    table_rows = table_body.find_elements_by_xpath('//tbody/tr[starts-with(@class,"Results")]')
    row_index = 0
    dict_lst = []
    while(row_index < len(table_rows)):
        table_columns = table_rows[row_index].find_elements_by_tag_name('td')
        wanted_column_data = [{'index': 2, 'name': 'part_number'},{'index':3, 'name': 'supplier'},{'index':4, 'name': 'discription'},{'index':5, 'name':'availability'},{'index':6, 'name':'pricing'}]
        wanted_columns = []
        row_data = {}
        for wanted_column in wanted_column_data:
            #print wanted_column['index']
            if wanted_column['index'] == 5:
                column_text = sanitizer.sanitize_item(table_columns[wanted_column['index']].find_element_by_id('avaiablity'))
            else:
                column_text = sanitizer.sanitize_item(table_columns[wanted_column['index']])
            row_data[wanted_column['name']] = column_text

        print row_data
        dict_lst.append(row_data)
        row_index += 1
    driver.close()

url = "http://www.masterelectronics.com/parts.aspx?Text=mmss8050-h-tp&pagenum=3"
ProductFromMasterElectronics(url)
