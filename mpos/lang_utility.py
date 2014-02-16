#! usr/bin/python

# encoding: -*- utf-8 -*-

# lang_utility.py

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

# contains utility functions for Mini POS 

import os, sys
import csv

def lang(id_list):
    '''Takes an id list of words to take from the lang file specified
    in the config file.'''
    # Get to the configuration file
    if hasattr(sys, 'frozen'):
        path = os.path.join('resources', 'config.csv')
    else:
        path = os.path.split(__file__)[0]
        path = os.path.join(path, 'resources', 'config.csv')
    file = open(path, 'rb')
    reader = csv.reader(file, dialect='excel')
    data = []
    for row in reader:
        data.append(row)
    lang = data[1][1] + '.csv'
    
    # Get the correct path to the lang directory
    if hasattr(sys, 'frozen'):
        path = os.path.join('resources', lang)
    else:
        path = os.path.split(__file__)[0]
        path = os.path.join(path, 'resources', lang)
    
    # Get the language list
    try:
        file = open(path, 'rb')
    except:
        print 'Fail!'
        print 'Path >', path
    reader = csv.reader(file, dialect='excel')
    lang_list = []
    for word in reader:
        lang_list.append(unicode(word[1], 'utf8'))
    
    # Get the words/phrases requested in the indext list
    rslt = []
    for i in id_list:
        rslt.append(lang_list[i+1])
    return rslt