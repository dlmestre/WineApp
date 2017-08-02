from keys_script import negoces_dictionary,wines_dictionary
import pandas as pd
import re,os,datetime,difflib,unidecode
from dbfeeder import updatedb
from helper import log

def getCostsAndMarkup(table_obj):
    costs_table = 'costs_costs'
    markup_table = 'costs_markup'

    unit_costs = table_obj.getValues("value",costs_table)
    unit_costs_type = table_obj.getValues("valuetype",costs_table)

    fixed_markup = table_obj.getValues("value",markup_table)

    costs_dictionary = {}
    costs_dictionary["%"] = []
    costs_dictionary["HK$"] = []
    for unit_cost,unit_cost_type in zip(unit_costs,unit_costs_type):
        if unit_cost_type == "%":
            costs_dictionary["%"].append(unit_cost)
        elif unit_cost_type == "HK$":
            costs_dictionary["HK$"].append(unit_cost)
    return costs_dictionary,fixed_markup[0]

def check_price(price):
    flag = False
    try:
        float(price)
        flag = True
    except Exception as e:
        pass
    return flag

def check(value,prices_list,rates_list):
    prices_list = list(prices_list)
    rates_list = list(rates_list)
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

def check_template_file(a_file):
    flag = False
    if a_file.endswith("xls"):
        flag = True
    if a_file.endswith("xlsx"):
        flag = True
    return flag
    
