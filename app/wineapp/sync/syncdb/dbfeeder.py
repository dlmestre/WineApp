import MySQLdb as mdb
import datetime
import os
import keys_script

class updatedb:
    def __init__(self):
        self.con = self.connect()
    def connect(self):
        return mdb.connect(keys_script.HOST,keys_script.USER,keys_script.PASSWORD,keys_script.NAME,use_unicode=True,charset="utf8mb4")
    def getPrice(self,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT value FROM {0}".format(table)
            cur.execute(cmd)
            lastpairprice = cur.fetchall()[-1][0]
        return lastpairprice
    def getLastValue(self,field,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT {0}".format(field)
            cmd = cmd + " FROM {0}".format(table)
            cur.execute(cmd)
            lastpairvalue = cur.fetchall()[-1][0]
        return lastpairvalue
    def getValues(self,field,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT {0}".format(field)
            cmd = cmd + " FROM {0}".format(table)
            cur.execute(cmd)
            values = [value[0] for value in cur.fetchall()]
        return values
    def update(self,columns,table,*args):
        with self.con:
            cur = self.con.cursor()
            string = "INSERT INTO " + str(table)
            #print string
            variables = ["%s"]*len(args)
            variables = ",".join(variables)
            variables = "("+variables+")"
            cmd = string + columns + " VALUES " + variables
            #print cmd
            cur.execute(cmd,args)
    def remove(self,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "TRUNCATE TABLE {0}".format(table)
            cur.execute(cmd)            
    def checkifexists(self,table,column,value):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cmd = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table,column,value)
            cur.execute(cmd)
            results = cur.fetchone()
            if results:
                return True,results
            else:
                return False,False
    def checkIfExistsTwoFields(self,table,column_a,value_a,column_b,value_b):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cmd = "SELECT * FROM {0} WHERE {1} = '{2}' AND {3} = '{4}'".format(table,column_a,value_a,column_b,value_b)
            cur.execute(cmd)
            results = cur.fetchone()
            if results:
                return True,results
            else:
                return False,False
    def editrecord(self,table,field,value,columns,*args):
        with self.con:
            cur = self.con.cursor()
            stringlist = []

            for x,column in enumerate(columns):
                if x == 0:
                    string = "Set %s" % column + "=%s," 
                elif x == len(columns) - 1:
                    string = "%s" % column + "=%s"
                else:
                    string = "%s" % column + "=%s,"
                stringlist.append(string)
            string = " ".join(stringlist)
            cmd = "UPDATE {0} ".format(table)
            print cmd
            cmd = cmd + string + " WHERE {0}='{1}'".format(field,value)
            print cmd
            cur.execute(cmd,args)
    def editRecordTwoFields(self,table,field_a,value_a,field_b,value_b,columns,*args):
        with self.con:
            cur = self.con.cursor()
            stringlist = []

            for x,column in enumerate(columns):
                if x == 0:
                    string = "Set %s" % column + "=%s," 
                elif x == len(columns) - 1:
                    string = "%s" % column + "=%s"
                else:
                    string = "%s" % column + "=%s,"
                stringlist.append(string)
            string = " ".join(stringlist)
            cmd = "UPDATE {0} ".format(table)
            cmd = cmd + string + " WHERE {0} = '{1}' AND {2} = '{3}'".format(field_a,value_a,field_b,value_b)
            print cmd
            cur.execute(cmd,args)
    def ShowTables(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            print tables

#db_obj = updatedb()
#db_obj.ShowTables()
