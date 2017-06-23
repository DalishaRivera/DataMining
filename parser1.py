#Author: Chris T.
#Editor: Dalisha R.
#Date recieved: 06/21/2017
#parser1.py

import re
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from logger import *

# Convenience Aliases
CLASS = By.CLASS_NAME
CSS = By.CSS_SELECTOR
ID = By.ID
TAG = By.TAG_NAME

# Date Parsing
DATE_RE = re.compile('(\d{4})-(\d{2})-(\d{2})')
YEAR_RE = re.compile('(\d{4})')


class Parser(object):
    def __init__(self, service, browser):
        self.service = service
        self.browser = browser
        self.driver = None

    def get_header(self):
        if self.service == 'fedora':
            return ('Crash_ID', 'Frame #', 'Function', 'Binary', 'File', 'Line')     
        else:
            return None

    def parse(self, ID, url):
        debug('Parsing {}'.format(url))
        if self.service == 'fedora':
            return self._parse_fedora(ID, url)

    def setup(self):
        self.driver = self._get_driver(self.browser)

    def teardown(self):
        if self.driver:
            self.driver.close()

    def _get_driver(self, browser):
        driver = None

        if browser == 'chrome':
            driver = webdriver.Chrome()
        else:
            error('Cannot create driver for browser {}'.format(browser))
            sys.exit(1)

        return driver

    def _parse_fedora(self, ID, url):
        _results = list()

        try:
            self.driver.get(url) #getting given URL
            results1 = self.driver.find_element_by_xpath("//table[contains(@class, 'table table-striped table-bordered table-condensed') and not(contains(@class, 'metric'))]")
                #print("Results")
                #print(results)
            first = True    
            for result in results1.find_elements(CSS, 'tr'):
                #print("Result")
                #print(result)
                line = list()
                if (first == False):
                    line.append(ID)        
                for td_result in result.find_elements(CSS,'td'): 
                    if (first == False):
                        line.append(td_result.text)
                        debug(td_result.text)
                        #print(td_result.text)
                first = False    

                if line:
                    #print(line)
                    _results.append(line) 

            print(_results)         

        except WebDriverException:
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)

        return _results

    def _contains(self, element, by, value):
        elements = element.find_elements(by, value)
        return len(elements) > 0
