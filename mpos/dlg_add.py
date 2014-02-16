#! /usr/bin/python

# encoding: -*- utf-8 -*-

# dialogs.py

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

import wx
import config
import string
import mpos_utility

class AddDlg(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(AddDlg, self).__init__(parent, *args, **kwargs)
        
        font1 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        self.Size = (500, 260)
        
        # Get necessary configuration information
        #------------------------------------------------------------------
        self.config = config.Configuration()
        self.cSettings = self.config.cCurrency()
        self.c_symbol = self.cSettings[0]
        self.c_dec = self.cSettings[1]
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #------------------------------------------------------------------
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.add_label = wx.StaticText(self, -1, '-')
        self.add_label.SetFont(font1)
        hbox1.Add(self.add_label, 0)
        sizer.Add(hbox1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        
        #--#
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.item_label = wx.StaticText(self, -1, '-', 
                                        size=(130, -1))
        self.item_label.SetFont(font2)
        self.item_input = wx.TextCtrl(self, -1, style=wx.TE_CENTER)
        hbox2.Add(self.item_label, 0, wx.TOP|wx.RIGHT, 5)
        hbox2.Add(self.item_input, 1)
        sizer.Add(hbox2, 0, wx.EXPAND|wx.ALL, 10)
        
        #--#
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.price_label = wx.StaticText(self, -1, 
                                         '-' +' ('+self.c_symbol+')',
                                         size=(130, -1))
        self.price_label.SetFont(font2)
        self.price_input = wx.TextCtrl(self, -1, style=wx.TE_CENTER)
        hbox3.Add(self.price_label, 0, wx.TOP|wx.RIGHT, 5)
        hbox3.Add(self.price_input, 1)
        sizer.Add(hbox3, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        #--#
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.bulk = wx.CheckBox(self, -1, 'Bulk Item')
        hbox4.Add(self.bulk, 0)
        sizer.Add(hbox4, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        #--#
        hbox5 = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(hbox5, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        sizer.Add((-1, 10))
        
        self.SetSizer(sizer)
        
        self.item_input.SetFocus()
        
        # Set Language ----------------------------------------------------
        self.Language()
        
        # Set Event Bindings
        #------------------------------------------------------------------
        self.price_input.Bind(wx.EVT_KEY_UP, self.ValidatePrice)
        self.price_input.Bind(wx.EVT_KILL_FOCUS, self.PrClean)
       
    #######################################################################
    def ValidatePrice(self, evt):
        'Checks that the user has entered a valid price'
        try:
            num = self.price_input.GetValue()
            if num[-1] not in string.digits+'.':
                wx.Bell()
                self.price_input.SetValue(num[:-1])
                self.price_input.SetInsertionPointEnd()
        except IndexError, e:
            pass
        
    #----------------------------------------------------------------------            
    def AddGetVals(self):
        'Gets Values from the dlg input TextCtrls'
        item = self.item_input.GetValue().strip()
        price = self.price_input.GetValue()
        if self.bulk.GetValue():
            bulk = 1
        else:
            bulk = 0
        if item and self.numCheck(price):
            return [item, price, bulk]
        else:
            self.m1 = 'You must enter the item name and price'
            self.t1 = 'Add Product Fail!'
            wx.MessageBox(self.m1, self.t1)
    
    #----------------------------------------------------------------------
    def PrClean(self, evt):
        'Turns whatever the user entered into a valid price'
        try:
            ins = '%.'+self.c_dec+'f'
            num = float(self.price_input.GetValue())
            rslt = ins % num
            self.price_input.SetValue(rslt)
        except ValueError, e:
            self.price_input.SetValue('')
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the config lang to the object.'
        # Create the word id list
        id_list = (5, 6, 7, 8, 9, 81)
        words = mpos_utility.lang(id_list)
        
        # Set Objects
        self.add_label.SetLabel(words[0])
        self.item_label.SetLabel(words[1])
        self.price_label.SetLabel(words[2] + ' ('+unicode(self.c_symbol, 'utf8')+')')
        self.t1 = words[3]
        self.m1 = words[4]
        self.bulk.SetLabel(words[5])
        
    #----------------------------------------------------------------------
    def numCheck(self, number):
        'Checks that the final number is valid.'
        try:
            x = float(number)
            return True
        except ValueError:
            return False
        
        
        
        