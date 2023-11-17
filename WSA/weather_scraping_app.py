# -*- coding: utf-8 -*-
"""
Created on Mon Nov  12 06:06:06 2023

@author: BT

"""

from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta, date
from tqdm import tqdm
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Metoffice forecast does not have all 81 of the Turkey's cities so the dictionary below is adjusted accordingly. 

TR_metoffice = {
    '01': 'adana', '02': 'NaN', '03': 'NaN', '04': 'NaN', '05': 'NaN', '06': 'ankara', '07': 'antalya', '08': 'hopa', '09': 'kusadasi', '10': 'NaN',
    '11': 'NaN', '12': 'NaN', '13': 'NaN', '14': 'bolu', '15': 'NaN', '16': 'bursa', '17': 'canakkale', '18': 'NaN', '19': 'corum', '20': 'NaN', 
    '21': 'diyarbakir', '22': 'edirne', '23': 'NaN', '24': 'NaN', '25': 'erzurum', '26': 'NaN', '27': 'gaziantep', '28': 'giresun', 
    '29': 'gumushane', '30': 'hakkari', '31': 'iskenderun', '32': 'isparta', '33': 'anamur', '34': 'istanbul', '35': 'izmir', '36': 'NaN',
    '37': 'kastamonu', '38': 'kayseri', '39': 'NaN', '40': 'kirsehir', '41': 'darica', '42': 'konya', '43': 'kutahya', '44': 'malatya', '45': 'akhisar',
    '46': 'NaN','47': 'NaN', '48': 'mugla', '49': 'NaN', '50': 'NaN', '51': 'nigde', '52': 'ordu', '53': 'rize', '54': 'NaN',  '55': 'samsun',
    '56': 'NaN', '57': 'sinop', '58': 'sivas', '59': 'tekirdag', '60': 'tokat',
    '61': 'trabzon', '62': 'ovacik', '63': 'NaN', '64': 'usak', '65': 'vantur',
    '66': 'yozgat', '67': 'zonguldak', '68': 'NaN', '69': 'NaN', '70': 'NaN', '71': 'NaN', '72': 'batman', '73': 'sirnak',
    '74': 'NaN','75': 'NaN','76': 'NaN', '77': 'NaN', '78': 'NaN', '79': 'NaN', '80': 'NaN', '81': 'NaN'
}

TR = {
    'adana': '01', 'adiyaman': '02', 'afyonkarahisar': '03', 'agri': '04', 'amasya': '05',
    'ankara': '06', 'antalya': '07', 'artvin': '08', 'aydin': '09', 'balikesir': '10',
    'bilecik': '11', 'bingol': '12', 'bitlis': '13', 'bolu': '14', 'burdur': '15',
    'bursa': '16', 'canakkale': '17', 'cankiri': '18', 'corum': '19', 'denizli': '20',
    'diyarbakir': '21', 'edirne': '22', 'elazig': '23', 'erzincan': '24', 'erzurum': '25',
    'eskisehir': '26', 'gaziantep': '27', 'giresun': '28', 'gumushane': '29', 'hakkari': '30',
    'hatay': '31', 'isparta': '32', 'mersin': '33', 'istanbul': '34', 'izmir': '35',
    'kars': '36', 'kastamonu': '37', 'kayseri': '38', 'kirklareli': '39', 'kirsehir': '40',
    'kocaeli': '41', 'konya': '42', 'kutahya': '43', 'malatya': '44', 'manisa': '45',
    'kahramanmaras': '46', 'mardin': '47', 'mugla': '48', 'mus': '49', 'nevsehir': '50',
    'nigde': '51', 'ordu': '52', 'rize': '53', 'sakarya': '54', 'samsun': '55',
    'siirt': '56', 'sinop': '57', 'sivas': '58', 'tekirdag': '59', 'tokat': '60',
    'trabzon': '61', 'tunceli': '62', 'sanliurfa': '63', 'usak': '64', 'van, van': '65',
    'yozgat': '66', 'zonguldak': '67', 'aksaray': '68', 'bayburt': '69', 'karaman': '70',
    'kirikkale': '71', 'batman': '72', 'sirnak': '73', 'bartin': '74', 'ardahan': '75',
    'igdir': '76', 'yalova': '77', 'karabuk': '78', 'kilis': '79', 'osmaniye': '80',
    'duzce': '81'
}
TR = {v: k for k, v in TR.items()}

# Adjust the dictionary so that keys are plate numbers and values are city names.

