from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sanitizer

def ProductFromRutronik(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )

    driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path='C:\\Users\\AB\\AppData\\Roaming\\npm\\node_modules\\phantomjs\\lib\\phantom\\bin\\phantomjs.exe') # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    driver.get(url)

    delay = 15 # seconds
    driver.implicitly_wait(10) # seconds
    main_content = driver.find_element_by_id("maincontent")
    print "Page is ready!"

    rows_list = main_content.find_elements_by_class_name("row")
    dict_lst = []
    product_dict = {}

    for rows in rows_list:
        product_dict['part number'] = sanitizer.sanitize_item(rows.find_element_by_xpath("//div/div/article/div/div[@class='col-md-12 oc_catalog_title']/h1"))
        disc_list= rows.find_elements_by_xpath("//div/div/article/div/div/div[@class='col-xs-12 col-sm-6']")
        for disc in disc_list:
            desc_item = disc.find_element_by_xpath("//span[@itemprop='description']")
            desc_text = sanitizer.sanitize_item(desc_item)

            seller_item = disc.find_element_by_xpath("//div[@class='rutstars']")
            seller_text = sanitizer.sanitize_item(seller_item)

            full_text = sanitizer.sanitize_item(disc)
            full_text = full_text.replace(desc_text, "")
            full_text = full_text.replace(seller_text, "")
            product_dict['Discription'] = full_text
        product_dict['stock'] = sanitizer.sanitize_item(rows.find_element_by_xpath("//div/div[@class='col-md-9 col-xs-12']/div/div/div[@class ='col-xs-10 col-sm-10']"))
        product_dict['price'] = sanitizer.sanitize_item(rows.find_element_by_xpath("//div/div[@class='col-md-3 col-xs-7']/table[@class ='table table-condensed occalc_pa_table']"))
        product_dict['Lead time'] = sanitizer.sanitize_item(rows.find_element_by_xpath("//div/div/dl[2]/dd[@class='col-xs-6 parameter text-nowrap'][4]"))
        
    dict_lst.append(product_dict)

    driver.close()
    return dict_lst
url = "https://www.rutronik24.com/product/vishay/ay2222m35y5us63l7/5953037.html"
print ProductFromRutronik(url)