class handleNegoceFile:
    def __init__(self,path,production_env,location='/home/ubuntu/app/data/',negoces=negoces_dictionary):
        self.path = path
        self.production_env = production_env
        self.location = location
        self.negoces = negoces
        self.negoce = None
        self.checkName()
        self.getCSV()
        self.getData()
    def checkName(self):
        print self.path
        self.filename = self.path.split("/")[-1].split(".")[0]
        filename_words = self.filename.split()
        self.filename_words = [word.lower() for word in filename_words]
        print self.filename_words
        if "ballande" in self.filename_words:
            self.negoce = "ballande"
        elif "diva" in self.filename_words:
            self.negoce = "diva"
        elif "dubos" in self.filename_words:
            self.negoce = "dubos"
        elif "twins" in self.filename_words:
            self.negoce = "twins"
        elif "rca" in self.filename_words:
            self.negoce = "rca"
        elif "joanne" in self.filename_words:
            self.negoce = "joanne"
        print self.negoce
    def isnan(self,value):
        try:
            return math.isnan(float(value))
        except Exception as e:
            return False
    def getCSV(self):
        if self.negoce and "eur" not in self.filename_words:
            df_xls = pd.read_excel(self.path)
            new_path = self.location+self.filename+".csv"
            print new_path
            df_xls.to_csv(new_path,encoding="utf-8")
            self.df = pd.read_csv(new_path)
        else:
            try:
                print "template file"
                print self.path
                if check_template_file(self.path):
                    df_xls = pd.read_excel(self.path)
                    new_path = self.location+self.filename+".csv"
                    print new_path
                    df_xls.to_csv(new_path,encoding="utf-8")
                    self.df = pd.read_csv(new_path)
                else:
                    df_csv = pd.read_csv(self.path)
                    new_path = self.location+self.filename+".csv"
                    print new_path
                    df_csv.to_csv(new_path,encoding="utf-8")
                    self.df = pd.read_csv(new_path,encoding="utf-8")
            except Exception as e:
                print e
    def cleaner(self,region):
        if type(region) == str:
            region = region.replace("AOC","").replace("BLANC","").replace("ROUGE","").replace("RGE","").strip()
            return region.lower().title()
        else:
            return region
    def getData(self):
        self.msg = {}
        if self.production_env:
            markup_prices = markup.objects.order_by().values_list("price",flat=True)
            markups = markup.objects.order_by().values_list("mark",flat=True)
            try:
                if self.negoces[self.negoce]["currency"] == "euro":
                    pair_rate = eurhkd.objects.latest("value").value
                if self.negoces[self.negoce]["currency"] == "dollar":
                    pair_rate = usdhkd.objects.latest("value").value
            except Exception as e:
                print e
                if "eur" in self.filename_words:
                    pair_rate = eurhkd.objects.latest("value").value
        else:
            table_obj = updatedb()
            table = "datadb_markup"
            markup_prices = table_obj.getValues("price",table)
            markups = table_obj.getValues("mark",table)
            if self.negoce:
                if self.negoces[self.negoce]["currency"] == "euro":
                    table = "datadb_eurhkd"
                    pair_rate = table_obj.getPrice(table)
                if self.negoces[self.negoce]["currency"] == "dollar":
                    table = "datadb_usdhkd"
                    pair_rate = table_obj.getPrice(table)
        if self.negoce and "eur" not in self.filename_words:
            print "a case"
            self.df.columns = self.negoces[self.negoce]["column"]
            wines = self.df[self.negoces[self.negoce]["wine"]]
            prices = []
            for price in self.df[self.negoces[self.negoce]["price"]].tolist():
                try:
                    hkdprice = "{0:.2f}".format(float(price)*float(pair_rate))
                    prices.append(hkdprice)
                except Exception as e:
                    prices.append(price)  
            years = self.df[self.negoces[self.negoce]["year"]]
            regions = self.df[self.negoces[self.negoce]["region"]]
            regions = [self.cleaner(region) for region in regions]
            formats = []
            for content in self.df[self.negoces[self.negoce]["format"]].tolist():
                try:
                    if self.isnan(content):
                        formats.append("75cl")
                    else:
                        formats.append(wines_dictionary[str(content).lower()])
                except Exception as e:
                    formats.append(content)

            all_years = []    
            all_wines = []
            all_prices = []
            all_regions = []
            all_formats = []

            for wine,price,year,region,a_format in zip(wines,prices,years,regions,formats):
                is_price_valid = check_price(price)
                try:
                    match = re.search('\d{4}',str(year))
                    year = match.group(0)
                except Exception as e:
                    year = None
                if year and is_price_valid:
                    all_wines.append(wine)
                    all_prices.append(price)
                    all_years.append(year)
                    all_regions.append(region)
                    all_formats.append(a_format)
            print len(all_prices)
            self.msg["quantities"] = ["0"] * len(all_prices)
            self.msg["negoces"] = [self.negoce.title()] * len(all_prices)
            self.msg["types"] = [""] * len(all_prices)
            self.msg["vendors"] = [""] * len(all_prices)
        else:
            all_wines = self.df["Wine"].tolist()
            all_prices = self.df["Cost"].tolist()
            all_years = self.df["Vintage"].tolist()
            all_regions = self.df["Region"].tolist()
            all_formats = [str(item) for item in self.df["Format"].tolist()]
            self.msg["quantities"] = self.df["Qty"].tolist()
            self.msg["negoces"] = self.df["Negoce"].tolist()
            print set(self.df["Negoce"].tolist())
            try:
                self.msg["types"] = self.df["Type"].tolist()
                self.msg["vendors"] = self.df["Vendor"].tolist()
            except Exception as e:
                print e
                self.msg["types"] = [""] * len(all_prices)
                self.msg["vendors"] = [""] * len(all_prices)
        if "eur" in self.filename_words in "EUR" in self.filename_words:
            table_obj = updatedb()
            table = "datadb_eurhkd"
            pair_rate = table_obj.getPrice(table)
            #print pair_rate
            prices = []
            for price in all_prices:
                try:
                    hkdprice = "{0:.2f}".format(float(price)*float(pair_rate))
                    prices.append(hkdprice)
                except Exception as e:
                    prices.append(price)
            self.msg["prices"] = prices
        else:
            self.msg["prices"] = all_prices
        self.msg["wines"] = all_wines
        self.msg["years"] = all_years
        self.msg["regions"] = all_regions
        self.msg["formats"] = all_formats
        
        prices_after_markup = []
        percentiles = []
        for price in self.msg["prices"]:
            try:
                #check(value,prices_list,rates_list)
                markup_rate,percentile = check(price,markup_prices,markups)
                price_after_markup = float(price) * (1 + markup_rate)
                price_after_markup = "{0:.2f}".format(price_after_markup)
                prices_after_markup.append(price_after_markup)
                percentiles.append(percentile)
            except Exception as e:
                print e
        self.msg["markup prices"] = prices_after_markup
        self.msg["percentiles"] = percentiles
        
    def getContent(self):
        return self.msg

