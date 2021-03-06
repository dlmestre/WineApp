# -*- coding: utf-8 -*-
import json
import pandas as pd
import lxml
import urllib
from xml.etree import ElementTree as ET
#from .forms import chuncks
from threading import Thread
import threading
from helper import log

def round_price(price):
    if int(price) > 200:
        rest = int(price) % 10
        if rest >= 5 and rest < 8:
            last_digit = 5
        elif rest < 5 :
            last_digit = 0
        else:
            last_digit = 8
        str_price = str(int(price))
        str_price = str_price[:-1] + str(last_digit)
        price = int(str_price)
    return price

def chuncks(l,n):
    avg = len(l)/float(n)
    out = []
    last = 0.0

    while last < len(l):
        out.append(l[int(last):int(last+avg)])
        last += avg
    return out

def chuncks2(l,n):
    #receives a dictionary and breaks the lists for each key into n lists
    for key in l.keys():
        a_list = l[key]
        avg = len(a_list)/float(n)
        out = []
        last = 0.0
        while last < len(a_list):
            out.append(a_list[int(last):int(last+avg)])
            last += avg
        l[key] = out 
    return l

class openAPI:
    def __init__(self,year,mode,wine,size):
        self.password = "cuvees"
        self.year = int(year)
        self.mode = mode
        self.wine = wine
        self.size = size
        self.url = self.getUrl()
    def getUrl(self):
        url_main = r"http://api.wine-searcher.com/wine-select-api.lml?Xkey="
        url_main = url_main + self.password + "&Xkeyword_mode=" + str(self.mode)
        url_main = url_main + "&Xwinename=" + str(self.wine) + "&Xvintage=" + str(self.year) + "&Xbottle_size=" + str(self.size)
        return url_main + "&Xlocation=hong+kong&Xcurrencycode=hkd"
    def getData(self):
        root = ET.parse(urllib.urlopen(self.url)).getroot()
        merchants = []
        prices = []
        bottles = []
        links = []
        for name in root.findall("./wines/wine"):
            for i in name:
                if i.tag == "link":
                    links.append(i.text)
                if i.tag == "merchant":
                    merchants.append(i.text)
                if i.tag == "bottle-size":
                    bottles.append(i.text)
                if i.tag == "price":
                    prices.append(i.text)
        tmp_links = []
        tmp_merchants = []
        tmp_bottles = []
        tmp_prices = []
        for link,merchant,bottle,price in zip(links,merchants,bottles,prices):
            #if bottle == "Bottle":
            try:
                mer_low = merchant.lower()
            except Exception as e:
                log("We have ane error : {0}".format(e))
            if "cuvees.com" not in mer_low and "aberdeen fine wine" not in mer_low and "cuvees fine wines" not in mer_low:
                tmp_links.append(link)
                tmp_merchants.append(merchant)
                tmp_bottles.append(bottle)
                tmp_prices.append(price)
        
        links = tmp_links
        merchantes = tmp_merchants
        bottles = tmp_bottles
        prices = tmp_prices
        try:
            prices = [float(price.replace(",","")) for price in prices]
            min_price = min(prices)
            indexes = [idx for idx,val in enumerate(prices) if val == min_price]
            merchants_min = [merchants[idx] for idx in indexes]
            prices_min = [prices[idx] for idx in indexes]
            bottles_min = [bottles[idx] for idx in indexes]
            links_min = [links[idx] for idx in indexes]
        except Exception as e:
            merchants_min = None 
            prices_min = None
            bottles_min = None 
            links_min = None                 
        return merchants_min, prices_min, bottles_min, links_min

