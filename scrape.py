from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime
import csv
import os

import seaborn as sns
sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import plot as plot
nb_colors = plot.define_NB_colors()
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates


try:
    f = open("nemlig_scraping.csv")
except IOError:
    print('Record does not exist. Creating new one')
    with open('nemlig_scraping.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['time', 'number_waiting', 'estimated_time'])
finally:
    f.close()

binary = FirefoxBinary(r'C:/Program Files/Mozilla Firefox/firefox.exe') # CHANGE 

run_every = 30 # Set every how many minutes to run


def collect_info():
    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get('https://nemlig.queue-it.net/?c=nemlig&e=nemligpaaske&t=https%3A%2F%2Fwww.nemlig.com%2F&cid=da-DK&l=nemlig.com')

    delay = 30  # seconds
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'MainPart_lbWhichIsInText')))
        print("Page is ready!")

        time.sleep(1)
        number_ahead = browser.find_element_by_id("MainPart_lbUsersInLineAheadOfYou").text
        time.sleep(10) # just to be safe
        estimated_wait_time = browser.find_element_by_id("MainPart_lbWhichIsIn").text
        number_ahead = browser.find_element_by_id("MainPart_lbUsersInLineAheadOfYou").text

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{now}: {number_ahead} in line, {estimated_wait_time} estimated wait time')
        
        # Exits the line to leave space to Hamsters
        browser.find_element_by_id('MainPart_aExitLine').click()
        
        # close the browser
        browser.close()
    except:
        print('No line...')
        now, number_ahead, estimated_wait_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, None
        # close the browser
        browser.close()

    return now, number_ahead, estimated_wait_time


if __name__ == "__main__":
    starttime=time.time()
    while True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': Scraping website...')
        try:
            now, number_ahead, estimated_wait_time = collect_info()
        except:
            print('Something went wrong...')
            now, number_ahead, estimated_wait_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, None

        with open('nemlig_scraping.csv', mode='a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([now, number_ahead, estimated_wait_time])
        
        # Plot figure
        plot.plot_figure()

        # copy files to dropbox for sharing
        os.system(r'copy nemlig_scraping.csv C:\Dropbox\Public')
        os.system(r'copy plot.pdf C:\Dropbox\Public')

        # Wait some minutes
        print(f'Waiting {run_every} minutes...')   
        time.sleep((60.0*run_every) - ((time.time() - starttime) % (60.0*run_every)))