class handleNegoce2File:
    def __init__(self,path,production_env,location='/home/ubuntu/app/data2/'):
        self.path = path
        self.production_env = production_env
        self.location = location
        self.checkName()
        self.getCSV()
        self.getData()
    def checkName(self):
        log("File : {0}".format(self.path))
        self.filename = self.path.split("/")[-1].split(".")[0]
        self.filename_words = self.filename.split()
    def isnan(self,value):
        try:
            return math.isnan(float(value))
        except Exception as e:
            return False
    def getCSV(self):
        try:
            log("checking file format ...")
            if check_template_file(self.path):
                df_xls = pd.read_excel(self.path)
                new_path = self.location+self.filename+".csv"
                log(new_path)
                df_xls.to_csv(new_path,encoding="utf-8")
                self.df = pd.read_csv(new_path)
            else:
                df_csv = pd.read_csv(self.path)
                new_path = self.location+self.filename+".csv"
                log(new_path)
                df_csv.to_csv(new_path,encoding="utf-8")
                self.df = pd.read_csv(new_path,encoding="utf-8")
        except Exception as e:
            log(e)
    def cleaner(self,region):
        if type(region) == str:
            region = region.replace("AOC","").replace("BLANC","").replace("ROUGE","").replace("RGE","").strip()
            return region.lower().title()
        else:
            return region
    def getListOfPrices(self,pair_rate,all_prices):
        prices = []
        for price in all_prices:
            try:
                hkdprice = "{0:.2f}".format(float(price)*float(pair_rate))
                prices.append(hkdprice)
            except Exception as e:
                prices.append(price)
        return prices
    def getData(self):
        self.msg = {}
        if self.production_env:
            pass         
        else:
            table_obj = updatedb()
            #table = "datadb_markup"
            #markup_prices = table_obj.getValues("price",table)
            #markups = table_obj.getValues("mark",table)
            costs_dictionary,fixed_markup = getCostsAndMarkup(table_obj)
        wines_dict = self.df.to_dict()

        for key in wines_dict.keys():
            if "Unnamed" not in key:
                self.msg[key.encode("utf-8")] = [wines_dict[key][item] for item in wines_dict[key].keys()]
        all_prices = self.msg["price"]
        if "eur" in self.filename_words or "EUR" in self.filename_words:
            table_obj = updatedb()
            table = "datadb_eurhkd"
            pair_rate = table_obj.getPrice(table)
            log("Pair rate for EUR : {0}".format(pair_rate))
            self.msg["price"] = self.getListOfPrices(pair_rate,all_prices)
        elif "usd" in self.filename_words or "USD" in self.filename_words:
            table_obj = updatedb()
            table = "datadb_usdhkd"
            pair_rate = table_obj.getPrice(table)
            log("Pair rate for USD : {0}".format(pair_rate))
            self.msg["price"] = self.getListOfPrices(pair_rate,all_prices)
        elif "gbp" in self.filename_words or "GBP" in self.filename_words:
            table_obj = updatedb()
            table = "datadb_gbphkd"
            pair_rate = table_obj.getPrice(table)
            log("Pair rate for GBP : {0}".format(pair_rate))
            self.msg["price"] = self.getListOfPrices(pair_rate,all_prices)
        else:
            self.msg["price"] = all_prices
        
        prices_after_markup = []
        percentiles = []
        #for price in self.msg["price"]:
        #    try:
        #        #check(value,prices_list,rates_list)
        #        markup_rate,percentile = check(price,markup_prices,markups)
        #        price_after_markup = float(price) * (1 + markup_rate)
        #        price_after_markup = "{0:.2f}".format(price_after_markup)
        #        prices_after_markup.append(price_after_markup)
        #        percentiles.append(percentile)
        #    except Exception as e:
        #        log(e)
        for price in self.msg["price"]:
            try:
                for unit_cost in costs_dictionary["HK$"]:
                    price = float(price) + float(unit_cost.replace("HK$",""))
                price_after_markup = float(price) * (1 + float(fixed_markup.replace("%",""))/100.0)
                
                percent = 0
                for unit_cost in costs_dictionary["%"]:
                    percent += float(unit_cost.replace("%",""))/100.0
                price_after_markup = float(price_after_markup) / (1.0 - percent)

                price_after_markup = "{0:.2f}".format(price_after_markup)
                prices_after_markup.append(price_after_markup)
                percentiles.append(fixed_markup)
            except Exception as e:
                log(e)
        self.msg["markup prices"] = prices_after_markup
        self.msg["percentiles"] = percentiles
        
    def getContent(self):
        return self.msg

