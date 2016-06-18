from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sanitizer
import urllib

def ProductFromFutureElectronics(url):
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
    search_results = driver.find_element_by_id("search-results")
    print "Page is ready!"

    main_product_summaries = search_results.find_elements_by_class_name("product-summary-main")
    row_index = 0
    dict_lst = []
    for main_product_summary in main_product_summaries:
        product_dict = {}
        product_dict['desc'] = sanitizer.sanitize_item(main_product_summary.find_element_by_xpath("//div/div/div[@class='desc']/p"))
        product_dict['manufacturer'] = sanitizer.sanitize_item(main_product_summary.find_element_by_tag_name('h5'))
        product_dict['mrf_part#'] = sanitizer.sanitize_item(main_product_summary.find_element_by_xpath("//div/div/div/p[@class='mfr-results']/a"))
        product_dict['price'] = sanitizer.sanitize_item(main_product_summary.find_element_by_xpath("//div/div/div/p/span[@class='prices-value']"))
        product_dict['stock'] = sanitizer.sanitize_item(main_product_summary.find_element_by_xpath("//div/div/div/p/span[@class='prices-in-stock-value']"))

        try:
            images = main_product_summary.find_element_by_xpath("//div/div/div/div[@class = 'thumbnail']/a/img[@class = 'productThumbnail']")
            src = images.get_attribute('src')
            print src
            file_name =  product_dict['mrf_part#']
            file_name = file_name.replace('\\', '')
            file_name = file_name.replace(':', '')

            urllib.urlretrieve(src, 'images\\future_electronics\\' + file_name + '.png')
        except Exception,e:
            print str(e)
            print "No image found"
        dict_lst.append(product_dict)
    driver.close()
    return dict_lst

url = "http://www.futureelectronics.com/en/Search.aspx?dsNav=Ntk:PartNumberSearch%7cMMSS8050%7c1%7c,Ny:True,Nea:True"
print ProductFromFutureElectronics(url)
