# Python 3 example using requests library.
import requests
from urllib import response
from bs4 import BeautifulSoup
import time
import math
from pathlib import Path
import certifi
import urllib3
import requests

count =0
def inc(): 
    global count 
    count += 1

API_URL = "https://api.zyte.com/v1/extract"
API_KEY = "48795bf73f4744428f6d9c99fece3e22"
for page in range(473,491):
    while True:
        try:
            response = requests.post(API_URL, auth=(API_KEY, ''), json={
                "url": "https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/wohnung-kaufen?pagenumber=" + str(page),
                "browserHtml": True
                })
            data = response.json()
            # print(data)
            # print(data['browserHtml'])
            soup = BeautifulSoup(data['browserHtml'], "lxml")
            break
        except KeyError:
            time.sleep(3)
            print("Will try again for page ", str(page))
    # print(soup.prettify())
    for a in soup.find_all('a', attrs = {'data-go-to-expose-referrer':"RESULT_LIST_LISTING"}):
        href = a['href']
        print(href)
        inc()
        with open('Germany/BadenWu.txt', "a") as myfile:
            myfile.write(href + '\n')
    print("Appended all " + str(count) + " to page: " + str(page))
    
myfile.close()