#! /usr/bin/python

# encoding: -*- utf-8 -*-

# mpos_panels.py

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

# Defines the POS_Panel

import wx
import string
from lc_mpos import *
import mpos_db
import config
import dlg_pos_addItem
import mpos_utility

class POS_Panel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(POS_Panel, self).__init__(parent, *args, **kwargs)
        
        # Set the fonts for the panel
        #------------------------------------------------------------------
        font_1 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_4 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        font_5 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD)
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
        self.title = wx.StaticText(self, -1, 'Point of Sale')
        self.title.SetFont(font_1)
        lbox1.Add(self.title, 0)
        vsizer1.Add(lbox1, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        lbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.search_label = wx.StaticText(self, -1, 'Search'+': ')
        self.search_label.SetFont(font_2)
#        self.search_bar = wx.TextCtrl(self, -1)
        self.search_bar = wx.SearchCtrl(self, -1)
        self.search_bar.ShowCancelButton(True)
        self.search_bar.ShowSearchButton(False)
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
        vsizer2.Add((-1, 30))
        #------------------------------------------------------------------
        rbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.receipt_label = wx.StaticText(self, -1, 'Receipt')
        self.receipt_label.SetFont(font_3)
        self.receipt_num = wx.TextCtrl(self, -1, style = wx.TE_READONLY|\
                                            wx.TE_CENTER)
        rbox1.Add(self.receipt_label, 0, wx.TOP, 5)
        rbox1.Add(self.receipt_num, 1, wx.LEFT|wx.RIGHT, 75)
        vsizer2.Add(rbox1, 0, wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        rbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sepLine1 = wx.StaticLine(self, -1)
        rbox2.Add(self.sepLine1, 1)
        vsizer2.Add(rbox2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        
        #------------------------------------------------------------------
        rbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.receipt_lc = ReceiptLC(self, -1, style=wx.LC_REPORT|\
                                    wx.LC_VRULES|wx.BORDER_DEFAULT|wx.LC_HRULES)
        rbox3.Add(self.receipt_lc, 1, wx.EXPAND)
        vsizer2.Add(rbox3, 4, wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        self.static_box = wx.StaticBox(self, -1, 'Sales Summary')
        rbox4 = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)
        
        # subbox1 will hold the total label and amount
        subbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.subtotal_label = wx.StaticText(self, -1, 'Sub Total')
        self.subtotal_label.SetFont(font_4)
        self.subtotal_amount = wx.TextCtrl(self, -1, 
                                           style=wx.TE_READONLY|wx.TE_RIGHT)
        self.subtotal_amount.SetFont(font_4)
        subbox1.Add(wx.StaticText(self, -1, ''), 2)
        subbox1.Add(self.subtotal_label, 2, wx.TOP|wx.RIGHT, 5)
        subbox1.Add(self.subtotal_amount, 2)
        rbox4.Add(subbox1, 0, wx.EXPAND|wx.ALL, 10)
        
        #--#
        subbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.tax_label = wx.StaticText(self, -1, 'Sales Tax')
        self.tax_amount = wx.TextCtrl(self, -1, 
                                           style=wx.TE_READONLY|wx.TE_RIGHT)
        self.tax_label.SetFont(font_2)
        self.tax_amount.SetFont(font_2)
        subbox2.Add(wx.StaticText(self, -1, ''), 2)
        subbox2.Add(self.tax_label, 2, wx.TOP|wx.RIGHT, 5)
        subbox2.Add(self.tax_amount, 2)
        rbox4.Add(subbox2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        #--#
        subbox3 = wx.BoxSizer(wx.HORIZONTAL)
        subbox3.Add(wx.StaticText(self, -1, ''), 2)
        subbox3.Add(wx.StaticLine(self, -1), 4)
        rbox4.Add(subbox3, 0, wx.EXPAND|wx.TOP, 10)
        
        #--#
        subbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.total_label = wx.StaticText(self, -1, 'Total')
        self.total_amount = wx.TextCtrl(self, -1, 
                                        style=wx.TE_READONLY|wx.TE_RIGHT)
        self.total_label.SetFont(font_5)
        self.total_amount.SetFont(font_5)
        subbox4.Add(wx.StaticText(self, -1, ''), 2)
        subbox4.Add(self.total_label, 2, wx.TOP|wx.RIGHT, 5)
        subbox4.Add(self.total_amount, 2)
        rbox4.Add(subbox4, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        #--#s
        vsizer2.Add(rbox4, 2, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        #------------------------------------------------------------------
        rbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.complete_btn = wx.Button(self, -1, "Complete Transaction",
                                      size=(-1, 100))
        self.complete_btn.SetFont(font_4)
        self.cancel_btn = wx.Button(self, -1, "Cancel",
                                       size=(-1, 100))
        self.cancel_btn.SetFont(font_4)
        rbox5.Add(self.cancel_btn, 1, wx.RIGHT, 10)
        rbox5.Add(self.complete_btn, 2)
        vsizer2.Add(rbox5, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        vsizer2.Add((-1, 5))
                                    
        #------------------------------------------------------------------
        endSizer.Add(vsizer2, 5, wx.EXPAND)
        self.SetSizer(endSizer)
        
        # Set up complimentary objects
        #------------------------------------------------------------------
        self.db = mpos_db.MPOS_DB()
        self.config = config.Configuration()
        self.c_symbol = self.config.cCurrency()[0]
        self.c_dec = self.config.cCurrency()[1]
        self.thous_sep = self.config.ThousandsSep()
        
        #------------------------------------------------------------------
        self.m1, self.t1, self.m2, self.t2, self.btn_l1 = '', '', '', '', ''
        self.btn_l2, self.r_label, self.t_label = '', '', ''
        self.Language()
        
        #-----------------------------------------------------------------
        self.PListRefresh()
        self.SetReceiptNo()
        self.SaleInfoSetup()
        self.edit_mode = False
        self.OnCancel(None)
        
        # Bindings
        #------------------------------------------------------------------
        self.search_bar.Bind(wx.EVT_TEXT, self.OnSearch)
        self.product_lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.receipt_lc.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRClick)
        self.receipt_lc.Bind(wx.EVT_LEFT_DCLICK, self.OnEdit)
        self.Bind(wx.EVT_BUTTON, self.OnComplete, self.complete_btn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_btn)
        self.search_bar.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel)
        
    #----------------------------------------------------------------------
    # Function Definitions
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
        
        
    #----------------------------------------------------------------------
    def OnSearch(self, evt):
        '''
        This performs a dynamic search of the products table using the 
        values entered in the search bar.'''
        
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
#            self.product_lc.Focus(0)
        
        except IndexError, e: # This occurs when the search bar is empty
            self.PListRefresh()    
        evt.Skip()
        
    #----------------------------------------------------------------------    
    def OnSelect(self, evt):
        'Brings up the dlg_pos_addItem dialog'
        dlg = dlg_pos_addItem.POS_AddItem(self, -1, 'miniPOS')
        # Get the info from the highlighted Item
        self.row = self.product_lc.GetFocusedItem()
        self.selected_info = []
        for column in range(3):
            item = self.product_lc.GetItem(self.row, column)
            self.selected_info.append(item.GetText())
        # Extract the float from the price column to pass
        self.selected_info[2] = float(((self.selected_info[2]).split(' '))[-1])
        # Set the info for the dlg
        dlg.SetInfo(self.selected_info)
        rslt = dlg.ShowModal()
        if rslt != wx.ID_CANCEL:
            self.input = dlg.SendInfo()

            if self.input[2] != 0 and not self.input[2]:
                self.m1, self.t1 = '', ''
                self.Language()
                wx.MessageBox(self.m1, self.t1)
                return False
            if not self.input[3] or self.input[3] == '0':
                self.m1, self.t1 = '', ''
                self.Language()
                wx.MessageBox(self.m1, self.t1)
                return False
        else:
            return False
        
        # Get the index #s, product IDs and prices from the receipt LC
        receipt = []
        item_count = self.receipt_lc.GetItemCount()
        for i in range(item_count):
            index = i
            prod_ID = self.receipt_lc.GetItem(i, 0).GetText()
            prod_price = (self.receipt_lc.GetItem(i, 2).GetText()).split(' ')
            prod_price = float(prod_price[-1])
            receipt.append((index, prod_ID, prod_price,))
            
        # Check to see if the product has been added at the same price
        match_boolean = False
        for item in receipt:
            if self.input[0] == item[1] and self.input[2] == item[2]:
                match_boolean = True
                insert_point = item[0]
                break
        
        # Check if the item was already added to the receipt
        row_count = self.receipt_lc.GetItemCount()
        productId_list = []
        for i in range(row_count):
            item = self.receipt_lc.GetItem(i, 0)
            productId_list.append(item.GetText())

        if not match_boolean:
            # Add the returned value to the Receipt list control
            i_point = self.receipt_lc.GetItemCount()
            self.receipt_lc.InsertStringItem(i_point, self.input[0])
            self.receipt_lc.SetStringItem(i_point, 1, self.input[1])
            ins = '%s %.'+self.c_dec+'f'
            rslt = ins % (self.c_symbol, self.input[2])
            self.receipt_lc.SetStringItem(i_point, 2, rslt)
            self.receipt_lc.SetStringItem(i_point, 3, self.input[3])
        else:
            i_point = insert_point
            item = self.receipt_lc.GetItem(i_point, 3)
            start_qty = float(item.GetText())
            self.input[3] = str(float(self.input[3]) + start_qty) 
            ins = '%s %.'+self.c_dec+'f'
            rslt = ins % (self.c_symbol, self.input[2])
            self.receipt_lc.SetStringItem(i_point, 2, rslt)
            self.receipt_lc.SetStringItem(i_point, 3, self.input[3])
            
        # Calculate the Price x Quantity
        price = float(self.input[2])
        quantity = float(self.input[3])
        amount = price * quantity
        ins = '%s %.'+self.c_dec+'f'
        rslt = ins % (self.c_symbol, amount)
        self.receipt_lc.SetStringItem(i_point, 4, rslt)
        self.Total()
        
        # Reset the search bar
#        self.search_bar.SetValue('')
#        self.PListRefresh()
        
    #----------------------------------------------------------------------
    def OnRClick(self, evt):
        'Deletes an item from the receipt if it is right clicked'
        row = self.receipt_lc.GetFocusedItem()
        if not self.edit_mode:
            self.receipt_lc.DeleteItem(row)
        else:
            self.receipt_lc.SetStringItem(row, 3, '0')
            rslt = ('%s 0') % self.c_symbol
            self.receipt_lc.SetStringItem(row, 4, rslt)
        self.Total()
        
    #----------------------------------------------------------------------
    def OnEdit(self, evt):
        'Opens up the edit dialog if an item in the receipt_lc is selected'
        dlg = dlg_pos_addItem.POS_AddItem(self, -1, 'miniPOS')
        # Get the info from the highlighted Item
        self.row = self.receipt_lc.GetFocusedItem()
        self.selected_info = []
        for column in range(4):
            item = self.receipt_lc.GetItem(self.row, column)
            self.selected_info.append(item.GetText())
        # Extract the float from the price column to pass
        self.selected_info[2] = float(((self.selected_info[2]).split(' '))[-1])
        
        dlg.SetInfo2(self.selected_info)
        rslt = dlg.ShowModal()
        if rslt != wx.ID_CANCEL:
            self.input = dlg.SendInfo()
        
            if self.input[2] != 0 and not self.input[2]:
                self.m1, self.t1 = '', ''
                self.Language()
                wx.MessageBox(self.m1, self.t1)
                return False
            if not self.input[3] or self.input[3] == '0':
                self.m1, self.t1 = '', ''
                self.Language()
                wx.MessageBox(self.m1, self.t1)
                return False
        else:
            return False
            
        # Add the returned value to the Receipt list control
        i_point = self.receipt_lc.GetFocusedItem()
        self.receipt_lc.SetStringItem(i_point, 1, self.input[1])
        ins = '%s %.'+self.c_dec+'f'
        rslt = ins % (self.c_symbol, self.input[2])
        self.receipt_lc.SetStringItem(i_point, 2, rslt)
        self.receipt_lc.SetStringItem(i_point, 3, self.input[3])
        
        # Calculate the Price x Quantity
        price = float(self.input[2])
        quantity = float(self.input[3])
        amount = price * quantity
        ins = '%s %.'+self.c_dec+'f'
        rslt = ins % (self.c_symbol, amount)
        self.receipt_lc.SetStringItem(i_point, 4, rslt)
        self.Total()
        
    #----------------------------------------------------------------------
    def Total(self):
        'Get all of the amounts from the receipt list control'
        row_count = self.receipt_lc.GetItemCount()
        amounts = []
        for i in range(0, row_count):
            item = self.receipt_lc.GetItem(i, 4)
            amounts.append(float(((item.GetText()).split(' '))[-1]))
        sum = 0
        for num in amounts:
            sum += num
        
        if self.salesTax_on:
            ins = '%s %.'+self.c_dec+'f'
            rslt = ins % (self.c_symbol, sum)
            rslt = self.TSep(rslt)
            self.subtotal_amount.SetValue(rslt)
            
            tax = float(sum) * (self.sales_tax/100)
            rslt = ins % (self.c_symbol, tax)
            rslt = self.TSep(rslt)
            self.tax_amount.SetValue(rslt)
            
            total = sum + tax
            rslt = ins % (self.c_symbol, total)
            rslt = self.TSep(rslt)
            self.total_amount.SetValue(rslt)
        else:
            self.subtotal_amount.SetValue('0')
            self.tax_amount.SetValue('0')
            ins = '%s %.'+self.c_dec+'f'
            rslt = ins % (self.c_symbol, sum)
            rslt = self.TSep(rslt)
            self.total_amount.SetValue(rslt)
    
    #----------------------------------------------------------------------    
    'Commit the transaction to the Sales and SaleItems tables'
    def OnComplete(self, evt):
        # Get item count
        item_count = self.receipt_lc.GetItemCount()
        if item_count != 0:
            # Get the total amount
            amount = ((self.total_amount.GetValue()).split(' '))[-1]
            amount = float(self.TotalRestore(amount))
            
            # Get the productIds and qantities from the receipt_lc
            receipt_info = []
            r_len = self.receipt_lc.GetItemCount()
            for i in range(r_len):
                item = self.receipt_lc.GetItem(i, 0)
                prod_id = item.GetText()
                item = self.receipt_lc.GetItem(i, 2)
                sale_price = item.GetText()
                sale_price = (sale_price.split(' '))[-1]
                item = self.receipt_lc.GetItem(i, 3)
                quantity = item.GetText()
                receipt_info.append((prod_id, sale_price, quantity))
            
            if not self.edit_mode:
                # Record the sale and get the saleId
                saleId = self.db.RecordSale(amount)
                if not saleId:
                    # If there's a read/write problem, do nothing
                    return False
                # Send the productId, SaleId and quantities to be entered in
                #       the soldItems table
                self.db.RecSaleItems(saleId, receipt_info)
                self.receipt_lc.DeleteAllItems()
                self.SetReceiptNo()
           
            else:
                # Get the Sale Id and Amount
                saleId = ((self.receipt_num.GetValue()).split(' '))[-1]
                amount = ((self.total_amount.GetValue()).split(' '))[-1]
                # Delete the original record in the database
                self.db.DeleteSIRecord(saleId)
                # Update the sale record
                amount = mpos_utility.UnTSep(amount)
                self.db.UpdateSale(saleId, float(amount))
                self.db.RecSaleItems(saleId, receipt_info)

            # Reset the POS screen
            self.OnCancel(None)
            
        else:
            self.m2, self.t2 = '', ''
            self.Language()
            wx.MessageBox(self.m2, self.t2)
            self.OnCancel(None)
            
    #----------------------------------------------------------------------
    def OnCancel(self, evt):
        if not self.edit_mode:
            pass
        else:
            self.SetReceiptNo()
            self.btn_l1 = ''
            self.Language()
            self.complete_btn.SetLabel(self.btn_l1)
        
        self.receipt_lc.DeleteAllItems()
        self.edit_mode = False 
        rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, 0.0)
        self.subtotal_amount.SetValue(rslt)
        self.tax_amount.SetValue(rslt)
        self.total_amount.SetValue(rslt)
    
    #----------------------------------------------------------------------
    def SetReceiptNo(self):
        'Sets the receipt number label to the next receiptId number'
        next_saleId = self.db.ReceiptNo()
        self.r_label = ''
        self.Language()
        self.receipt_num.SetValue(self.r_label + ':  ' + str(next_saleId))
    
    #----------------------------------------------------------------------
    def EditModeToggle(self, saleId, receipt_table):
        'Edit a sale record using the POS panel'
        self.btn_l2 = ''
        self.Language()
        self.complete_btn.SetLabel(self.btn_l2)
        self.edit_mode = True 
        self.r_label = ''
        self.Language()
        self.receipt_num.SetValue(self.r_label + ':  ' + saleId)
        
        # Add in receipt table for editing
        self.receipt_lc.DeleteAllItems()
        for i in range(len(receipt_table)):
            self.receipt_lc.InsertStringItem(i, str(receipt_table[i][0]))
            self.receipt_lc.SetStringItem(i, 1, str(receipt_table[i][1]))
            x = ('%s %.'+self.c_dec+'f') % (self.c_symbol, receipt_table[i][2])
            self.receipt_lc.SetStringItem(i, 2, x)
            self.receipt_lc.SetStringItem(i, 3, str(receipt_table[i][3]))
            x = ('%s %.'+self.c_dec+'f') % (self.c_symbol, receipt_table[i][4])
            self.receipt_lc.SetStringItem(i, 4, x)
            
        self.Total()
    
        
    #----------------------------------------------------------------------
    def TotalRestore(self, total):
        total = list(total)
        for i in total:
            if i == ',':
                del total[total.index(i)]
        return ''.join(total)
            
    #----------------------------------------------------------------------
    def SaleInfoSetup(self):
        'Sets up the Sales Info box based on the config info for sales tax.'
        config_info = self.config.SalesTaxInfo()
        if config_info[0] != '1':
            self.salesTax_on = False
        else:
            self.salesTax_on = True
         
        if self.salesTax_on:
            self.subtotal_label.Enable()
            self.subtotal_amount.Enable()
            self.tax_label.Enable()
            self.tax_amount.Enable()
            self.sales_tax = float(config_info[1])
            self.t_lable = ''
            self.Language()
            self.tax_label.SetLabel(self.t_label+' '+str(self.sales_tax)+' %')
        else:
            self.subtotal_label.Disable()
            self.subtotal_amount.Disable()
            self.tax_label.Disable()
            self.tax_amount.Disable()
            self.subtotal_amount.SetValue('0')
            self.tax_amount.SetValue('0')
            self.sales_tax = 0.0
    
    #----------------------------------------------------------------------
    def TSep(self, amount):
        'Adds in thousands separator, if toggled'
        if self.thous_sep:
            amount = amount.split(' ')
            pFix = amount[0]
            amount = amount[-1]
            if '.' in amount: 
                amount = amount.split('.')
                sfx = '.' + amount[-1]
                amount = amount[0]
            else:
                sfx = ''
            tSep_cnt = 0        # counts the number of tseps added
            tSep_lst = []       # tells where to insert the tseps
            amount = list(amount)
            amount.reverse()
            for i in range(1, len(amount)):
                if i%3 == 0:
                    tSep_lst.append(i + tSep_cnt)
                    tSep_cnt += 1
            for i in tSep_lst:
                amount.insert(i, ',')
            amount.reverse()
            return pFix + ' ' + ''.join(amount) + sfx
        else:
            return amount
            
    #----------------------------------------------------------------------
    def ConfigUpdate(self):
        'Updates the pages after the configuration file is changed'
        self.c_symbol = self.config.cCurrency()[0]
        self.c_dec = self.config.cCurrency()[1]
        self.thous_sep = self.config.ThousandsSep()
        # Update the product list control
        self.PListRefresh()
        # Refresh the current receiept
        row_count = self.receipt_lc.GetItemCount()
        for i in range(row_count):
            # Refresh Prices
            price = ((self.receipt_lc.GetItem(i, 2)).GetText()).split(' ')
            price = float(price[-1])
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, price)
            self.receipt_lc.SetStringItem(i, 2, rslt)
            # Refresh Amounts
            amount = ((self.receipt_lc.GetItem(i, 4)).GetText()).split(' ')
            amount = float(amount[-1])
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, amount)
            self.receipt_lc.SetStringItem(i, 4, rslt)
        # Refresh the total amount
        self.SaleInfoSetup()
        self.Total()
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the language.'
        objects1 = [self.title, self.search_label, 
                  self.receipt_label, self.static_box, 
                  self.subtotal_label, self.tax_label,
                  self.total_label, self.complete_btn,
                  self.cancel_btn]
        ids1 = 1, 33, 36, 37, 38, 40, 39, 41, 42
        words = mpos_utility.lang(ids1)
        for object, word in zip(objects1, words):
            object.SetLabel(word)

        ids2 = 43, 8, 45, 44, 41, 47, 46, 40
        words = mpos_utility.lang(ids2)
        self.m1, self.t1, self.m2, self.t2 = words[:4]
        self.btn_l1, self.btn_l2 = words[4:6]
        self.r_label, self.t_label = words[6:]
        
    #----------------------------------------------------------------------
    def OnSearchCancel(self, evt):
        '''When the search bar Cancel button is pressed, this function 
        clears the search bar value and updates the product list.'''
        self.search_bar.SetValue('')
        self.PListRefresh()
        
    