def get_weather_weather(city):
    Z = []
    driver = webdriver.Chrome()
    base_url = "https://weather.com/tr-TR"
    driver.get(base_url)
    driver.refresh()
    wait = WebDriverWait(driver, 10)
    # Make a search with the city's name
    search_input = driver.find_element(By.ID, "LocationSearch_input")
    search_input = wait.until(EC.element_to_be_clickable((By.ID, "LocationSearch_input")))
    search_input.click()
    search_input.send_keys(city)
    # Enter city
    time.sleep(2)
    xity = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/header/div/div[2]/div[1]/form/div/div[2]/div[2]/button[1]')
    xity.send_keys(Keys.ENTER)   
    # Select ten days forecasting
    time.sleep(1)
    tendays = driver.find_element(By.XPATH, '//*[@id="WxuLocalsuiteNav-header-71dadf79-621d-43ff-9a1a-d99a39f16abe"]/div/nav/div/div[1]/a[3]')
    tendays.click()
    soup = BeautifulSoup(driver.page_source, "lxml")
    for day in range(0,7):
        if day == 0:
            weather = soup.find_all("details", class_ = "DaypartDetails--DayPartDetail--2XOOV Disclosure--themeList--1Dz21 DaypartDetails--openDisclosure--9wY9b DaypartDetails--openDisclosureDesktop--1FSB5")
            high = weather[day].find("span", class_ = "DetailsSummary--highTempValue--3PjlX").get_text()[0:-1]
            low = float(weather[day].find("span", class_ = "DetailsSummary--lowTempValue--2tesQ").get_text()[0:-1]) 

            if high == "-":  # So in the website, when you try to get the data at night, the today's day temperature is not present
                high = weather[day].find("span", class_ = "DetailsSummary--highTempValue--3PjlX").get_text()[0:-1]
            else:
                high = float(weather[day].find("span", class_ = "DetailsSummary--highTempValue--3PjlX").get_text()[0:-1])

        elif day == 1:
            weather = soup.find_all("details", class_ = "DaypartDetails--DayPartDetail--2XOOV DaypartDetails--enablePreviousBorder--2B1p5 Disclosure--themeList--1Dz21 Disclosure--disableBorder--3Np63")
            high = float(weather[day-1].find("span", class_ = "DetailsSummary--highTempValue--3PjlX").get_text()[0:-1])
            low = float(weather[day-1].find("span", class_ = "DetailsSummary--lowTempValue--2tesQ").get_text()[0:-1])

        else:
            weather = soup.find_all("details", class_ = "DaypartDetails--DayPartDetail--2XOOV Disclosure--themeList--1Dz21")
            high = float(weather[day-2].find("span", class_ = "DetailsSummary--highTempValue--3PjlX").get_text()[0:-1])
            low = float(weather[day-2].find("span", class_ = "DetailsSummary--lowTempValue--2tesQ").get_text()[0:-1])

        Z_day = [high, low]
        Z.append(Z_day)
        
    driver.quit()
    return Z

def get_weather_metoffice(city):  
    X = []
    if city != 'NaN':    
        driver = webdriver.Chrome()
        base_url = "https://www.metoffice.gov.uk/weather/world/turkey/"
        driver.get(base_url)
        search_input = driver.find_element(By.ID, "location-search-input")
        search_input.send_keys(Keys.CONTROL, "a")
        search_input.send_keys(Keys.BACKSPACE)
        search_input.send_keys(city)
        time.sleep(1)
        search_input.send_keys(Keys.RETURN)
        soup = BeautifulSoup(driver.page_source, "lxml")
        for day in range(0,7):
            if day < 6:
                metoffice = soup.find_all("li", class_ = "forecast-tab")
                high = float(metoffice[day].find("span", class_ = "tab-temp-high").get_text()[0:-1])
                low = float(metoffice[day].find("span", class_ = "tab-temp-low").get_text()[0:-1])
                X_day = [high, low]
            else:
                metoffice = soup.find_all("li", class_ = "forecast-tab")     
                high = metoffice[day].find("span", class_ = "tab-temp-high")

                if high is None:
                    X_day = ("NaN","NaN") 

                else:
                    high = float(metoffice[day].find("span", class_ = "tab-temp-high").get_text()[0:-1])
                    low = float(metoffice[day].find("span", class_ = "tab-temp-low").get_text()[0:-1])
                    X_day = [high, low]
            X.append(X_day)
        driver.quit()
    else:
        for day in range(0,7):
            X_day = ["NaN", "NaN"]
            X.append(X_day)
    
    return X

def get_weather_havadurumux(city):
    Y = []
    base_url = "https://www.havadurumux.net/"
    url = f"{base_url}{city.lower()}-hava-durumu/"
    
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"}
    r_havadurumux = requests.get(url, headers = header)
    
    soup = BeautifulSoup(r_havadurumux.content, "lxml")
    havadurumux = soup.find_all("tr")
    # index 2: high
    # index 3: low
    for day in range(0,7):
        high = float(havadurumux[day+1].select("td")[2].get_text()[0:-1])
        low = float(havadurumux[day+1].select("td")[3].get_text()[0:-1])
        Y_day = [high, low]          
        Y.append(Y_day)
    
    return Y

DB = []

def get_weather(plt, cty):

    if cty not in TR_metoffice.values():
        X = get_weather_havadurumux(cty)
        Y = get_weather_metoffice("NaN")
        Z = get_weather_weather(cty)
    else:
        X = get_weather_havadurumux(cty)
        Y = get_weather_metoffice(cty)
        Z = get_weather_weather(cty)
    for day in range(0,7):
        dt = date.today() + timedelta(days = day)
        weatherapp = {
            'provincial_plate': plt,
            'date': datetime.combine(dt, datetime.min.time()),
            'weather': {
                "metoffice": {'up': Y[day][0], 'low': Y[day][1]},
                "weather_com": {'up': Z[day][0], 'low': Z[day][1]},
                "havadurumux": {'up': X[day][0], 'low': X[day][1]},
            }
        }

        DB.append(weatherapp)
    print(f"{cty}({plt}) Saved!")

max_workers = 3 # Adjust the number of workers
max_retries =3 # Adjust the number of max trials in case of an error

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for plt, cty in TR.items():
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Submit the task to the executor
                future = executor.submit(get_weather, plt, cty)
                futures.append(future)
                break
            except Exception as e:
                print(f"An error occurred for: {cty} retrying...")
                retry_count +=1 
    #wait futures to complete
    for future in concurrent.futures.as_completed(futures):
        retry = 0
        while retry < max_retries:
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred retrying...{e}")
                retry += 1
