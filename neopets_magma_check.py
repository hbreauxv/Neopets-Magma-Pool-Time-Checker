#! /usr/bin/env python3

'''
neopets_magma_check.py is a script that will check the neopets magma pool every 5 minutes and log your magma
bath time.  The results of every check are logged with timestamps to magmaLog.txt.  A screenshot will be taken of your
magma bath time when it is detected.
'''

import time
import logging
from selenium import webdriver

# Logging configuration
logging.basicConfig(filename='magmaLog.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Starting Program...')

# Username and Password
user = "yourusernamehere"
password = "yourpasswordhere"

# Chrome webdriver path.  You may need to modify this to match your chrome webdriver path.
driver = webdriver.Chrome(r'your/web/driver/path')
driver.implicitly_wait(1)
driver.set_window_size(1280,800)


def login():
    # Go to the login for Neopets
    driver.get("http://www.neopets.com/login/")

    # Login
    driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td/div[3]/div[4]/form/div/div[1]/div[2]/input').send_keys(user)
    driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td/div[3]/div[4]/form/div/div[2]/div[2]/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td/div[3]/div[4]/form/input[2]').click()
    logging.info('Logged in to Neopets!')

    # Ignore the damn change email reminder, we're going to magma land
    driver.get("http://www.neopets.com/magma/pool.phtml")
    logging.info('Made it to the magma pool. First refresh incoming')


# This is a counter so we can name our screenshots differently.  There has to be a more elegant way to do this.
# Right now, I dont know what the way is.
n = 0


def magma_check():
    global n
    # Save the current text from the guard so we can check for changes
    element = driver.find_element_by_xpath('//*[@id="poolOuter"]')
    guard_text1 = element.text
    # Wait 5 minutes and then refresh the page
    time.sleep(300)
    driver.refresh()
    # Check the guards text again and store it
    element2 = driver.find_element_by_xpath('//*[@id="poolOuter"]')
    guard_text2 = element2.text
    # Compare the text.  If its different, log it.  Other wise, loop again baby
    if guard_text1 == guard_text2:
        logging.info('Guards text is the same.  Waiting 5 minutes, then retrying')
    # Difference detected! Log it and save a screenshot
    else:
        n += 1
        logging.info('Difference detected! Taking screenshot!')
        driver.save_screenshot('difference %s.png' % str(n))


# Getting ready to go.  Calculating the end time of the program.
t_end = time.time() + 60 * 60 * 24
logging.info('All set! Program will run until %s' % t_end)


login()
# Launches magma_check.  Time to wait 24 hours and cross your damn fingers
while time.time() < t_end:
    # Check the pool
    try:
        magma_check()
    # If something goes wrong, just try and login again and go back to the magma pool
    # This exception is broad, which isn't best practice. but.  ¯\_(ツ)_/¯
    except:
        logging.error('Exception occurred, ¯\_(ツ)_/¯.  Logging back in and continuing script.  Yes, this error mess'
                      + "age is terrible and should be improved at a later date")
        login()