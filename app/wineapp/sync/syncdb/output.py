# -*- coding: utf-8 -*-
import sys
#sys.path.append('/home/ubuntu/app/wineapp/datadb')
from apiAccess import Main
import pandas as pd
from dbfeeder import updatedb
import datetime,time,os,re
from wineClass import handleNegoce2File,handleDictionary
from helper import log
#from apiAccess import Main

TESTING = False

def check_file(a_file):
    flag = False
    if a_file.endswith("xls"):
        flag = True
    if a_file.endswith("xlsx"):
        flag = True
    return flag

def cleaner(region):
    if type(region) == str:
        region = region.replace("AOC","").replace("BLANC","").replace("ROUGE","").replace("RGE","").strip()
        return region.lower().title()
    else:
        return region

def check(value,prices_list,rates_list):
    for i in range(len(prices_list)):
        if float(value) < float(prices_list[i]):
            if i > 0:
                rate = rates_list[i-1].replace("%","").strip()
                return float(rate)/100.0,rates_list[i-1]
            else:
                rate = rates_list[0].replace("%","").strip()
                return float(rate)/100.0,rates_list[0]
            break
    rate = rates_list[-1].replace("%","").strip()
    return float(rate)/100.0,rates_list[-1]

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

def get_updated_databases(path):
    files = [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and f.endswith("converted.csv")]
    original_files = [a_file.replace("_converted","") for a_file in files]
    for a_file in original_files:
        log("Updating {0}".format(a_file))
        handleDictionary(a_file,True,location=path)
    return files

def test():
    import collections
    log("starting...")
    print
    path = r"/home/ubuntu/app/data2/"
    #files = [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and f.endswith("converted.csv")]
    files = get_updated_databases(path)
    dfs = []
    errors = []
    for a_file in files:
        log(a_file)
        try:
            #dfs.append(pd.read_csv(a_file))      
            msg_obj = handleNegoce2File(a_file,False,location=path)
            msg = msg_obj.getContent()
            df_converted = pd.DataFrame(msg)
            dfs.append(df_converted)
        except Exception as e:
            log(e)
            errors.append((e,a_file))          
    log("")
    log("---------------------------")
    log("tester results:")
    log("Number of dataframes : {0}".format(len(dfs)))
    for a_df in dfs:
        log(a_df.shape)
    final_df = pd.concat(dfs)
    log(len(final_df["negoce"].tolist()))
    log(set(final_df["negoce"].tolist()))
    final_df.to_csv("tester.csv",encoding="utf-8")
    final_df = final_df.where((pd.notnull(final_df)),"N/A")
    log(len(final_df["negoce"].tolist()))
    log(set(final_df["negoce"].tolist()))
    sender = final_df.to_dict()
    log(len(sender["negoce"]))
    msg = {}
    for key in final_df.columns:
        if "Unnamed" not in key:
            msg[key] = final_df[key].tolist()
    log("msg:")
    log(msg.keys())
    log(collections.Counter(msg["negoce"]))
    log(len(msg["negoce"]))
    log(set(msg["negoce"]))
    for error in errors:
        log(error)
    log(msg)
