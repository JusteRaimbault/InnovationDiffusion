from selenium import webdriver
from selenium.webdriver.common import action_chains
import time
import sys


def get_page(url,socks_port,write_to_file,jsrender_delay):
    #driver = webdriver.Firefox()
    profile=webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    #profile.set_preference("network.proxy.socks_port",int(sys.argv[1]))
    profile.set_preference("network.proxy.socks_port",socks_port)
    profile.set_preference("network.proxy.socks_version", 5)
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile)

    #url=open('urls/url').readline()
    #driver.get('http://shiny.parisgeo.cnrs.fr/jsrender')
    driver.get(url)
    
    if write_to_file==True:
        with open('test/landing.html','w') as f1:
            #print(driver.page_source)
            f1.write(driver.page_source)
            f1.close()

    time.sleep(jsrender_delay)

    if write_to_file==True:
        with open('test/descr.html','w') as f2:
            #print(driver.page_source)
            f2.write(driver.page_source)
            f2.close()

    res=str(driver.page_source)

    #driver.get("http://api.ipify.org")
    #print('IP is : '+str(driver.page_source))
    
    driver.close()
    
    return(res)

#driver.close()

#for i in range(20):
#    print(i)
#    driver.get('http://shiny.parisgeo.cnrs.fr/jsrender')
    #element.get_attribute('innerHTML')
    #time.sleep(10)
    #b1 = driver.find_element_by_css_selector("#tab-8338-5")
    #b1=driver.find_elements_by_link_text("link text")[0]
    #b2 =driver.find_elements_by_link_text("link text")[0]
    #print(b1)
    #action_chains.ActionChains(driver).click(b1).perform()
    #time.sleep(5)
    #action_chains.ActionChains(driver).click(b2).perform()
    #time.sleep(5)
    #actions = action_chains.ActionChains(driver)
    #actions.move_to_element(b1)
    #actions.click(b2)
    #actions.perform()
    #time.sleep(10)

    #driver.close()