class handleDictionary:
    def __init__(self,path,is_negoce,location='/home/ubuntu/app/data2/'):
        self.path = path
        self.location = location
        self.is_negoce = is_negoce
        self.found_wines = []
        self.not_found_wines = []
        self.getStart()
    def getStart(self):
        if not self.is_negoce:
            df_xls = pd.read_excel(self.path)
            df_xls.to_csv(os.path.join(self.location,"dictionary.csv"),encoding="utf-8")
            self.getDictionary()
        else:
            self.convertedfilename = self.path.split("/")[-1].split(".")[0]
            self.convertedfilename = self.location + self.convertedfilename + "_converted.csv"
            print self.convertedfilename
            self.match_wines = {}
            self.getDictionary()
            self.getCSV()
    def getDictionary(self):
        df_dictionary = pd.read_csv(os.path.join(self.location,"dictionary.csv"))
        df_dictionary = df_dictionary.dropna(subset=["Item ID"],how="all")
        self.wines_ids = df_dictionary["Item ID"].tolist()
        self.growth_dictionary = df_dictionary["Growth"].tolist()
        self.type_english = df_dictionary["Type (English)"].tolist()
        self.type_chinese = df_dictionary["Type (Chinese)"].tolist()
        self.vendor_english = df_dictionary["Vendor (English)"].tolist()
        self.vendor_chinese = df_dictionary["Vendor (Chinese)"].tolist()
        self.wines_english = df_dictionary["Wine (English)"].tolist()
        self.wines_chinese = df_dictionary["Wine (Chinese)"].tolist()
        self.regions_english = df_dictionary["Region (English)"].tolist()
        self.regions_chinese = df_dictionary["Region (Chinese)"].tolist()
        self.countries_english = df_dictionary["Country (English)"].tolist()
        self.countries_chinese = df_dictionary["Country (Chinese)"].tolist()
        self.ratings = df_dictionary["Ratings"].tolist()
        self.dictionary_content = df_dictionary.to_dict()
    def getCSV(self):
        try:
            self.filename = self.path.split("/")[-1].split(".")[0]
            df_xls = pd.read_excel(self.path)
            new_path = self.location+self.filename+".csv"
            print new_path
            df_xls.to_csv(new_path,encoding="utf-8")
            self.df = pd.read_csv(new_path)
        except Exception:
            self.df = pd.read_csv(self.path)
        
        wines = self.df["Wine"].tolist()
        vintages = self.df["Vintage"].tolist()
        try:
            formats = self.df["Format"].tolist()
        except Exception:
            formats = self.df["Size"].tolist()
        try:
            costs = self.df["Cost"].tolist()
        except Exception:
            costs = self.df["Price"].tolist()
        qtys = self.df["Qty"].tolist()
        negoces = self.df["Negoce"].tolist()
        
        for wine in list(set(wines)):
            self.getSimilar(wine)
        print self.match_wines
        wines_ids_csv = []
        wines_csv = []
        wines_chinese_csv = []
        growth_csv = []
        type_english_csv = []
        type_chinese_csv = []
        vendor_english_csv = []
        vendor_chinese_csv = []
        regions_english_csv = []
        regions_chinese_csv = []
        countries_english_csv = []
        countries_chinese_csv = []
        ratings_csv = []
        vintages_csv = []
        formats_csv = []
        costs_csv = []
        qtys_csv = []
        negoces_csv = []
        for wine,vintage,a_format,cost,qty,negoce in zip(wines,vintages,formats,costs,qtys,negoces):
            try:
                wine_id = self.match_wines[wine]["id"][0]
                print wine_id       
		if (a_format == "75cl" or a_format == "750ML" 
                    or a_format == "750ml" or a_format == "75" 
                    or a_format == "75.0" or a_format == "75,0"
                    or a_format == 75.0):
                    size = "750"
                elif (a_format == "150cl" or a_format == "1500ML" 
                      or a_format == "1500ml" or a_format == "150" 
                      or a_format == "150.0" or a_format == "150,0" 
                      or a_format == 150.0):
                    size = "1500"
                elif (a_format == "37.5cl" or a_format == "375ML" 
                      or a_format == "375ml" or a_format == "37.5" 
                      or a_format == "37,5" or a_format == "37,5cl"
                      or a_format == 37.5):
                    size = "375"
                else:
                    size = a_format
                if type(size) == float:
                    size = str(int(size))
                format_cleaned = re.sub(r'[^\d.]+','',size)
                format_cleaned = "%05d"%(int(format_cleaned))
                wine_id_cleaned = str(self.wines_ids[wine_id].split("-")[0]) + "-" + str(int(vintage)) + "-" + str(format_cleaned)
                wines_csv.append(self.wines_english[wine_id])
                wines_ids_csv.append(wine_id_cleaned)
                wines_chinese_csv.append(self.wines_chinese[wine_id])
                growth_csv.append(self.growth_dictionary[wine_id])
                type_english_csv.append(self.type_english[wine_id])
                type_chinese_csv.append(self.type_chinese[wine_id])
                vendor_english_csv.append(self.vendor_english[wine_id])
                vendor_chinese_csv.append(self.vendor_chinese[wine_id])
                regions_english_csv.append(self.regions_english[wine_id])
                regions_chinese_csv.append(self.regions_chinese[wine_id])
                countries_english_csv.append(self.countries_english[wine_id])
                countries_chinese_csv.append(self.countries_chinese[wine_id])
                ratings_csv.append(self.ratings[wine_id])
                vintages_csv.append(vintage)
                formats_csv.append(a_format)
                costs_csv.append(cost)
                qtys_csv.append(qty)
                negoces_csv.append(negoce)
            except Exception as e:
                print e
        df_csv = pd.DataFrame()
        df_csv["item id"] = wines_ids_csv
        df_csv["wine"] = wines_csv
        df_csv["wine chinese"] = wines_chinese_csv
        df_csv["growth"] = growth_csv
        df_csv["type english"] = type_english_csv
        df_csv["type chinese"] = type_chinese_csv
        df_csv["vendor english"] = vendor_english_csv
        df_csv["vendor chinese"] = vendor_chinese_csv
        df_csv["region english"] = regions_english_csv
        df_csv["region chinese"] = regions_chinese_csv
        df_csv["country english"] = countries_english_csv
        df_csv["country chinese"] = countries_chinese_csv
        df_csv["rating"] = ratings_csv
        df_csv["year"] = vintages_csv
        df_csv["format"] = formats_csv
        df_csv["price"] = costs_csv
        df_csv["qty"] = qtys_csv
        df_csv["negoce"] = negoces_csv
        df_csv.to_csv(self.convertedfilename,encoding="utf-8")
        self.converted_file = df_csv.to_dict()
    def getSimilar(self,wine):
        found_wine = False
        regex_pattern = r"""(\bDE\b|\bd\b|
                     |\bDU\b|\bLA\b|
                     |\bLE\b|\bCHATEAU\b|
                     |\bCH\b|\bCH\b|
                     |\bLes\b|\bTenuta\b|
                     |\bde la\b\|\bdell\b|
                     |\bl\b|\bhaut\b)"""
        special_chars_pattern = r'[^A-Za-z0-9 ]+'
        rouge_pattern = r"(\br\b|\brge\b)"
        blanc_pattern = r"(\bb\b|\bblc\b)"

        self.match_wines[wine] = {}
        self.match_wines[wine]["Wine"] = []
        self.match_wines[wine]["Wine Chinese"] = []
        self.match_wines[wine]["id"] = []
        
        regex_checker = re.compile(regex_pattern,re.IGNORECASE)
        regex_special_chars = re.compile(special_chars_pattern)
        regex_rouge = re.compile(rouge_pattern)
        regex_blanc = re.compile(blanc_pattern)
        
        cleaned_wine = unidecode.unidecode(regex_checker.sub("",wine.decode("utf-8")).lower())
        cleaned_wine = regex_special_chars.sub("",cleaned_wine).strip()
        cleaned_wine = regex_rouge.sub("",cleaned_wine).strip()
        cleaned_wine = regex_blanc.sub("",cleaned_wine).strip()
        cleaned_wine = " ".join([word.strip() for word in cleaned_wine.split()])

        for x,(dictionary_wine,dictionary_wine_chinese) in enumerate(zip(self.wines_english,self.wines_chinese)):
       
            dictionary_wine_cleaned = unidecode.unidecode(regex_checker.sub("",dictionary_wine.decode("utf-8")).lower())
            dictionary_wine_cleaned = regex_special_chars.sub("",dictionary_wine_cleaned).strip()
            dictionary_wine_cleaned = regex_rouge.sub("",dictionary_wine_cleaned).strip()
            dictionary_wine_cleaned = regex_blanc.sub("",dictionary_wine_cleaned).strip()
            dictionary_wine_cleaned = " ".join([word.strip() for word in dictionary_wine_cleaned.split()])

            res = difflib.SequenceMatcher(None,cleaned_wine,dictionary_wine_cleaned).ratio()
            if res > 0.92:
                found_wine = True
                self.match_wines[wine]["Wine"].append(dictionary_wine)
                self.match_wines[wine]["Wine Chinese"].append(dictionary_wine_chinese)
                self.match_wines[wine]["id"].append(x)
                self.found_wines.append((wine,dictionary_wine))
                break
        if not found_wine:
            if wine not in self.not_found_wines:
                self.not_found_wines.append(wine)
    def getDictionaryData(self):
        return self.dictionary_content
    def getConvertedFileData(self):
        return self.converted_file
