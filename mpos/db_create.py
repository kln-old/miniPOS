#! /usr/bin/python

# encoding: -*- utf-8 -*-

# createDb.py

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

# This file creates the database that will be used for the scale
# model of the POS program

import sqlite3
import sys, os

def DBCreate():
    try:
        open(os.path.join('resources', 'pos_data.db'))
        print 'pos_data.db already exists!'
        
    except IOError, e:
        if hasattr(sys, 'frozen'):
            filepath = os.path.join('resources', 'pos_data.db')
        else:
            filepath = os.path.join(os.path.split(__file__)[0], 'resources',
                                    'pos_data.db')
        
        # Create the new database
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
        
        # Add in the products table
        cursor.execute('''
                       CREATE TABLE products (
                        productId       INTEGER PRIMARY KEY,
                        productName     TEXT,
                        productPrice    REAL, 
                        bulk            INTEGER
                        );''')
        connection.commit()
        
        # Add the sales table
        cursor.execute('''
                       CREATE TABLE sales (
                        saleId          INTEGER PRIMARY KEY,
                        date            TEXT,
                        Amount          REAL
                        );''')
        connection.commit()
        
        # Add the sale_items table
        cursor.execute('''
                       CREATE TABLE sale_items(
                        sale_itemId     INTEGER PRIMARY KEY,
                        productId       INTEGER,
                        saleId          INTEGER,
                        salePrice       REAL,
                        quantity        REAL,
                        FOREIGN KEY(productId) REFERENCES products(productId),
                        FOREIGN KEY(saleId) REFERENCES sales(saleId)
                        );''')
        connection.commit()
        
if __name__ == '__main__':
    DBCreate()
