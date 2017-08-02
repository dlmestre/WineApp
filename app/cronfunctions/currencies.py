from dbfeeder import updatedb
import datetime
from yahoo_finance import Currency

def currencies(currency):
    if currency == "euro":
        try:
            return Currency('EURHKD').get_rate()
        except Exception as e:
            print e
            return None
    elif currency == "dollar":
        try:
            return Currency('USDHKD').get_rate()
        except Exception as e:
            print e
            return None
    elif currency == "pound":
        try:
            return Currency('GBPHKD').get_rate()
        except Exception as e:
            print e
            return None

def feeddatabase(value,date,works,table,obj):
    column = "(value, date, works)"
    obj.update(column,table,value,date,works)

def main():
    print "running"
    # tables -> ('datadb_eurhkd'), ('datadb_usdhkd')
    # variables -> value, date, works
    eurhkd = currencies("euro")
    usdhkd = currencies("dollar")
    gbphkd = currencies("pound")
    datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    pair_obj = updatedb()

    if eurhkd and usdhkd and gbphkd:
        print eurhkd,usdhkd,gbphkd
        feeddatabase(eurhkd,datenow,"Yes",'datadb_eurhkd',pair_obj)
        feeddatabase(usdhkd,datenow,"Yes",'datadb_usdhkd',pair_obj) 
        feeddatabase(gbphkd,datenow,"Yes",'datadb_gbphkd',pair_obj)
    else:
        #getPrice(self,table)
        tableEUR = 'datadb_eurhkd'
        tableUSD = 'datadb_usdhkd'
        tableGBP = 'datadb_gbphkd'
        eurhkd = pair_obj.getPrice(tableEUR)
        usdhkd = pair_obj.getPrice(tableUSD)
        gbphkd = pair_obj.getPrice(tableGBP)        
        feeddatabase(eurhkd,datenow,"No",'datadb_eurhkd',pair_obj)
        feeddatabase(usdhkd,datenow,"No",'datadb_usdhkd',pair_obj)
        feeddatabase(usdhkd,datenow,"No",'datadb_gbphkd',pair_obj)
    print "Done"
main()