class APIThread:
    def __init__(self,ws_working=True):
        self.ws_working = ws_working
        self.addlock = threading.Lock()
        self.ws_wines = {} #contains all wines that got through the API (merchants_min, prices_min, bottles_min, links_min)
        self.wine_dictionary = {}
        self.wine_dictionary_with_formats = {"b":"750ml","m":"1500ml","h":"375ml"}
    def getDictionary(self):
        return self.wine_dictionary
    def getRecommendedPrice(self,markup_price,ws_price):
        applied_percent = "2%"
        ws_price = float(ws_price)
        es_price_2_percent = ws_price * 0.98
        markup_price = float(markup_price)
        if ws_price < markup_price:
            #price = es_price_2_percent
            price = markup_price
            applied_percent = "None"
        else:
            if es_price_2_percent > markup_price:
                price = es_price_2_percent
            else:
                price = markup_price
                applied_percent = "None"
        #return "{0:.2f}".format(price)
        return round(price),applied_percent
    def getMarginHKD(self,recommended_price,cost):
        #return "{0:.2f}".format(float(recommended_price) - float(cost))
        return round(float(recommended_price) - float(cost))
    def getSell(self,lowest_ws_price,recommended_price):
        if float(lowest_ws_price) > float(recommended_price):
            return "Yes"
        else:
            return "No"
    def getThread(self,dictionary):
        try:
            wines = dictionary["wine"]
            years = dictionary["year"]
            formats = dictionary["format"]
            prices = dictionary["price"]
            negoces = dictionary["negoce"]
            print wines,years
            if not self.ws_working:
                log("not using Wine Search API")
            for i, (wine,year,a_format,price,negoce) in enumerate(zip(wines,years,formats,prices,negoces)):
                if a_format not in self.wine_dictionary_with_formats.keys() or not self.ws_working:
                    merchants_min = ["N/A"]
                    prices_min = ["N/A"]
                    bottles_min = "N/A"
                    links_min = ["N/A"]
                else:
                    unique_wine = wine + " " + a_format
                    if unique_wine not in self.ws_wines.keys():
                        obj_wine = openAPI(year,"A",wine,a_format)
                        merchants_min, prices_min, bottles_min, links_min = obj_wine.getData()
                        with self.addlock:
                            self.ws_wines[unique_wine] = {}
                            self.ws_wines[unique_wine]["merchant min"] = merchants_min
                            self.ws_wines[unique_wine]["prices min"] = prices_min
                            self.ws_wines[unique_wine]["bottles min"] = bottles_min
                            self.ws_wines[unique_wine]["links min"] = links_min
                    else:
                        merchants_min = self.ws_wines[unique_wine]["merchant min"]
                        prices_min = self.ws_wines[unique_wine]["prices min"]
                        bottles_min = self.ws_wines[unique_wine]["bottles min"]
                        links_min = self.ws_wines[unique_wine]["links min"]
                try:
                    if a_format not in self.wine_dictionary_with_formats.keys():
                        wine_format = a_format
                    else:
                        wine_format = self.wine_dictionary_with_formats[a_format]
                except Exception as e:
                    log(e)
                try:
                    string = str(year) + " " + str(wine) + " " + str(wine_format) + " " + str(negoce)
                    if merchants_min and prices_min and bottles_min and links_min:
                        with self.addlock:
                            self.wine_dictionary[string] = {}
                            for key in dictionary.keys():
                                self.wine_dictionary[string][key] = dictionary[key][i]

                            self.wine_dictionary[string]["merchants"] = merchants_min
                            self.wine_dictionary[string]["pricesmin"] = prices_min
                            self.wine_dictionary[string]["bottles"] = bottles_min
                            self.wine_dictionary[string]["links"] = links_min
                            self.wine_dictionary[string]["format"] = wine_format
                            
                            if self.ws_working:

                                if a_format not in self.wine_dictionary_with_formats.keys():
                                    recommendedPrice = "N/A"
                                    marginHKD = "N/A"
                                    sell = "N/A"
                                    applied_percent = "None"
                                else:
                                    markup = self.wine_dictionary[string]["markup prices"]
                                    recommendedPrice,applied_percent = self.getRecommendedPrice(markup,prices_min[0])
                                    recommendedPrice = round_price(float(recommendedPrice))
                                    marginHKD = self.getMarginHKD(recommendedPrice,price)
                                    sell = self.getSell(prices_min[0],recommendedPrice)
                                self.wine_dictionary[string]["recommended"] = recommendedPrice
                                self.wine_dictionary[string]["margin"] = marginHKD
                                self.wine_dictionary[string]["sell"] = sell
                                self.wine_dictionary[string]["cheapest percent"] = applied_percent
                            else:
                                recommendedPrice = self.wine_dictionary[string]["markup prices"]
                                self.wine_dictionary[string]["recommended"] = round_price(float(recommendedPrice))
                                self.wine_dictionary[string]["margin"] = self.getMarginHKD(recommendedPrice,price)
                                self.wine_dictionary[string]["sell"] = "N/A"
                                self.wine_dictionary[string]["cheapest percent"] = "2%"
                except Exception as e:
                    log(e)
        except Exception as e:
            log(e)

def Main(msg):
    log("Acessing apiAccess.py ...")
    log(msg.keys())
    log(set(msg["negoce"]))
    log(len(msg))

    for x,a_format in enumerate(msg["format"]):
        log("Position {0} ; Format {1}".format(x,a_format))
        if a_format == "75cl" or a_format == "750ML" or a_format == "750ml" or a_format == "75" or a_format == "75.0" or a_format == "75,0":
            size = "b"
        elif a_format == "150cl" or a_format == "1500ML" or a_format == "1500ml" or a_format == "150" or a_format == "150.0" or a_format == "150,0":
            size = "m"
        elif a_format == "37.5cl" or a_format == "375ML" or a_format == "375ml" or a_format == "37.5" or a_format == "37,5" or a_format == "37,5cl":
            size = "h"
        else:
            size = a_format
        msg["format"][x] = size

    if len(msg["format"]) < 50:
        n = 1
    else:    
        n = 10        
    log(len(msg))
    l = chuncks2(msg,n)

    new_dictionary = {}

    for key in l.keys():
        for x,a_list in enumerate(l[key]):
            #print x,key,a_list
            if x not in new_dictionary.keys():
                new_dictionary[x] = {}
            new_dictionary[x][key] = a_list

    threads_running = []

    apiThread_obj = APIThread(ws_working=False)
    for key in new_dictionary.keys():
        t = Thread(target=apiThread_obj.getThread,
                   args=(new_dictionary[key],))
        threads_running.append(t)
    for t in threads_running:
        t.start()
    for t in threads_running:
        t.join()
    return apiThread_obj.getDictionary()
