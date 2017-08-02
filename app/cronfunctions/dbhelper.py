import MySQLdb as mdb
import keys_script
from dbfeeder import updatedb
import pandas as pd

def access():
    con = mdb.connect(keys_script.HOST,keys_script.USER,keys_script.PASSWORD,keys_script.NAME)
    cmd = "SHOW TABLES"
    with con:
        cur = con.cursor()
        cur.execute(cmd)
        print cur.fetchall()

def accessLatestValue():
    con = mdb.connect(keys_script.HOST,keys_script.USER,keys_script.PASSWORD,keys_script.NAME)
    cmd = "SELECT value FROM datadb_eurhkd"
    with con:
        cur = con.cursor()
        cur.execute(cmd)
        print cur.fetchall()[-1][0]

def feedMarkup(path):
    df = pd.read_csv(path)
    prices = df["price"].tolist()
    markups = df["markup"].tolist()

    db_obj = updatedb()
    #update(self,columns,table,*args)
    table = "datadb_markup"
    columns = "(price,mark)"
    for price,markup in zip(prices,markups):
        db_obj.update(columns,table,price,markup)

def getValues():
    #table = "datadb_markup"
    #markup_prices = markup.objects.order_by().values_list("price",flat=True)
    #markups = markup.objects.order_by().values_list("mark",flat=True)
    table_obj = updatedb()
    table = "datadb_markup"
    #getLastValue(self,field,table):
    #rate = table_obj.getLastValue("price",table)
    rate = table_obj.getValues("price",table) #getValues
    print rate
    rate = table_obj.getValues("mark",table)
    print rate

def removeValues():
    table_obj = updatedb()
    table = "merchants_negoces"
    #remove(self,table)
    table_obj.remove(table)

path = r"/home/ubuntu/app/cronfunctions/markup.csv"
#accessLatestValue()
#feedMarkup(path)
access()
#getValues()
#removeValues()
