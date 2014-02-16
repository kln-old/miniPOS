#! /usr/bin/python

# encoding: -*- utf-8 -*-

# dlg_pos_addItem.py

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

# This is the dialog for when an item is selected on the POS panel.
# It allows the user to specify the quantity and change the price of the 
# selected good, if necessary.

import wx
import config
import string        
import mpos_utility
import mpos_db

class POS_AddItem(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(POS_AddItem, self).__init__(parent, *args, **kwargs)
        
        # Set styles for the dialog
        #------------------------------------------------------------------
        font_1 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_2 = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
        
        self.Size = (400, 230)
        
        # Get necessary configuration information
        #------------------------------------------------------------------
        self.config = config.Configuration()
        self.cSettings = self.config.cCurrency()
        self.c_symbol = self.cSettings[0]
        self.c_dec = self.cSettings[1]
        
        self.db = mpos_db.MPOS_DB()
        
        # Set up the box sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        #--#
        self.pos_add_title = wx.StaticText(self, -1, 'Add Items to Receipt')
        self.pos_add_title.SetFont(font_1)
        hbox1.Add(self.pos_add_title, 0)
        sizer.Add(hbox1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 5)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #--#
        self.item_label = wx.TextCtrl(self, -1, '',
                                      style=wx.TE_READONLY|wx.TE_CENTER)
        self.item_label.SetFont(font_2)
        self.item_label.SetBackgroundColour(wx.LIGHT_GREY)
        hbox2.Add(self.item_label, 1)
        sizer.Add(hbox2, 0, wx.EXPAND|wx.ALL, 10)
        
        sizer.Add((-1, 10))
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        #--#
        self.qt_label = wx.StaticText(self, -1, 'Quantity', size=(80, -1))
        self.qt_input = wx.TextCtrl(self, -1, '', style=wx.TE_CENTER)
        self.pr_label = wx.StaticText(self, -1, 'Price'+' ('+self.c_symbol+')',
                                       size=(80, -1))
        self.pr_input = wx.TextCtrl(self, -1, '', 
                                    style=wx.TE_CENTER)
        hbox3.Add(self.qt_label, 0, wx.TOP|wx.RIGHT, 5)
        hbox3.Add(self.qt_input, 1, wx.RIGHT, 20)
        hbox3.Add(self.pr_label, 0, wx.TOP|wx.RIGHT, 5)
        hbox3.Add(self.pr_input, 1)
        sizer.Add(hbox3, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        #--#
        hbox4 = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(hbox4, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        sizer.Add((-1, 10))
        
        self.SetSizer(sizer)
        
        #------------------------------------------------------------------
        self.pr_input.Bind(wx.EVT_KEY_UP, self.PriceValidate)
        self.qt_input.Bind(wx.EVT_KEY_UP, self.QtValidate)
        self.pr_input.Bind(wx.EVT_KILL_FOCUS, self.PrClean)
        self.qt_input.Bind(wx.EVT_KILL_FOCUS, self.QtClean)
        
        #------------------------------------------------------------------
        self.Language()
    
    #######################################################################
    def SetInfo(self, info_list):
        'Gets the product info from the POS panel'
        self.item_id = info_list[0]
        self.item_label.SetValue(info_list[1])
        ins = '%.'+self.c_dec+'f'
        rslt = ins % (info_list[2])
        self.pr_input.SetValue(rslt)
        self.qt_input.SetValue('1')
        self.qt_input.SetInsertionPointEnd()
        self.qt_input.SetFocus()
    
    #----------------------------------------------------------------------
    def SetInfo2(self, info_list):
        'The same as SetInfo, except it also sets the quantity'
        self.item_id = info_list[0]
        self.item_label.SetValue(info_list[1])
        ins = '%.'+self.c_dec+'f'
        rslt = ins % (info_list[2])
        self.pr_input.SetValue(rslt)
        self.qt_input.SetValue(info_list[3])
        self.qt_input.SetFocus()
        
    #----------------------------------------------------------------------    
    def SendInfo(self):
        'Returns the input values to the POS panel'
        if self.numCheck(self.pr_input.GetValue()) and self.numCheck(self.qt_input.GetValue()):
            values = [self.item_id, self.item_label.GetValue(),
                      float(self.pr_input.GetValue()), self.qt_input.GetValue()]
            return values
        else:
            return [None, None, None, None]
    #----------------------------------------------------------------------    
    def PriceValidate(self, evt):
        'Validate the price'
        try:
            # Make sure the last entered value is a digit
            num = self.pr_input.GetValue()[-1]
            if num not in string.digits + '.':
                wx.Bell()
                self.pr_input.SetValue(self.pr_input.GetValue()[:-1])
                self.pr_input.SetInsertionPointEnd()
        except IndexError, e:
            print 'Field Empty'
            
    #----------------------------------------------------------------------
    def QtValidate(self, evt):
        'Validate the quantity entered'
        # Find if the product is sold in bulk
        productName = self.item_label.GetValue()
        bulk = self.db.GetItemId(productName)
        bulk = self.db.GetBulk(bulk)
        # Create an appropriate accept list
        if bulk == 1:
            accept = list(string.digits) + ['.']
        else:
            accept = list(string.digits)
        try:
            input = self.qt_input.GetValue()
            if input[-1] not in accept:
                wx.Bell()
                self.qt_input.SetValue(input[:-1])
                self.qt_input.SetInsertionPointEnd()
        except IndexError, e:
            pass
        
    #----------------------------------------------------------------------
    def PrClean(self, evt):
        'Turns whatever the user entered into a valid price'
        try:
            ins = '%.'+self.c_dec+'f'
            num = float(self.pr_input.GetValue())
            rslt = ins % num
            self.pr_input.SetValue(rslt)
        except ValueError:
            self.pr_input.SetValue('INVALID ENTRY')
        
    #----------------------------------------------------------------------
    def QtClean(self, evt):
        'Turns whatever the user entered into a valid quantity'
        # Find if the product is sold in bulk
        try:
            productName = self.item_label.GetValue()
            bulk = self.db.GetItemId(productName)
            bulk = self.db.GetBulk(bulk)
            
            input = float(self.qt_input.GetValue())
            if bulk == 1:
                ins = '%.'+'3'+'f'
            else:
                ins = '%.'+'0'+'f'
            rslt = ins % input
            self.qt_input.SetValue(rslt)
        except ValueError:
            self.qt_input.SetValue('INVALID ENTRY')
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the language.'
        ids = 15, 16, 7
        words = mpos_utility.lang(ids)
        self.pos_add_title.SetLabel(words[0])
        self.qt_label.SetLabel(words[1])
        self.pr_label.SetLabel(words[2] + ' ('+unicode(self.c_symbol, 'utf8')+')')
        
    #----------------------------------------------------------------------
    def numCheck(self, number):
        'Checks that the final number is valid.'
        try:
            x = float(number)
            return True
        except ValueError:
            return False