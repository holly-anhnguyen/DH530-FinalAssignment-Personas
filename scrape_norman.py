from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import requests
import time
import os
import pandas as pd
import csv
import re
from bs4 import BeautifulSoup
from html import unescape
from datetime import datetime
def get_articles_url():
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    articles = []  
    url_list =[]
    page = 1
    while page < 9:
        url ='https://www.nngroup.com/topic/user-testing/?apage='+str(page)+'#articles'
        driver.get(url)         
        tab = driver.find_elements(By.ID,'articlesTabContent')
        titles = tab[0].find_elements(By.CLASS_NAME, 'publication-list-item')        
        for title in titles:       
            name = title.find_elements(By.CSS_SELECTOR,'h2 a')
            url_list.append(name[0].get_attribute('href'))     
        page=page+1    
    return url_list  #This line converts the dictionary object into a pandas DataFrame.    

def get_articles(url_list):
    articles=[]
    for item in url_list:
        print('Process: {}'.format(item))
        r =requests.get(item)
        time.sleep(50)
        soup = BeautifulSoup(r.content,'lxml')      
        full_text=soup.find(id='articleBody').text
        try:
            timestamp=soup.find(id='gaDataPubDate').text
        except:
            timestamp=''    
        articles.append({
            'timestamp': timestamp,
            'content':full_text
        })
    return pd.DataFrame(articles)

def break_file():
    org_file='nielsen_norman_group/user_tesing_articles.csv' 
    for i in range(1993,2023):  
        with open(org_file, mode='r') as infile:
            reader = csv.reader(infile)
            next(reader, None)  
            for row in reader:
                col_date = datetime.strptime(row[1],'%Y-%m-%d').date()
                year =col_date.year                
                split_file='nielsen_norman_group/user_testing/'+str(year)+'.csv'
                if int(year)==i:
                    with open(split_file, 'a+') as outcsv:
                        writer = csv.DictWriter(outcsv,fieldnames = ["Content"])
                        writer.writerow({'Content':row[2]})
break_file()

#This line will open a new chrome window and start the scraping.
# url_list = get_articles_url()
# df=get_articles(url_list)
# #Write a file
# os.makedirs('nielsen_norman_group', exist_ok=True)  
# df.to_csv('nielsen_norman_group/user_tesing_articles.csv')  

