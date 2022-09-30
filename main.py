from urllib import response
from bs4 import BeautifulSoup
import time
import math
from pathlib import Path
import certifi
import urllib3
import re
import requests
from urllib3 import ProxyManager, make_headers
from urllib.request import Request, urlopen
import mysql.connector
from urllib.parse import urlparse
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import concurrent.futures
import random
from requests.auth import HTTPProxyAuth
import pyjson5
from datetime import datetime


from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
ua = UserAgent()
chrome_ua = ua.google

# MYSQL CONNECTION PARAMS
cnx = mysql.connector.connect(host='localhost', user='python', password='password',database='immoscoutdedb')
cursor = cnx.cursor(buffered=True)
start = time.time()


session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=8))
session.mount("http://", HTTPAdapter(max_retries=8))
count = 0
def status(str):
    print(str)

def inc(): 
    global count 
    count += 1

global cursor_count 

pcount = 0
good_proxies = []

def clear_txt():
    f = open('response.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f = open('good2.txt', 'r+')
    f.truncate(0) # need '0' when using r+
   
def clear_states():
    f = open('/home/compscript/Aarau.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f = open('/home/compscript/Bern.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f = open('/home/compscript/Lucerne.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f = open('/home/compscript/Zug.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f = open('/home/compscript/Zurich.txt', 'r+')
    f.truncate(0) # need '0' when using r+

def proxies_list():
    headers={'User-Agent': ua.chrome}
    response = requests.get('https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt', headers=headers)
    with open("response.txt", "w") as f:
        f.write(response.text)
        f.close()

def proxies_arr():
    proxies_arr = []
    with open('response.txt', 'r') as reader:
        for line in reader.readlines():
            # print(line, end='')
            proxies_arr.append(line.strip())
    return proxies_arr

# #get the list of free proxies
# def getProxies():
#     r = requests.get('https://free-proxy-list.net/')
#     soup = BeautifulSoup(r.content, 'html.parser')
#     table = soup.find('tbody')
#     proxies = []
#     for row in table:
#         if row.find_all('td')[4].text =='elite proxy':
#             proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
#             proxies.append(proxy)
#         else:
#             pass
#     return proxies

def extract(proxy):
    global pcount
    headers={'User-Agent': ua.google}
    proxies={
            "http": proxy,
            "https": proxy,
        }
    # auth = HTTPProxyAuth("ahmdevnb", "d6n2kw7b9l03")
    # while True:
    try:
        r = requests.get('https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?enteredFrom=one_step_search', proxies=proxies, headers=headers, timeout=2)
        if(r.status_code == 200):
            pcount = pcount + 1
            print(pcount, " ", proxy, " is working ", r.status_code)
            with open("good2.txt", "a") as myfile:
                myfile.write(proxy)
                myfile.write('\n')
                myfile.close()
            good_proxies.append(proxy)
    except requests.exceptions.ProxyError:
        pass
    
    return proxy





def getAllBuyProperties():
    # proxy = proxy + '/'
    status("GETTING RENT PROPERTIES....")
    ids = []
    time.sleep(2)
    API_URL = "https://api.zyte.com/v1/extract"
    API_KEY = "48795bf73f4744428f6d9c99fece3e22"

    response = requests.post(API_URL, auth=(API_KEY, ''), json={
        "url": 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?enteredFrom=one_step_search',
        "browserHtml": True
        })
    data = response.json()
    print(data)
# data['browserHtml'] contains HTML of a web page.
    
    # soup = BeautifulSoup(response.text, 'lxml')
    # div = soup.findAll('button',attrs = {'class':'result-list-entry__map-link'})
    # for x in div:
    #     print(x.text)
    # j = json.loads(div.text)
    # title = j["props"]["pageProps"]["pageTitle"]
    # translated = GoogleTranslator(source='de', target='en').translate(text=title)
    # state = translated.split()[-1]
    # print(state)
    # file = '/home/compscript/' + state + ".txt"
    # ids = j["props"]["pageProps"]["initialResultData"]["adIds"]

    # with open(file, "w") as  f:
    #     for line in ids:
    #         f.write(str(line) + "\n") 
    # print("successful written to the file ", file)
    # f.close()
            

def getTimeRange(lines):
    arr = []
    dt = datetime.now()
    day = dt.isoweekday()
    count = math.ceil(lines / 168)
    print(count)
    timestamp = time.strftime('%H');
    hour = int(timestamp) + ((day - 1) * 24)
    arr = [count * hour,count * (hour + 1)]
    return arr



def readFile(file):
    with open(file, 'r') as f:
        arr = f.readlines()
        lines = len(arr)
        lines_range = getTimeRange(lines)
        print(lines_range)
        data = arr[lines_range[0]:lines_range[1]]
        # data = arr[300:321]
       
    f.close()
    return data

def unique(file):
    uniqlines = set(open(file).readlines())
    bar = open(file, 'w').writelines(uniqlines)
    print("successful")
    urls = list()
    with open(file) as f:
        while (line := f.readline().rstrip()):
            urls.append(line)
    start = 'https://www.immobilienscout24.de'
    end = '#/'
    new = [start + str(x) + end for x in urls]
    with open(file, "w") as outfile:
        outfile.write("\n".join(new))
    print("done")

def loadData(propertylink, title, cursor_count, address):
    country = "Germany"
    section = "Buy"
    typeProp = 'Apartment Buy'
    f = open('/home/immodework/data.json')
    data = json.load(f)
    state = data["obj_regio1"]
    try:
        livingSpace = data["obj_livingSpace"]
    except KeyError:
        livingSpace = ''  
    try:  
        numRooms = data["obj_noRooms"]
    except KeyError:
        numRooms = '' 
    try:
        price = data["obj_purchasePrice"]
    except KeyError:
        price = '' 
    try:
        numFloors = data["obj_numberOfFloors"]
    except KeyError:
        numFloors = ''
    try:
        yearConstructed = data["obj_yearConstructed"]
    except KeyError:
        yearConstructed = ''
    f = open('/home/immodework/data2.json')
    data = json.load(f)
    city = data["city"]
    f = open('/home/immodework/data3.json')
    data = json.load(f)
    try:
        listing_person_utf = data["contactPerson"]["salutationAndTitle"] + ' ' + data["contactPerson"]["firstName"]  + ' ' +  data["contactPerson"]["lastName"]
        listing_person = listing_person_utf
    except KeyError:
        listing_person = ''
    try:
        listing_contact = data["phoneNumbers"]["phoneNumber"]["contactNumber"]
    except KeyError:
        listing_contact = ''
    sql = 'INSERT INTO properties(country, section, typeProp, state, livingSpace, numRooms, price, numFloors, yearConstructed, city, listing_person, listing_contact, propertylink, title, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    sql_vals =  (country, section, typeProp, state, livingSpace, numRooms, price, numFloors, yearConstructed, city, listing_person, listing_contact, propertylink, title, address)

    cursor.execute(sql, sql_vals)
    cnx.commit()
    cursor_count = cursor_count + cursor.rowcount
    print("affected rows = " + str(cursor.rowcount))


def saveData(file):
    cursor_count = 0 
    ids = readFile(file)
    print("SAVING DATA FOR ", Path(file).stem)
    for id in ids:
        new_id = str(id).strip()
        print(new_id)
        vals = (new_id,)
        cursor.execute('SELECT propertylink FROM properties WHERE propertylink = %s', vals)
        cnx.commit()
        newcount = cursor.rowcount
        if(newcount == 0):
            time.sleep(1)
            API_URL = "https://api.zyte.com/v1/extract"
            API_KEY = "48795bf73f4744428f6d9c99fece3e22"
            while True:
                try:
                    response = requests.post(API_URL, auth=(API_KEY, ''), json={
                        "url": new_id,
                        "browserHtml": True
                        })
                    data = response.json()
                    soup = BeautifulSoup(data['browserHtml'], "html.parser")
                    break
                except KeyError:
                    time.sleep(3)
                    print("Will try again for page ")
            title = soup.find('title').text
            address_full = soup.find('span', attrs={'class':'zip-region-and-country'}).text
            print(address_full)
            patternKeyValues = re.compile(r'var keyValues = .*};$', re.MULTILINE)
            patternAddress = re.compile(r'.+locationAddress: {(\n.*)+\"\n.+}\n.+$', re.MULTILINE)
            patternContactdata = re.compile(r' .+contactData: {.*},$', re.MULTILINE)
            script1 = soup.find("script", text=patternKeyValues)
            keyvalues = patternKeyValues.search(script1.text).group(0)
            keyvalues_b = keyvalues.strip()
            keyvalues_r = keyvalues_b.rstrip(";")
            keyvalues_l = keyvalues_r.lstrip("var keyValues = ")
            with open('/home/immodework/data.json', 'w') as f:
                json.dump(json.loads(keyvalues_l), f)
            # print("successful key values")

            script2 = soup.find("script", text=patternAddress)
            address = patternAddress.search(script2.text).group(0)
            address_b = address.strip()
            address_r = address_b.rstrip(",")
            address_l = address_r.lstrip("locationAddress: ")
            la = address_l.replace('undefined', 'null')
            py_obj = pyjson5.loads(la)
            with open('/home/immodework/data2.json', 'w') as f:
                json.dump(py_obj, f)
            # print("successful address")

            script3 = soup.find("script", text=patternContactdata)
            contact = patternContactdata.search(script3.text).group(0)
            contact_b = contact.strip()
            contact_r = contact_b.rstrip(",")
            contact_l = contact_r.lstrip("contactData: ")

            with open('/home/immodework/data3.json', 'w') as f:
                json.dump(json.loads(contact_l), f)
            print("successful search")

            loadData(new_id, title, cursor_count, address_full)
        else:
            print("Already in Database")

    print("No of rows affected = ", cursor_count)



                


# print(save_proxies)
start = time.time()
# readFile('Germany/BadenWu.txt')

# clear_states()
# getAllBuyProperties()
# clear_txt()

# proxies_list()
# proxylist = proxies_arr()

# saveData()
# # print(test())
# with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(extract, proxylist)
# proxies = [*set(good_proxies)]
# print(len(proxies), " are working well")
# proxy = random.choice(proxies)
# hr = time.strftime('%H')
# clear_states()
# getAllBuyProperties()
# saveData("/home/compscript/Zurich.txt")
# saveData("/home/compscript/Lucerne.txt")
# saveData("/home/compscript/Aarau.txt")
# saveData("/home/compscript/Bern.txt")
# saveData("/home/compscript/Zug.txt")
# loadData("propertylink", "title", 0)
saveData('/home/immodework/Germany/BadenWu.txt')
# append()
cursor.close()
end = time.time()

print(end - start)