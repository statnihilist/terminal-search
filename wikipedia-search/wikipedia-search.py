# This is a simple webscraper to scrap summary of any topic from
# "https://en.wikipedia.org"
#
# Assumptions :
# 1. The search is well-formed i.e. it can be searched directly searched in wikipedia
#    eg. 'harvard university' will work
# 2. Firefox is installed

# importing modules
import urllib3
import certifi
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# opening site in web browser
browser = webdriver.Firefox()
browser.get('https://en.wikipedia.org')

# searching in seach box
elem = browser.find_element_by_name('search')
elem.send_keys('harvard university' + Keys.RETURN)

# to handle loading of new pages in selenium
# through the method of checking staleness of page
# credits: http://www.obeythetestinggoat.com/how- \
# to-get-selenium-to-wait-for-page-load-after-a-click.html
timeout = 30
old_page = browser.find_element_by_tag_name('html')
WebDriverWait(browser, timeout).until(staleness_of(old_page))

# getting the url of the new page
url = browser.current_url

# opening a socket
http = urllib3.PoolManager(
    cert_reqs = 'CERT_REQUIRED',
    ca_certs=certifi.where())
source = http.request('GET', url)

# reading the data in a variable
html = source.data.decode()
soup = BeautifulSoup(html, 'html.parser')

# finding the appropriate section and printing
paras = soup.find_all('p')
req_para = paras[0]
print(req_para.text)
browser.close()
