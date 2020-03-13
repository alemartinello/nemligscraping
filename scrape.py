from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime
import csv

with open('nemlig_scraping.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['time', 'number_waiting', 'estimated_time'])

binary = FirefoxBinary(r'C:/Program Files/Mozilla Firefox/firefox.exe') # CHANGE 

run_every = 30 # Set every how many minutes to run
with open('nemlig_scraping.csv','w') as f:
    f.write('time, number_waiting, estimated_time \n')


def collect_info():
    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get('https://nemlig.queue-it.net/?c=nemlig&e=nemligpaaske&t=https%3A%2F%2Fwww.nemlig.com%2F&cid=da-DK&l=nemlig.com')

    delay = 30  # seconds

    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'MainPart_lbWhichIsInText')))
    print("Page is ready!")

    time.sleep(1)
    number_ahead = browser.find_element_by_id("MainPart_lbUsersInLineAheadOfYou").text
    time.sleep(3) # just to be safe
    estimated_wait_time = browser.find_element_by_id("MainPart_lbWhichIsIn").text
    number_ahead = browser.find_element_by_id("MainPart_lbUsersInLineAheadOfYou").text

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{now}: {number_ahead} in line, {estimated_wait_time} estimated wait time')
    
    # Exits the line to leave space to Hamsters
    browser.find_element_by_id('MainPart_aExitLine').click()

    # close the browser
    browser.close()
    return now, number_ahead, estimated_wait_time

if __name__ == "__main__":
    now, number_ahead, estimated_wait_time = collect_info()

    with open('nemlig_scraping.csv', mode='a', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([now, number_ahead, estimated_wait_time])
