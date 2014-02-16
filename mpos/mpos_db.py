#! /usr/bin/python

# encoding: -*- utf-8 -*-

# mpos_db.py

#    This file is part of miniPOS.

#    miniPOS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    miniPOS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with miniPOS.  If not, see <http://www.gnu.org/licenses/>.

# This module creates the database object class for the Mini POS program

import wx
import sqlite3
import os, sys
import config
import time
import datetime
import db_create

class MPOS_DB(object):
    
    def __init__(self, filename = 'pos_data.db'):
        if hasattr(sys, 'frozen'):
            filepath = os.path.join('resources', filename)
        else:
            filepath = os.path.join(os.path.split(__file__)[0], 'resources', 
                                    filename)
            
        if not os.path.isfile(filepath):
            db_create.DBCreate()
            
        self.conn = sqlite3.connect(filepath)
            
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys = ON;")
        
        # Create complimentary objects
        #------------------------------------------------------------------
        self.config = config.Configuration()
        
    #######################################################################
    #                          PRODUCT TABLE METHODS                      #
    #######################################################################
    def AddProduct(self, info_list):
        'Takes input from Invetory => Add Item and adds it to the database'
        item, price, bulk = info_list
        values = (item, price, bulk)
        self.curs = self.conn.cursor()
        try:
            self.curs.execute('''
                          INSERT INTO products (productName, productPrice, 
                            bulk) VALUES (?, ?, ?);''', values)
        except sqlite3.OperationalError:
            wx.MessageBox('''miniPOS is installed in a read-only directory!
Try reinstalling in a different directory.''', 
                          'Installation Error')
        self.conn.commit()
    
    #----------------------------------------------------------------------
    def EditProduct(self, info_list):
        'Takes input from Inventory => Edit Item and updates the database.'
        id = int(info_list[0])
        name = info_list[1]
        price = self._PriceRestore(info_list[2])
        bulk = info_list[3]
        values = (name, price, bulk, id)
        sql = '''UPDATE products
                SET productName = ?, productPrice = ?, bulk = ? 
                WHERE productId = ?'''
        self.curs = self.conn.cursor()
        try:
            self.curs.execute(sql, values)
        except sqlite3.OperationalError:
            wx.MessageBox('''miniPOS is installed in a read-only directory!
Try reinstalling in a different directory.''', 
                          'Installation Error')
            return False
        self.conn.commit()
        
    #----------------------------------------------------------------------    
    def AllProducts(self):
        'Returns the entire product table as a list of tuples'
        self.curs = self.conn.cursor()
        self.curs.execute('''
                          SELECT * 
                          FROM products;''')
        product_table = []
        
        for row in self.curs:
            product_table.append(list(row))
            
        return product_table
    
    #----------------------------------------------------------------------
    def productSearch(self, term_list):
        # Create a dynamic where condition
        where_stmt = "WHERE productName LIKE " + term_list[0] + ' '
        for term in term_list:
            if term_list.index(term) != 0:
                where_stmt += "OR productName LIKE " + term + " "
            where_stmt += "OR productId LIKE " + term + " "
            where_stmt += "OR productPrice LIKE " + term + " "
        
        sql = 'SELECT * FROM products ' + where_stmt + ';'
        
        # Execute in Sqlite
        product_table = []
        self.curs = self.conn.cursor()
        self.curs.execute(sql)
        for row in self.curs:
            product_table.append(list(row))
        
        return product_table
    
    #----------------------------------------------------------------------
    def productRecordSearch(self, stDate, endDate, term_list):
        'This is used by the sales panel to search for product records within\
            the specified dates.'
        where_stmt = "products.productName LIKE " + term_list[0] + ' '
        for term in term_list:
            if term_list.index(term) != 0:
                where_stmt += "OR products.productName LIKE " + term + " "
            where_stmt += "OR products.productId LIKE " + term + " "
            where_stmt += "OR products.productPrice LIKE " + term + " "
            
        date_stmt = self.DateStmt(stDate, endDate, True)
        
        sql='''
        SELECT sale_items.productId, products.productName,
            sale_items.salePrice, SUM(sale_items.quantity)
        FROM products, sale_items, sales
        WHERE products.productId = sale_items.productId AND 
        sale_items.saleId = sales.saleId
        AND (''' + date_stmt + ") and (" + where_stmt + ") " +\
        "GROUP BY sale_items.productId, sale_items.salePrice;"
        
        self.curs = self.conn.cursor()
        self.curs.execute(sql)
        rslt = []
        for row in self.curs:
            rslt.append(list(row))
        for i in range(len(rslt)):
            rslt[i].append(rslt[i][2] * rslt[i][3])
        return rslt
            
    #----------------------------------------------------------------------
    def ProductRecUpdate(self, stDate, endDate):
        'Returns summary report of products sold within the specified dates.'
        date_stmt = self.DateStmt(stDate, endDate)
        
        # Get Items grouped by name and then price
        sql = '''
        SELECT sale_items.productId, products.productName,
            sale_items.salePrice, SUM(sale_items.quantity)
        FROM products, sale_items, sales
        WHERE products.productId = sale_items.productId AND 
        sale_items.saleId = sales.saleId
        AND (''' + date_stmt + ") " +\
        "GROUP BY sale_items.productId, sale_items.salePrice;"
        self.curs.execute(sql)
        
        rslt = []
        for row in self.curs:
            rslt.append(list(row))
        for i in range(len(rslt)):
            rslt[i][1].encode('utf8')
            rslt[i].append(rslt[i][2] * rslt[i][3])
        return rslt
        # rslt=[productId, productName, SalePrice, quantity]
      
    #----------------------------------------------------------------------
    def GetBulk(self, productId):
        'Returns the boolean value indicating if an item is sold by the bulk.'
        sql = 'SELECT bulk FROM products WHERE productId = ?'
        self.curs = self.conn.cursor()
        self.curs.execute(sql, (productId, ))
        rslt = []
        for line in self.curs:
            rslt.append(line[0])
        return rslt[0]
    
    #----------------------------------------------------------------------
    def GetItemId(self, productName):
        'Given a productName, returns the product\s bulk status'
        sql = '''SELECT productId FROM products WHERE productName = ?;'''
        self.curs = self.conn.cursor()
        self.curs.execute(sql, (productName, ))
        id = []
        for line in self.curs:
            id.append(line[0])
        return id[0]
        
    #######################################################################
    #                        Sales Table Function                         #
    #######################################################################
    def RecordSale(self, amount):
        'Records a sale into the database'
        date = time.localtime()[:5]
        date = (date[2], date[1], date[0], date[3], date[4],)
        date = "%d/%d/%d %d:%02d" % date
        
        value = (date, float(amount))
        sql = '''INSERT INTO sales 
                (date, amount)
                VALUES (?, ?);'''
        
        self.curs = self.conn.cursor()
        try:
            self.curs.execute(sql, value)
        except sqlite3.OperationalError:
            wx.MessageBox('''miniPOS is installed in a read-only directory!
Try reinstalling in a different directory.''', 
                          'Installation Error')
            return False
        self.conn.commit()
        # get saleId
        sql2 = 'SELECT saleId FROM sales WHERE date = ? AND amount = ?;'
        self.curs.execute(sql2, value)
        saleId = 'x'
        for row in self.curs:
            saleId = row[0]
        return saleId
        
    #----------------------------------------------------------------------    
    def GetTime(self):
        'Returns the 24 hr time of sale'
        x = time.localtime(time.time())
        hour, min = str(x[3]), str(x[4])
        return hour + ':' + min 
            
    #----------------------------------------------------------------------
    def DateTrans1(self, date):
        'Translates the YYYY-MM-DD object into a D/M/YYYY string'
        date = str(date).split('-')
        y, m, d = date
        if m[0] == '0': m = m[1]
        if d[0] == '0': d = d[1]
        date = ('%s/%s/%s')%(d, m, y)
        return date
    
    #----------------------------------------------------------------------
    def DateTrans2(self, date):
        'Translates the D/M/YYYY string into a datetime.date object'
        date = date.split('/')
        d, m, y = int(date[0]), int(date[1]), int(date[2])
        date = datetime.date(y, m, d)
        return date
    
    #----------------------------------------------------------------------
    def DateStmt(self, stDate, endDate, sTable = False):
        'Returns the date section between the supplied dates for SQL'
        # sTable tells is the date statement is part of a joint query 
        #       using the sales table
        if sTable:
            d_stmt = 'sales.date'
        else:
            d_stmt = 'date'
        # Make the first part of the datxe_stmt and break if stDate == endDate
        date = self.DateTrans1(self.DateTrans2(stDate))
        date_stmt = d_stmt + " LIKE '" + date + "%' "
        if stDate == endDate: return date_stmt
        # Make the stDate and endDate into timedate objects
        stDate, endDate = self.DateTrans2(stDate), self.DateTrans2(endDate)
        # Make the timedelta
        delta = datetime.timedelta(days=1)
        # Add to the date_stmt until stDate == endDate
        while True:
            stDate = stDate + delta
            date = self.DateTrans1(stDate)
            date_stmt += "OR " + d_stmt + " LIKE '" + date + "%' "
            if stDate == endDate:
                break
        
        return date_stmt
    
    #----------------------------------------------------------------------
    def SalesRecords(self, stDate, endDate):
        'Returns the sales_table for the selected dates'
        date_stmt = self.DateStmt(stDate, endDate, False)
        sql = 'SELECT saleId, date, amount FROM sales WHERE ' +\
             date_stmt + 'ORDER BY saleId DESC;'
        self.curs = self.conn.cursor()
        self.curs.execute(sql)
        rslt = []
        for row in self.curs:
            rslt.append(list(row))
        return rslt
    
    #----------------------------------------------------------------------
    def UpdateSale(self, saleId, amount):
        'Updates a sale record on the sales table. Only updates Amount'
        values = (amount, saleId)
        sql = 'UPDATE sales SET amount = ? WHERE saleId = ?'
        self.curs = self.conn.cursor()
        self.curs.execute(sql, values)
        self.conn.commit()
        
        
    #######################################################################
    #                       SALE_ITEMS FUNCTIONS                          #
    #######################################################################
    def RecSaleItems(self, saleId, receipt_list):
        self.curs = self.conn.cursor()
        for i in range(len(receipt_list)):
            values = (receipt_list[i][0], saleId, receipt_list[i][1], 
                      receipt_list[i][2])
            sql = '''INSERT INTO sale_items
                    (productId, saleId, salePrice, quantity)
                    VALUES (?, ?, ?, ?);'''
                    
            self.curs.execute(sql, values)
            self.conn.commit()
    
    #---------------------------------------------------------------------
    def DeleteSIRecord(self, saleId):
        'Updates the sale_items list when an old receipt is changed'
        # Set the sale price and quantity to zero for all items in the 
        # original receipt
        sql= '''DELETE FROM sale_items
                WHERE saleId = ?'''
        values = (saleId, )
        self.curs = self.conn.cursor()
        self.curs.execute(sql, values)
        self.conn.commit()
        
    #----------------------------------------------------------------------    
    def ReceiptSelect(self, saleId):
        if saleId:
            self.curs = self.conn.cursor()
            sql = '''SELECT products.productName, sale_items.salePrice,
            sale_items.quantity
            FROM products, sale_items
            WHERE sale_items.saleId = ''' + saleId + ''' AND products.productId 
            = sale_items.productId;'''
            self.curs.execute(sql)
            rslt = []
            for row in self.curs:
                rslt.append(list(row))
            
            for i in range(len(rslt)):
                rslt[i][0].encode('utf8')
                rslt[i].append(rslt[i][1] * rslt[i][2])
        
            return rslt
        else:
            return False
    
    #----------------------------------------------------------------------    
    def ReceiptRecall(self, saleId):
        sql = '''
                SELECT products.productId, products.productName, 
                    sale_items.salePrice, sale_items.quantity
                FROM products, sale_items
                WHERE products.productId = sale_items.productId AND
                    sale_items.saleId = ''' + saleId + ';'
        
        self.curs = self.conn.cursor()
        self.curs.execute(sql)
        
        rslt = []
        for row in self.curs:
            rslt.append(list(row))
        for i in range(len(rslt)):
            rslt[i].append(rslt[i][2] * rslt[i][3])
        return rslt
    
    #----------------------------------------------------------------------    
    def ReceiptNo(self):
        try:
            sql = 'SELECT MAX(saleId) FROM sales'
            self.curs = self.conn.cursor()
            self.curs.execute(sql)
            max = ''
            for row in self.curs:
                max = row[0]
            return int(max) + 1
        except TypeError, e:
            return 1
            
    
    #######################################################################
    #                       SPECIAL QUERIES                               #
    #######################################################################
    def QuantitySold(self, productId):
        self.curs = self.conn.cursor()
        self.curs.execute('''SELECT sum(sale_items.quantity) 
                          FROM sale_items, products
                          WHERE sale_items.productId = ? 
                          and products.productID = ?;''', 
                          (productId, productId))
        self.conn.commit()
        for x in self.curs:
            return str(x[0])
    
    #----------------------------------------------------------------------
    def ResetDB(self):
        'Deletes all records from the DB'
        sql = ['DELETE FROM sale_items', 'DELETE FROM sales', 
               'DELETE FROM products;']
        self.curs = self.conn.cursor()
        for line in sql:
            self.curs.execute(line)
        self.conn.commit()
        
    #----------------------------------------------------------------------
    def _PriceRestore(self, price):
        'Restores the price from a string back into a float'
        try:
            space_index = price.index(' ')
            price = price[space_index:]
        except ValueError:
            pass
        
        return float(price)
    
   
        
        
        
