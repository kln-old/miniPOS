#! /usr/bin/python

# encoding: -*- utf-8 -*-

# config.py

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

# This module creates the CSV object that manages the config.csv file

import csv
import os, sys

class Configuration(object):
    'Handles the CVS functions for the config.csv object'
    def __init__(self, filename = 'config.csv'):
        
        
        filename = self._fPath(filename)
        if not os.path.isfile(filename):
            print 'Creating config.csv'
            
            if __name__ != '__main__':
                    filename = self._fPath(filename)
    
            file = open('config.csv', 'wb')
            writer = csv.writer(file, dialect='excel')
            writer.writerow(['ID'] + ['Value'])
            writer.writerow(['Language'] + ['English'])
            writer.writerow(['Currency Sign'] + ['$'])
            writer.writerow(['Currency Decimal Points'] + [2])
            writer.writerow(['Toggle Thousands Sep'] + [1])
            writer.writerow(['Toggle Sales Tax'] + [0])
            writer.writerow(['Sales Tax'] + [0.0])
            
            file.close()
    
    #----------------------------------------------------------------------
    def _wOpen(self, filename = 'config.csv'):
        'Opens the file to be written to'
        if __name__ != '__main__':
            filename = self._fPath(filename)
        self.cFile = open(filename, 'wb')
    
    #----------------------------------------------------------------------
    def _rOpen(self, filename = 'config.csv'):
        'Opens the file to be read'
        if __name__ != '__main__':
            filename = self._fPath(filename)
        self.cFile = open(filename, 'rb')
    
    #----------------------------------------------------------------------
    def _fPath(self, filename = 'config.csv'):
        'This writes the correct filepath to the config.csv file'
        if hasattr(sys, 'frozen'):
            fullpath = os.path.abspath('./resources/config.csv')
        else:
            fullpath = os.path.split(__file__)[0]
            fullpath = os.path.join(fullpath, 'resources', filename)
        return fullpath
    
    #----------------------------------------------------------------------
    def _ReadConfig(self):
        'Reads the configuration values and returns them as a list'
        self._rOpen()
        reader = csv.reader(self.cFile, dialect='excel')
        config_table = []
        for row in reader:
            config_table.append(row[-1])
        return config_table
        cFile.close()
        
    # Return the language config
    #----------------------------------------------------------------------
    def cLanguage(self):
        'Returns the current language setting as a string'
        clist = self._ReadConfig()
        return clist[1]
            
    # Return the Currency symbol and decimal places
    #----------------------------------------------------------------------
    def cCurrency(self):
        'Returns the symbol and number of decimal places as a list.'
        clist = self._ReadConfig()
        rtn = clist[2:4]
        rtn[0] = unicode(rtn[0].decode('utf8'))
        return clist[2:4]
        
    # Return a Boolean value for the thousands separator
    #----------------------------------------------------------------------
    def ThousandsSep(self):
        'Returns a boolean value indicating if the user wants a thousands sep'
        clist=self._ReadConfig()
        if clist[4] == '1':
            return True
        else:
            return False
        
    # Return the information for the sales tax
    #----------------------------------------------------------------------
    def SalesTaxInfo(self):
        'Returns the toggle and rate for Sales Tax'
        clist=self._ReadConfig()
        # rslt = [toggle value, sales tax percent]
        rslt = [clist[5], clist[6]]
        return rslt
    
    # Return the language
    #----------------------------------------------------------------------
    def LangInfo(self):
        'Returns the selected language'
        clist = self._ReadConfig()
        return clist[1]
        
    # Return all configuration information
    #----------------------------------------------------------------------
    def ConfigSettings(self):
        'Returns all the current configuration information'
        clist = self._ReadConfig()
        return clist
    
    # Write new config settings to config.csv
    #----------------------------------------------------------------------
    def SetConfig(self, settings):
        '''Takes user choices from the prefs.py dlg and puts 
        them into the csv file'''
        if hasattr(sys, 'frozen'):
            path = os.path.abspath('./resources/config.csv')
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources', 'config.csv')
        file = open(path, 'wb')
        
        writer = csv.writer(file, dialect='excel')
        writer.writerow(['ID'] + ['Value'])
        writer.writerow(['Language'] + [settings[0]])
        writer.writerow(['Currency Sign'] + [settings[1]])
        writer.writerow(['Currency Decimal Points'] + [settings[2]])
        writer.writerow(['Toggle Thousands Sep'] + [settings[3]])
        writer.writerow(['Toggle Sales Tax'] + [settings[4]])
        writer.writerow(['Sales Tax'] + [settings[5]])
        file.close()

###########################################################################
        
# Create object for testing            
if __name__ == '__main__':
    j = Configuration()