def run():
    import collections
    log("starting...")
    print
    path = r"/home/ubuntu/app/data2/"
    #files = [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and f.endswith("converted.csv")]
    files = get_updated_databases(path)    

    dfs = []
    for a_file in files:
        try:
            #dfs.append(pd.read_csv(a_file))      
            msg_obj = handleNegoce2File(a_file,False,location=path)
            msg = msg_obj.getContent()
            df_converted = pd.DataFrame(msg)
            dfs.append(df_converted)
        except Exception as e:
            log(e)          

    final_df = pd.concat(dfs)
    final_df = final_df.where((pd.notnull(final_df)),"N/A")

    msg = {}
    for key in final_df.columns:
        if "Unnamed" not in key:
            msg[key] = final_df[key].tolist()
    
    log(collections.Counter(msg["negoce"]))
    log(set(msg["negoce"]))
    dictionary = Main(msg)
    log(dictionary.keys())
    wine_dict = {}
    for each_result in dictionary:
        
        wine = dictionary[each_result]["wine"]
        year = dictionary[each_result]["year"]
        a_format = dictionary[each_result]["format"]
        negoce = dictionary[each_result]["negoce"]

        wine_id = "_".join(wine.split()) + "_" + str(year) + "_" + str(a_format) + "_" + str(negoce)
        if wine_id not in wine_dict.keys():
            wine_dict[wine_id] = {}
            for key in dictionary[each_result].keys():
                if type(dictionary[each_result][key]) == list:
                    wine_dict[wine_id][key] = dictionary[each_result][key][0]
                else:
                    wine_dict[wine_id][key] = dictionary[each_result][key]
        else:
            if dictionary[each_result]["price"] < wine_dict[wine_id]["price"]:
                for key in dictionary[each_result].keys():
                    if type(dictionary[each_result][key]) == list:
                        wine_dict[wine_id][key] = dictionary[each_result][key][0]
                    else:
                        wine_dict[wine_id][key] = dictionary[each_result][key]
    #print wine_dict
  
    table_obj = updatedb()

    table = "merchants_negoces2"
    table_obj.remove(table)

    
    columns = """(wineid, wine, wine_chinese, year, region_english, region_chinese, a_format, negoce_name, price, markup_percentile, markup_price, ws_merchants, ws_price, recommended_price, margin, sell, date, quantity, a_type_english, a_type_chinese, vendor_english, vendor_chinese, rating, growth, country_english, country_chinese, cheapest_percent)"""
    log("inserting data ...")    
    records_inserted = 0
    updated_records = 0
    new_records = 0
    for each_result in wine_dict:
        #print wine_dict[each_result]["negoce"]
        wineid = wine_dict[each_result]["item id"]
        negoce = wine_dict[each_result]["negoce"]
        datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")        
        #todo check if wineid is on DB
        result = table_obj.checkIfExistsTwoFields(table,"wineid",wineid,"negoce_name",negoce)
        if result[0]:
            sell = wine_dict[each_result]["sell"]
            cheapest_percent = result[1]['cheapest_percent']
            if sell == "Yes" and cheapest_percent != "None":
                cheapest_percent = float(cheapest_percent.replace("%",""))
                recommended = float(result[1]['ws_price'])*(100.0 - cheapest_percent)/100.0
                recommended = round_price(recommended)
                margin = round(float(recommended - float(result[1]['price'])))
            else:
                cheapest_percent = wine_dict[each_result]["cheapest percent"]
                recommended = wine_dict[each_result]["recommended"]
                margin = wine_dict[each_result]["margin"]
            quantity = result[1]["quantity"]
            table_obj.editRecordTwoFields(table,"wineid",wineid,"negoce_name",negoce,
                                 ["date","cheapest_percent","recommended_price","margin","quantity"],
                                 datenow,cheapest_percent,recommended,margin,quantity)
            updated_records += 1
            records_inserted += 1
        else:
            wine = wine_dict[each_result]["wine"]
            wine_chinese = wine_dict[each_result]["wine chinese"]
            price = wine_dict[each_result]["price"]
            year = wine_dict[each_result]["year"]
            region_english = wine_dict[each_result]["region english"]
            region_chinese = wine_dict[each_result]["region chinese"]
            a_format = wine_dict[each_result]["format"]
            merchant = wine_dict[each_result]["merchants"]
            price_min = wine_dict[each_result]["pricesmin"]
            markup = wine_dict[each_result]["markup prices"]
            percentile = wine_dict[each_result]["percentiles"]
            negoce = wine_dict[each_result]["negoce"]           
            recommended = wine_dict[each_result]["recommended"] 
            sell = wine_dict[each_result]["sell"]
            margin = wine_dict[each_result]["margin"]
            quantity = wine_dict[each_result]["qty"]
            a_type_english = wine_dict[each_result]["type english"]
            a_type_chinese = wine_dict[each_result]["type chinese"]
            vendor_english = wine_dict[each_result]["vendor english"]
            vendor_chinese = wine_dict[each_result]["vendor chinese"]
            growth = wine_dict[each_result]["growth"]
            rating = wine_dict[each_result]["rating"]
            country_english = wine_dict[each_result]["country english"]
            country_chinese = wine_dict[each_result]["country chinese"]
            cheapest_percent = wine_dict[each_result]["cheapest percent"]

            #datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            table_obj.update(columns,table,wineid,wine,wine_chinese,year,region_english,region_chinese,a_format,negoce,
                             price,percentile,markup,merchant,price_min,recommended,margin,sell,datenow,
                             quantity,a_type_english,a_type_chinese,vendor_english,vendor_chinese,
                             rating,growth,country_english,country_chinese,cheapest_percent)
            records_inserted += 1
            new_records += 1
    log("{0} records inserted on DB".format(records_inserted))
    log("{0} updated records on DB".format(updated_records))
    log("{0} new records inserted on DB".format(new_records))
    return records_inserted


def main():
    init_time = time.time()

    if TESTING:
        test()
    else:
        records = run()

    time_took = time.time() - init_time
    log("It took {0} seconds".format(time_took))

    log("Done")
    return records,time_took
