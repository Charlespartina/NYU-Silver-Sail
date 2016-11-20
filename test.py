import os
import threading
import selenium
import sys
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    display = Display(visible=0, size=(800, 800))
    display.start()
    driver = webdriver.Chrome()
    driver.get('http://www.google.com')
    print driver.title
    driver.close()
