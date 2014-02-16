#! /usr/bin/python

# encoding: -*- utf-8 -*-

# inventory_panel.py

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

import string
import wx
from lc_mpos import *
import mpos_db
import dlg_add
import dlg_edit
import config
import mpos_utility

class Inventory_Panel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(Inventory_Panel, self).__init__(parent, *args, **kwargs)
        
        # Set the fonts for the panel
        #------------------------------------------------------------------
        font_1 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_4 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.SetBackgroundColour(wx.WHITE)
        
        # EndSizer will be the parent of vsizer1 and vsizer2
        #------------------------------------------------------------------
        endSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #------------------------------------------------------------------
        # vsizer1 will be the parent of the left wx.Boxsizers
        #------------------------------------------------------------------
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        
        #------------------------------------------------------------------
        lbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.title = wx.StaticText(self, -1, 'Inventory Management')
        self.title.SetFont(font_1)
        lbox1.Add(self.title, 0)
        vsizer1.Add(lbox1, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        lbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.search_label = wx.StaticText(self, -1, 'Search'+': ')
        self.search_label.SetFont(font_2)
        self.search_bar = wx.SearchCtrl(self, -1)
        self.search_bar.ShowSearchButton(False)
        self.search_bar.ShowCancelButton(True)
        lbox2.Add(self.search_label, 0, wx.RIGHT|wx.TOP, 5)
        lbox2.Add(self.search_bar, 1)
        vsizer1.Add(lbox2, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5)
        
        vsizer1.Add((-1, 2))
        
        #------------------------------------------------------------------
        lbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.product_lc = ProductLC(self, -1, style=wx.LC_REPORT|\
                                    wx.LC_VRULES|wx.BORDER_DEFAULT)
        lbox3.Add(self.product_lc, 1, wx.EXPAND)
        vsizer1.Add(lbox3, 1, wx.EXPAND|wx.ALL, 5)
        
        endSizer.Add(vsizer1, 4, wx.EXPAND|wx.RIGHT, 5)
        
        
        #------------------------------------------------------------------
        # vsizer2 will be the parent of the right wx.Boxsizers
        #------------------------------------------------------------------
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add((-1, 35))
        
        #------------------------------------------------------------------
        self.details_box = wx.StaticBox(self, -1, 'Product Details')
        rbox1 = wx.StaticBoxSizer(self.details_box, wx.VERTICAL)
        
        #--#
        dbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.id_label = wx.StaticText(self, -1, 'Product ID', size=(180, -1))
        self.id_label.SetFont(font_2)
        self.id_number = wx.TextCtrl(self, -1, size = (200, -1),
                                     style=wx.TE_READONLY|wx.TE_CENTER)
        self.id_number.SetFont(font_4)
        dbox1.Add(self.id_label, 0, wx.RIGHT|wx.TOP, 7)
        dbox1.Add(self.id_number, 1)
        rbox1.Add(dbox1, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10)
        
        #--#
        dbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.item_label = wx.StaticText(self, -1, 'Product', size=(180, -1))
        self.item_label.SetFont(font_2)
        self.item = wx.TextCtrl(self, -1, size = (200, -1),
                                     style=wx.TE_READONLY|wx.TE_CENTER)
        self.item.SetFont(font_4)
        dbox2.Add(self.item_label, 0, wx.RIGHT|wx.TOP, 7)
        dbox2.Add(self.item, 1)
        rbox1.Add(dbox2, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10)
        
        #--#
        dbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.price_label = wx.StaticText(self, -1, 'Price', size=(180, -1))
        self.price_label.SetFont(font_2)
        self.price = wx.TextCtrl(self, -1, size = (200, -1),
                                     style=wx.TE_READONLY|wx.TE_CENTER)
        self.price.SetFont(font_4)
        dbox3.Add(self.price_label, 0, wx.RIGHT|wx.TOP, 7)
        dbox3.Add(self.price, 1)
        rbox1.Add(dbox3, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10)
        
        #--#
        dbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.bulk_label = wx.StaticText(self, -1, 'Bulk Item', size=(180, -1))
        self.bulk_label.SetFont(font_2)
        self.bulk = wx.TextCtrl(self, -1, size = (200, -1), 
                                style=wx.TE_READONLY|wx.TE_CENTER)
        self.bulk.SetFont(font_4)
        dbox4.Add(self.bulk_label, 0, wx.RIGHT|wx.TOP, 7)
        dbox4.Add(self.bulk, 1)
        rbox1.Add(dbox4, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10)
        
        #--#
        rbox1.Add((-1, 10))
        
        vsizer2.Add(rbox1, 0, wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        self.options_box = wx.StaticBox(self, -1, 'Inventory Options')
        rbox2 = wx.StaticBoxSizer(self.options_box, wx.VERTICAL)
        
        #--#
        obox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.add_product_btn = wx.Button(self, -1, 'Add Product')
        self.add_product_btn.SetFont(font_2)
        obox1.Add(self.add_product_btn, 1, wx.LEFT|wx.RIGHT, 20)
        rbox2.Add(obox1, 0, wx.EXPAND|wx.TOP, 20)
        
        #--#
        obox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.edit_product_btn = wx.Button(self, -1, 'Edit Product')
        self.edit_product_btn.SetFont(font_2)
        obox2.Add(self.edit_product_btn, 1, wx.LEFT|wx.RIGHT, 20)
        rbox2.Add(obox2, 0, wx.EXPAND|wx.TOP, 20)
        rbox2.Add((-1, 20))
        
        vsizer2.Add(rbox2, 0, wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        endSizer.Add(vsizer2, 3, wx.EXPAND)
        self.SetSizer(endSizer)
        

        #------------------------------------------------------------------
        # Creates the panel objects
        #------------------------------------------------------------------
        self.db = mpos_db.MPOS_DB()
        self.config = config.Configuration()
        self.c_symbol = self.config.cCurrency()[0]
        self.c_dec = self.config.cCurrency()[1]
        
        #------------------------------------------------------------------
        # Bindings
        #------------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.add_product_btn)
        self.Bind(wx.EVT_BUTTON, self.OnEdit, self.edit_product_btn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.product_lc)
        self.search_bar.Bind(wx.EVT_TEXT, self.OnSearch)
        self.search_bar.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel)
        
        self.PListRefresh()
        self.Language()
        
    #----------------------------------------------------------------------
    # Function Definitions
    #----------------------------------------------------------------------
    def OnAdd(self, evt):
        self.dlg_l1 = ''
        self.Language()
        self.dlg = dlg_add.AddDlg(self, -1, title=self.dlg_l1)
        rslt = self.dlg.ShowModal()
        if rslt == wx.ID_OK:
            values = self.dlg.AddGetVals()
            if values:
                self.db.AddProduct(values)
        self.PListRefresh()
        
    #----------------------------------------------------------------------
    def PListRefresh(self):
        'Refreshes the Product List'
        self.product_table = self.db.AllProducts()
        self.product_lc.DeleteAllItems()
        
        # Add in table
        for i in range(0, len(self.product_table)):
            self.product_lc.InsertStringItem(i, str(self.product_table[i][0]))
            self.product_lc.SetStringItem(i, 1, self.product_table[i][1])
            ins = '%s %.'+str(self.c_dec)+'f'
            rslt = ins % (self.c_symbol, self.product_table[i][2])
            self.product_lc.SetStringItem(i, 2, rslt)
            if i % 2 == 0:
                self.product_lc.SetItemBackgroundColour(i, wx.LIGHT_GREY)
        self.product_lc.Select(0, 0)
        
    #----------------------------------------------------------------------
    def OnSelect(self, evt):
        self.row = self.product_lc.GetFocusedItem()
        self.selected_info = []
        for column in range(3):
            item = self.product_lc.GetItem(self.row, column)
            self.selected_info.append(item.GetText())
        # Find out if the product is sold in bulk
        bulk = self.db.GetBulk(self.selected_info[0])
        if bulk == 1:
            self.bulk.SetValue('Yes')
        else:
            self.bulk.SetValue('No')
        
        # Put the info into the Product Information panel
        self.id_number.SetValue(self.selected_info[0])
        self.item.SetValue(self.selected_info[1])
        self.price.SetValue(self.selected_info[2])
        
    #----------------------------------------------------------------------
    def OnEdit(self, evt):
        # Create the EditDlg instance
        self.dlg_l2 = ''
        self.Language()
        self.dlg = dlg_edit.EditDlg(self, -1, title=self.dlg_l2)
        
        # Get the information of the currently selected product
        self.row = self.product_lc.GetFocusedItem()
        if self.row == -1: self.row = 0
        self.selected_info = []
        for column in range(3):
            item = self.product_lc.GetItem(self.row, column)
            self.selected_info.append(item.GetText())
        price = self.selected_info[2]
        
        sp_index = price.index(' ')
        price = price[sp_index+1:]
        self.selected_info[2] = price
        
        # Get the bulk boolean from the database
        bulk = self.db.GetBulk(self.selected_info[0])
        self.selected_info.append(bulk)
        
        # Transfer the product values to the Edit Dialog
        self.dlg.SetValues(self.selected_info)
        
        self.user_inpt = self.dlg.ShowModal()
        
        if self.user_inpt != wx.ID_CANCEL:
            self.new_info = self.dlg.GetValues()
            if self.new_info:
                self.selected_info[1] = self.new_info[0]
                self.selected_info[2] = self.new_info[1]
                self.selected_info[3] = self.new_info[2]
                # print self.selected_info
                self.db.EditProduct(self.selected_info)
        self.search_bar.SetValue('')
        self.PListRefresh()
        self.product_lc.Select(0, 0)
        
    #----------------------------------------------------------------------
    def OnSearch(self, evt):
        '''
        This performs a dynamic search of the products table using the 
        values entered in the searc bar.'''
        try:    
            # Create a list of the terms entered in the search bar
            self.search_text = (self.search_bar.GetValue()).split()
            
            # Identify any prices in the search apply SQL formatting accordingly
            accept = list(string.digits) + ['.']
            for i in range(0, len(self.search_text)):
                term = self.search_text[i]
                price_type = True
                for ch in term:
                    if ch not in accept:
                        price_type = False
                        break
                if not price_type:
                    index = self.search_text.index(term)
                    self.search_text[index] = "'%" + term + "%'"
                else:
                    self.search_text.append("'%" + term + "%'")
                    
            # Pass the list to the pSearch function in mpos_db.py
            self.product_table = self.db.productSearch(self.search_text)
            
            # Add in table
            self.product_lc.DeleteAllItems()
            for i in range(0, len(self.product_table)):
                self.product_lc.InsertStringItem(i, str(self.product_table[i][0]))
                self.product_lc.SetStringItem(i, 1, self.product_table[i][1])
                
                ins = '%s %.'+str(self.c_dec)+'f'
                rslt = ins % (self.c_symbol, self.product_table[i][2])
                self.product_lc.SetStringItem(i, 2, rslt)
                
                if i % 2 == 0:
                    self.product_lc.SetItemBackgroundColour(i, wx.LIGHT_GREY)
            self.product_lc.Select(0, 0)
        
        except IndexError, e: # This occurs when the search bar is empty
            self.PListRefresh()
            
    #----------------------------------------------------------------------
    def ConfigUpdate(self):
        self.c_symbol = (self.config.cCurrency()[0])
        self.c_dec = self.config.cCurrency()[1]
        self.OnSearch(None)
        self.product_lc.Language()
        self.Language()
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the language'
        ids = 32, 33, 34, 17, 18, 7, 35, 5, 13, 81
        words = mpos_utility.lang(ids)
        self.title.SetLabel(words[0])
        self.search_label.SetLabel(words[1])
        self.details_box.SetLabel(words[2])
        self.id_label.SetLabel(words[3])
        self.item_label.SetLabel(words[4])
        self.price_label.SetLabel(words[5])
        self.options_box.SetLabel(words[6])
        self.add_product_btn.SetLabel(words[7])
        self.edit_product_btn.SetLabel(words[8])
        self.dlg_l1, self.dlg_l2 = words[-3:-1]
        self.bulk_label.SetLabel(words[-1])
        
    #----------------------------------------------------------------------
    def OnSearchCancel(self, evt):
        '''When the search bar's cancel button is pressed, this method will
        clear the value and reset the product list.'''
        self.search_bar.SetValue('')
        self.PListRefresh()
        