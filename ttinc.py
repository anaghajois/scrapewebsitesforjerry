from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sanitizer
import time

def GetMoreInfo(partdetail):
    table_body = partdetail.find_element_by_xpath("//div/table[@id='prodDetailTbl']/tbody")
    table_rows = table_body.find_elements_by_xpath("//tr")
    table_columns = table_rows[1].find_elements_by_tag_name('td')

    part_details_table = table_body.find_element_by_tag_name('table')
    part_details_table_rows = part_details_table.find_elements_by_tag_name('tr')
    part_details_table_rows = part_details_table_rows[:4]
    part_details_rows_text = sanitizer.sanitize_item_list(part_details_table_rows)

    part_details_text = ','.join(part_details_rows_text)
    avail_col = table_body.find_element_by_id('colAvailability')
    avail_rows = avail_col.find_elements_by_tag_name('tr')

    availability = sanitizer.sanitize_item(avail_rows[0])
    lead_time = sanitizer.sanitize_item(avail_rows[3])

    try:
        images = table_columns[1].find_element_by_tag_name("img")
        src = images.get_attribute('src')
        file_name =  row_data['part'].split()[0]
        file_name = file_name.replace('\\', '')
        file_name = file_name.replace(':', '')
        urllib.urlretrieve(src, 'tti\\' + file_name + '.png')
    except:
        print "No image found"

    return {'part_details':part_details_text, 'availability':availability, 'lead_time':lead_time}

def ProductFromTTINC(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )

    #driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path='C:\\Users\\AB\\AppData\\Roaming\\npm\\node_modules\\phantomjs\\lib\\phantom\\bin\\phantomjs.exe') # or add to your PATH
    driver = webdriver.Firefox()
    driver.set_window_size(1024, 768) # optional
    driver.get(url)

    delay = 15 # seconds
    driver.implicitly_wait(10) # seconds
    main_content = driver.find_element_by_id("main-content")
    print "Page is ready!"

    result_table = main_content.find_element_by_class_name("results")
    table_rows = result_table.find_elements_by_tag_name('tr')
    row_index = 1
    dict_lst = []
    while(row_index < len(table_rows)):
        table_columns = table_rows[row_index].find_elements_by_tag_name('td')
        wanted_column_data = [{'index': 2, 'name': 'part'}]
        wanted_columns = []
        row_data = {}
        for wanted_column in wanted_column_data:
            table_columns[wanted_column['index']].find_element_by_tag_name('a').click() #.get_attribute('href')
            domain_name = 'http://www.ttiinc.com'
            driver.implicitly_wait(10) # seconds
            part_detail = driver.find_element_by_id("partdetail")
            row_data = GetMoreInfo(part_detail)
            dict_lst.append(row_data)
            driver.execute_script("window.history.go(-1)")
            driver.implicitly_wait(10)
            main_content = driver.find_element_by_id("main-content")
            result_table = main_content.find_element_by_class_name("results")
            table_rows = result_table.find_elements_by_tag_name('tr')

        row_index += 1
    driver.close()
    return dict_lst

url ="http://www.ttiinc.com/page/search_results.html?s=729090318_43"
print ProductFromTTINC(url)
