from keys_script import negoces_dictionary,wines_dictionary
import pandas as pd
import re
import difflib,unidecode
from .models import eurhkd, usdhkd, markup

def check_price(price):
    flag = False
    try:
        float(price)
        flag = True
    except Exception as e:
        pass
    return flag

def check_template_file(a_file):
    flag = False
    if a_file.endswith("xls"):
        flag = True
    if a_file.endswith("xlsx"):
        flag = True
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

def getMarkup():
    markup_prices = markup.objects.order_by().values_list("price",flat=True)
    markups = markup.objects.order_by().values_list("mark",flat=True)
    return markup_prices,markups
    
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
        self.filename = self.path.split("/")[-1].split(".")[0]
        filename_words = self.filename.split()
        self.filename_words = [word.lower() for word in filename_words]
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
            markup_prices,markups = getMarkup()
            try:
                if self.negoces[self.negoce]["currency"] == "euro":
                    pair_rate = eurhkd.objects.latest("value").value
                if self.negoces[self.negoce]["currency"] == "dollar":
                    pair_rate = usdhkd.objects.latest("value").value
            except Exception as e:
                print e
        else:
            path_markup = r"/home/david/Documents/notebooks/Joseph Luk/markup.csv" 
            df_markup = pd.read_csv(path_markup)
            markup_prices = df_markup["price"].tolist()
            markups = df_markup["markup"].tolist()
            if self.negoce:
                if self.negoces[self.negoce]["currency"] == "euro":
                    pair_rate = "8.5319"
                if self.negoces[self.negoce]["currency"] == "dollar":
                    pair_rate = "7.7552"
        if self.negoce and "eur" not in self.filename_words:
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
            if "eur" in self.filename_words:
                pair_rate = eurhkd.objects.latest("value").value

                prices = []
                for price in self.df["Cost"].tolist():
                    hkdprice = "{0:.2f}".format(float(price)*float(pair_rate))
                    prices.append(hkdprice)
                all_prices = prices
            else:
                all_prices = self.df["Cost"].tolist()
            all_wines = self.df["Wine"].tolist()
            all_years = self.df["Vintage"].tolist()
            all_regions = self.df["Region"].tolist()
            all_formats = self.df["Format"].tolist()
            self.msg["quantities"] = self.df["Qty"].tolist()
            self.msg["negoces"] = self.df["Negoce"].tolist()
            try:
                self.msg["types"] = self.df["Type"].tolist()
                self.msg["vendors"] = self.df["Vendor"].tolist()
            except Exception as e:
                print e
                self.msg["types"] = [""] * len(all_prices)
                self.msg["vendors"] = [""] * len(all_prices)
            
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

class handleDictionary:
    def __init__(self,path,is_negoce,location='/home/ubuntu/app/data2/'):
        self.path = path
        self.location = location
        self.is_negoce = is_negoce
        self.getStart()
    def getStart(self):
        if not self.is_negoce:
            df_xls = pd.read_excel(self.path)
            df_xls.to_csv(self.location+"dictionary.csv",encoding="utf-8")
            self.getDictionary()
        else:
            self.convertedfilename = self.path.split("/")[-1].split(".")[0]
            self.convertedfilename = self.location + self.convertedfilename + "_converted.csv"
            print self.convertedfilename
            self.match_wines = {}
            self.getDictionary()
            self.getCSV()
    def getDictionary(self):
        df_dictionary = pd.read_csv(self.location+"dictionary.csv")
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
        regex_pattern = r"""(\bDE\b|\bd\b|
                     |\bDU\b|\bLA\b|
                     |\bLE\b|\bCHATEAU\b|
                     |\bCH\b|\bCH\b|
                     |\bLes\b|\bTenuta\b|
                     |\bde la\b\|\bdell\b|
                     |\bl\b|\bhaut\b|
                     |\br\b|\bb\b)"""
        special_chars_pattern = r'[^A-Za-z0-9 ]+'

        self.match_wines[wine] = {}
        self.match_wines[wine]["Wine"] = []
        self.match_wines[wine]["Wine Chinese"] = []
        self.match_wines[wine]["id"] = []
     
        regex_checker = re.compile(regex_pattern,re.IGNORECASE)
        regex_special_chars = re.compile(special_chars_pattern)
        
        cleaned_wine = unidecode.unidecode(regex_checker.sub("",wine.decode("utf-8")).lower())
        cleaned_wine = regex_special_chars.sub("",cleaned_wine).strip()

        for x,(dictionary_wine,dictionary_wine_chinese) in enumerate(zip(self.wines_english,self.wines_chinese)):

            dictionary_wine_cleaned = unidecode.unidecode(regex_checker.sub("",dictionary_wine.decode("utf-8")).lower())
            dictionary_wine_cleaned = regex_special_chars.sub("",dictionary_wine_cleaned).strip()

            res = difflib.SequenceMatcher(None,cleaned_wine,dictionary_wine_cleaned).ratio()
            if res > 0.92:
                print wine, dictionary_wine
                self.match_wines[wine]["Wine"].append(dictionary_wine)
                self.match_wines[wine]["Wine Chinese"].append(dictionary_wine_chinese)
                self.match_wines[wine]["id"].append(x)
    def getDictionaryData(self):
        return self.dictionary_content
    def getConvertedFileData(self):
        return self.converted_file
