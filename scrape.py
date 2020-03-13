from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time, datetime

binary = FirefoxBinary(r'C:/Program Files/Mozilla Firefox/firefox.exe') # CHANGE 


if __name__ == "__main__":

    driver = webdriver.Firefox(firefox_binary=binary)

    browser = webdriver.Firefox()
    browser.get('https://nemlig.queue-it.net/?c=nemlig&e=nemligpaaske&t=https%3A%2F%2Fwww.nemlig.com%2F&cid=da-DK&l=nemlig.com')

    delay = 30  # seconds

    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'MainPart_lbWhichIsInText')))
    print("Page is ready!")

    time.sleep(1)
    number_ahead = browser.find_element_by_id("MainPart_lbUsersInLineAheadOfYou").text
    time.sleep(1)
    estimated_wait_time = browser.find_element_by_id("MainPart_lbWhichIsIn").text
    number_ahead = browser.find_element_by_id("MainPart_lbUsersInLineAheadOfYou").text

    now = datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    print(f'{now}: {number_ahead} in line, {estimated_wait_time} estimated wait time')

    # Exits the line to leave space to Hamsters
    browser.find_element_by_id('MainPart_aExitLine').click()
