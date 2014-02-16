#! usr/bin/python

# encoding: -*- utf-8 -*-

# mpos_utility.py

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
import config
import csv

def lang(id_list):
    '''Takes an id list of words to take from the lang file specified
    in the config file.'''
    conf = config.Configuration()
    lang = conf.LangInfo() + '.csv'
    
    # test for finding the correct dir
    if hasattr(sys, 'frozen'):
        path = os.path.join('resources', lang)
    else:
        x = os.path.split(__file__)[0]
        path = os.path.join(x, 'resources', lang)
    
    # Get the language list
    file = open(path, 'rb')
    reader = csv.reader(file, dialect='excel')
    lang_list = []
    for word in reader:
        lang_list.append(unicode(word[1], 'utf8'))
    
    # Get the words/phrases requested in the indext list
    rslt = []
    for i in id_list:
        rslt.append(lang_list[i+1])
    return rslt

#----------------------------------------------------------------------
def UnTSep(amount):
    'Removes any thousand separating commas from an amount.'
    amount = list(amount)
    sep_count = 0
    for i in range(len(amount)):
        if amount[i] == ',': sep_count += 1
    for i in range(sep_count):
        amount.remove(',')
    return ''.join(amount)
    
#--------------------------------------------------------------------------            
def CheckPath():
    'Checks to see if the root path of the program has adequate privileges.'
    # Set 'resource' dir path, depending on sys.version()
    path = os.path.split(__file__)[0]
    if hasattr(sys, 'frozen'):
        path = os.path.split(path)[0]
        path = os.path.split(path)[0]
        path = os.path.join(path, 'resources')
    else:
        path = os.path.join(path, 'resources')

    # If unable to find correct dir
    if not os.access(path, os.F_OK):
        path = os.getcwd()
    # Check Privileges
    check = True
    if not os.access(path, os.W_OK):
        check = False
    return check

#--------------------------------------------------------------------------
def DirFailMessage():
    'Informs of inability to perform some database action.'
    if hasattr(sys, 'frozen'):
        m = '''
You do not have read/write privileges in the miniPOS installation directory! 

The program may not function correctly! Try reinstalling in "My Documents",

or changing the installation directory's permissions.'''
    else:
        m = '''
You do not have read/write privileges in the miniPOS installation directory!

The program may not function correctly! Try starting the program with: 

'sudo mini_pos.py', or changing the installation directory's permissions.'''
            
    wx.MessageBox(m, 'Warning!')