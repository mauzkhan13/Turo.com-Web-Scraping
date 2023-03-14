# Import necessary libraries from Selenium and other libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import random
import pandas as pd
import os
import time
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options

# Set proxy configuration
PROXY = ''
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = PROXY
prox.ssl_proxy = PROXY
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

# Set Chrome options
options = Options()
# Add arguments to Chrome options
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--mute-audio')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')
options.add_argument('--disable-translate')
options.add_argument('--disable-logging')
options.add_argument('--disable-default-apps')
options.add_argument('--disable-background-timer-throttling')
options.add_argument('--disable-backgrounding-occluded-windows')
options.add_argument('--disable-breakpad')
options.add_argument('--disable-component-extensions-with-background-pages')
options.add_argument('--disable-features=TranslateUI')
options.add_argument('--disable-hang-monitor')
options.add_argument('--disable-ipc-flooding-protection')
options.add_argument('--disable-prompt-on-repost')
options.add_argument('--disable-renderer-backgrounding')
options.add_argument('--disable-sync')
options.add_argument('--disable-web-resources')
options.add_argument('--enable-automation')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--log-level=3')
options.add_argument('--test-type=webdriver')
options.add_argument('--user-data-dir=/tmp/user-data')
options.add_argument('--v=99')

# Set the proxy for the ChromeOptions
options.add_argument('--proxy-server={}'.format(PROXY))

# Add experimental options
options.add_experimental_option('prefs', {
    'profile.managed_default_content_settings.images': 2,
    'profile.managed_default_content_settings.stylesheets': 2,
    'profile.managed_default_content_settings.plugins': 2,
    'profile.managed_default_content_settings.popups': 2,
    'profile.managed_default_content_settings.geolocation': 2,
    'profile.managed_default_content_settings.notifications': 2,
    'profile.managed_default_content_settings.automatic_downloads': 1,
    'profile.managed_default_content_settings.fullscreen': 2,
    'profile.managed_default_content_settings.mouselock': 2,
    'profile.managed_default_content_settings.pointerLock': 2,
    'profile.managed_default_content_settings.webusb': 2,
    'profile.managed_default_content_settings.webxr': 2,
    'profile.default_content_setting_values.media_stream_mic': 2,
    'profile.default_content_setting_values.media_stream_camera': 2,
})

# Create new webdriver instance with the specified options and capabilities
driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

# Set URL and navigate to it
url = 'https://turo.com/'
driver.get(url)

#Initialize empty lists to store data

city = []
makes = []
models = []
years = []
trips = []
day_rates = []
total_earnings = []
month = []

# Set the initial scroll height
scroll_height = 0

# Set the scroll pause time
scroll_pause_time = 2

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-1xhwfei-StyledText"]')))
#Set the initial values for the current city and month to empty strings
current_city = ''
current_month = ''
# Loop through the page and extract data from each item
while True:
   #Find all search result items on the page
    my_lists = driver.find_elements(By.XPATH, '//div[@class="searchResult-gridItem"]')
    for lists in my_lists:
        try:
            # Find all text elements within each item
            items = lists.find_elements(By.XPATH, './/div[@class="css-1xhwfei-StyledText"]')
            for item in items:

                # Extract make, model, and year values from current item
                text = item.text
                words = text.split()
                model = words[0]
                year = ' '.join(words[1:-1])
                make = words[-1]

                # Append make, model, and year values to their respective lists
                models.append(model)
                makes.append(make)
                years.append(year)

                # Append current city and month values to their respective lists
                city.append(current_city)
                month.append(current_month)

            # Extract trips, day rates, and total earnings
            trips_ = lists.find_elements(By.XPATH, './/p[@class="css-om0pa0-StyledText"]')
            if trips_:
                for trip in trips_:
                    trips.append(trip.text)
            else:
                trips.append('')

            rates = lists.find_elements(By.XPATH, './/span[@class="css-1y0wisr-StyledText-DailyPrice"]')
            for rate in rates:
                day_rates.append(rate.text)

            earned = lists.find_elements(By.XPATH, './/p[@class="css-a5rkwn-StyledText-StyledTotalPrice"]')
            for earn in earned:
                total_earnings.append(earn.text)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

            # Get the current scroll height
    last_scroll_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the page to load
    time.sleep(scroll_pause_time)

            # Check if the new scroll height is the same as the last scroll height
    new_scroll_height = driver.execute_script("return document.body.scrollHeight")
    if new_scroll_height == last_scroll_height:
        break

    
# Creating a DataFrame with the given data using the zip() function to combine the lists into tuples
# and the pd.DataFrame() function to convert it into a DataFrame object
df = pd.DataFrame((zip(city, makes, models, years, trips, day_rates, total_earnings, month)), 
                  columns=['City','Make','Model','Year','Trips', 'Daily Rates', 'Offers Tittle Earned', 'Month'])

# Assigning a file path to the variable "path"
path = r'C:\my_file.csv'

# Writing the DataFrame to a CSV file using the to_csv() function and specifying the file path
# and setting index to False to not include index in the csv file.
df.to_csv(path, index=False)