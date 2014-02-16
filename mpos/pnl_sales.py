#! /usr/bin/python

# encoding: -*- utf-8 -*-

# sale_panel.py

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

# This panel displays the sales records for Mini POS

import wx
import string
from lc_mpos import *
import mpos_db
import config
import dlg_cal
import time
import datetime
import mpos_utility
import sys
import mpos_print

ID_EDIT_RECEIPT = wx.NewId()

class Sales_Panel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(Sales_Panel, self).__init__(parent, *args, **kwargs)
        
        # Set fonts for the panel
        #------------------------------------------------------------------
        font_1 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_4 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.SetBackgroundColour(wx.WHITE)
        
        # The endSizer will hold the left and right box sizers
        #------------------------------------------------------------------
        endSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Language
        #------------------------------------------------------------------
        self.day, self.week, self.month, self.year = '', '', '', ''
        self.d1, self.d2, self.w1, self.m1, self.t1 = '', '', '', '', ''
        self.Language2()
        
        #------------------------------------------------------------------
        # vsizer1 will hold the widgets for the left side
        #------------------------------------------------------------------
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        
        #------------------------------------------------------------------
        lbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sales_label = wx.StaticText(self, wx.ID_EDIT, 'Sales Records')
        self.sales_label.SetFont(font_1)
        lbox1.Add(self.sales_label, 0)
        vsizer1.Add(lbox1, 0, wx.TOP|wx.LEFT, 5)
        
        #------------------------------------------------------------------
        self.sales_box = wx.StaticBox(self, -1, 'Period Sales Records')
        lbox2 = wx.StaticBoxSizer(self.sales_box, wx.VERTICAL)
        #--#
        a_box1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sales_lc = SalesLC(self, -1, 
                                style=wx.LC_REPORT|wx.LC_VRULES|\
                                    wx.BORDER_DEFAULT)
        a_box1.Add(self.sales_lc, 1, wx.EXPAND)
        lbox2.Add(a_box1, 1, wx.EXPAND|wx.ALL, 5)
        vsizer1.Add(lbox2, 4, wx.EXPAND)
        
        #--#
        vsizer1.Add((-1, 10))
        
        #------------------------------------------------------------------
        self.sale_items_box = wx.StaticBox(self, -1, 'Sale Record Receipt')
        lbox3 = wx.StaticBoxSizer(self.sale_items_box, wx.VERTICAL)
        #--#
        self.receipt_lc = RecReviewLC(self, -1, 
                                    style=wx.LC_REPORT|wx.LC_VRULES|\
                                        wx.LC_HRULES|wx.BORDER_DEFAULT)
        b_box = wx.BoxSizer(wx.HORIZONTAL)
        b_box.Add(self.receipt_lc, 1, wx.EXPAND)
        lbox3.Add(b_box, 1, wx.EXPAND|wx.ALL, 5)
        vsizer1.Add(lbox3, 5, wx.EXPAND)
        
        #------------------------------------------------------------------
        lbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.edit_receipt_btn = wx.Button(self, ID_EDIT_RECEIPT, 
                                          'Edit Receipt')
        self.print_receipt_btn = wx.Button(self, -1, 'Print Receipt')
        self.edit_receipt_btn.SetFont(font_4)
        self.print_receipt_btn.SetFont(font_4)
        lbox4.Add(self.edit_receipt_btn, 1, wx.RIGHT|wx.LEFT, 10)
        lbox4.Add(self.print_receipt_btn, 1, wx.RIGHT, 10)
        vsizer1.Add(lbox4, 0, wx.EXPAND|wx.ALL, 5)
    
        #------------------------------------------------------------------
        # vsizer2 - Holds the gadgets for the right side
        #------------------------------------------------------------------
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        
        #------------------------------------------------------------------
        rbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sales_period_label = wx.StaticText(self, -1, 
                                                'Choose Sales Period'+' -')
        self.sales_period_label.SetFont(font_3)
        periods = [self.day, self.week, self.month, self.year]
        self.period_choice = wx.ComboBox(self, -1, choices=periods,
                                         style = wx.CB_READONLY)
        rbox1.Add(self.sales_period_label, 0, wx.TOP, 5)
        rbox1.Add((10, -1))
        rbox1.Add(self.period_choice, 0)
        vsizer2.Add(rbox1, 0, wx.ALIGN_CENTER_HORIZONTAL|\
                    wx.TOP|wx.RIGHT|wx.LEFT, 5)
        
        #--#
        vsizer2.Add((-1, 10))
        vsizer2.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        vsizer2.Add((-1, 10))
        
        #------------------------------------------------------------------
        rbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.st_date_btn = wx.Button(self, -1, 'Start Date')
        self.st_date_btn.SetFont(font_2)
        self.st_date = wx.TextCtrl(self, -1, '-', 
                                   style=wx.TE_CENTER|wx.TE_READONLY)
        self.st_date.SetFont(font_2)
        self.end_date_btn = wx.Button(self, -1, 'End Date')
        self.end_date_btn.SetFont(font_2)
        self.end_date = wx.TextCtrl(self, -1, '-', 
                                    style=wx.TE_CENTER|wx.TE_READONLY)
        self.end_date.SetFont(font_2)
        rbox2.Add(self.st_date_btn, 0, wx.RIGHT, 5)
        rbox2.Add(self.st_date, 1, wx.RIGHT, 20)
        rbox2.Add(self.end_date_btn, 0, wx.RIGHT, 5)
        rbox2.Add(self.end_date, 1)
        vsizer2.Add(rbox2, 0, wx.EXPAND|wx.ALL, 5)
        
        #--#
        vsizer2.Add((-1, 10))
        vsizer2.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        vsizer2.Add((-1, 10))
        
        #------------------------------------------------------------------
        self.summary_sbox = wx.StaticBox(self, -1, 'Sales Summary')
        rbox3 = wx.StaticBoxSizer(self.summary_sbox, wx.VERTICAL)
        
        #--#
        rbox3_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.subtotal_label = wx.StaticText(self, -1, 'Sub-total'+'- ', 
                                               size = (200, -1))        
        self.subtotal_label.SetFont(font_2)
        self.subtotal_amount = wx.TextCtrl(self, -1, size=(200, -1), 
                                       style=wx.TE_READONLY|wx.TE_CENTER)
        self.subtotal_amount.SetFont(font_2)
        rbox3_1.Add(self.subtotal_label, 0, wx.TOP|wx.RIGHT, 5)
        rbox3_1.Add(self.subtotal_amount, 0)
        rbox3.Add(rbox3_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        
        #--#
        rbox3_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sTax_label = wx.StaticText(self, -1, 'Sales Tax'+' -',
                                          size = (200, -1))
        self.sTax_label.SetFont(font_2)
        self.sTax_amount = wx.TextCtrl(self, -1, size=(200, -1),
                                       style=wx.TE_READONLY|wx.TE_CENTER)
        self.sTax_amount.SetFont(font_2)
        rbox3_2.Add(self.sTax_label, 0, wx.TOP|wx.RIGHT, 5)
        rbox3_2.Add(self.sTax_amount, 0)
        rbox3.Add(rbox3_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.LEFT, 10)
        
        #--#
        rbox3.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        #--#
        rbox3_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.total_label = wx.StaticText(self, -1, 'Total'+' -',
                                         size=(200, -1))
        self.total_label.SetFont(font_4)
        self.total_amount = wx.TextCtrl(self, -1, size=(200, -1),
                                        style=wx.TE_READONLY|wx.TE_CENTER)
        self.total_amount.SetFont(font_4)
        rbox3_3.Add(self.total_label, 0, wx.TOP|wx.RIGHT, 5)
        rbox3_3.Add(self.total_amount, 0)
        rbox3.Add(rbox3_3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        
        vsizer2.Add(rbox3, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5)
        
        #--#
        vsizer2.Add((-1, 10))
        
        #------------------------------------------------------------------
        self.product_sbox = wx.StaticBox(self, -1, 'Product Sales Summary')
        rbox4 = wx.StaticBoxSizer(self.product_sbox, wx.VERTICAL)
        
        #--#
        rbox4_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.search_label = wx.StaticText(self, -1, 'Search'+': ')
        self.search_label.SetFont(font_2)
        self.search_bar = wx.TextCtrl(self, -1)
        rbox4_1.Add(self.search_label, 0, wx.TOP|wx.RIGHT, 5)
        rbox4_1.Add(self.search_bar, 1)
        rbox4.Add(rbox4_1, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        
        #--#
        rbox4_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.product_lc = ReceiptLC(self, -1, style=wx.LC_REPORT|wx.LC_VRULES|\
                                    wx.BORDER_DEFAULT)
        rbox4_2.Add(self.product_lc, 1, wx.EXPAND)
        rbox4.Add(rbox4_2, 1, wx.EXPAND|wx.ALL, 5)
        
        #--#
        rbox4_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.print_prodList = wx.Button(self, -1, 'Print Product List')
        self.print_prodList.SetFont(font_4)
        rbox4_3.Add(self.print_prodList, 1, wx.LEFT|wx.RIGHT, 20)
        rbox4.Add(rbox4_3, 0, wx.EXPAND|wx.ALL, 10)
                                    
        vsizer2.Add(rbox4, 1, wx.EXPAND|wx.ALL, 5)

        #------------------------------------------------------------------
        endSizer.Add(vsizer1, 1, wx.EXPAND|wx.ALL, 5)
        endSizer.Add(vsizer2, 1, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        self.SetSizer(endSizer)
        
        # Initialize complementary object instances
        #------------------------------------------------------------------
        self.db = mpos_db.MPOS_DB()
        self.config = config.Configuration()
        self.c_symbol = self.config.cCurrency()[0]
        self.c_dec = self.config.cCurrency()[1]
        self.thous_sep = self.config.ThousandsSep()
        self.Language()
        
        # Panel Bindings
        #------------------------------------------------------------------
        self.st_date_btn.Bind(wx.EVT_BUTTON, self.OnStDate)
        self.end_date_btn.Bind(wx.EVT_BUTTON, self.OnEndDate)
        self.st_date.Bind(wx.EVT_LEFT_DCLICK, self.OnStDate)
        self.end_date.Bind(wx.EVT_LEFT_DCLICK, self.OnEndDate)
        #--#
        self.Bind(wx.EVT_COMBOBOX, self.OnPeriodSel, self.period_choice)
        self.sales_lc.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnSaleSelect)
        self.search_bar.Bind(wx.EVT_KEY_UP, self.OnSearch)
        self.Bind(wx.EVT_BUTTON, self.EditSaleRec)
        self.print_prodList.Bind(wx.EVT_BUTTON, self.OnPrintProdList)
        self.print_receipt_btn.Bind(wx.EVT_BUTTON, self.OnPrintReceipt)
        
        #------------------------------------------------------------------
        self.period_choice.SetValue(self.day)
        self.SetDates()
        self.SalesRecUpdate()
        self.ProductRecUpdate()
        
    #----------------------------------------------------------------------
    #                           PANEL FUNCTIONS
    #----------------------------------------------------------------------
    def OnStDate(self, evt):
        'Opens the calendar dialog for the user to select a start date'
        self.d1 = ''
        self.Language2()
        dlg = dlg_cal.Calendar(self, -1, self.d1)
        x = dlg.ShowModal()
        if x == wx.ID_OK:
            rslt = dlg.SendDate()
            if rslt:
                check = self.DateEval(rslt, self.end_date.GetValue())
                if check:
                    self.st_date.SetValue(rslt)
                    self.SalesRecUpdate()
                    self.ProductRecUpdate()
                    self.w1 = ''
                    self.Language2()
                    self.period_choice.SetValue(self.w1)
                else:
                    self.m1, self.t1 = '', ''
                    self.Language2()
                    wx.MessageBox(self.m1, self.t1)
                    self.period_choice.SetValue(self.day)
                    self.OnPeriodSel(None)
            else:
                return False
    
    #----------------------------------------------------------------------        
    def OnEndDate(self, evt):
        'Opens the calendar dialog for the user to select an end date'
        self.d2 = ''
        self.Language2()
        dlg = dlg_cal.Calendar(self, -1, 'End Date Select')
        x = dlg.ShowModal()
        if x == wx.ID_OK:
            rslt = dlg.SendDate()
            if rslt:
                check = self.DateEval(self.st_date.GetValue(), rslt)
                if check:
                    self.end_date.SetValue(rslt)
                    self.SalesRecUpdate()
                    self.ProductRecUpdate()
                    self.w1 = ''
                    self.Language2()
                    self.period_choice.SetValue(self.w1)
                else:
                    self.m1, self.t1 = '', ''
                    self.Language2()
                    wx.MessageBox(self.m1, self.t1)
                    self.period_choice.SetValue(self.day)
                    self.OnPeriodSel(None)
            else:
                return False
        
    #----------------------------------------------------------------------
    def SetDates(self):
        'Automatically sets the start and end dates to the current date'
        today = str(datetime.date.today())
        today = today.split('-')
        d, m, y = today[2], today[1], today[0]
        vals = (d, m, y)
        today = ('%s/%s/%s') % vals
        self.st_date.SetValue(today)
        self.end_date.SetValue(today)
        
    #----------------------------------------------------------------------
    def DateEval(self, date1, date2):
        'Checks that date 1 is the same or prior to date2'
        date1 = date1.split('/')
        date2 = date2.split('/')
        date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
        date2 = datetime.date(int(date2[2]), int(date2[1]), int(date2[0]))
        if date1 > date2:
            return False
        else:
            return True
    
    #----------------------------------------------------------------------
    def OnWeek(self):
        'Finds the date one week prior to today.'
        # Get the starting date using datetime
        today = datetime.date.today()
        week = datetime.timedelta(days=6)
        week_start = today - week
        week_start = str(week_start)
        # Change the YYYY-MM-DD format to DD/M/YYYY
        week_start = week_start.split('-')
        d, m, y = (week_start[2], week_start[1], week_start[0])
        vals = (d, m, y)
        week_start = ('%s/%s/%s') % vals
        self.SetDates()
        self.st_date.SetValue(week_start)
    
    #----------------------------------------------------------------------
    def OnMonth(self):
        'Finds the date one month prior to today'
        # Get the starting date using datetime
        today = datetime.date.today()
        month = datetime.timedelta(days=30)
        date = str(today-month)
        # Change the YYYY-MM-DD format to DD/M/YYYY
        date = date.split('-')
        d, m, y = date[2], date[1], date[0]
        vals = (d, m, y)
        date = ('%s/%s/%s') % vals
        self.SetDates()
        self.st_date.SetValue(date)
    
    #----------------------------------------------------------------------    
    def OnYear(self):
        'Finds the date one year prior to today'
        # Get the starting date using datetime
        today = datetime.date.today()
        year = datetime.timedelta(days=364)
        date = str(today-year)
        # Change the YYYY-MM-DD format to DD/M/YYYY
        date = date.split('-')
        d, m, y = date[2], date[1], date[0]
        vals = (d, m, y)
        date = ('%s/%s/%s') % vals
        self.SetDates()
        self.st_date.SetValue(date)
        
    #----------------------------------------------------------------------
    def OnPeriodSel(self, evt):
        # Get Selection
        period = self.period_choice.GetValue()#.encode('utf8')
        if period == self.day:
            self.SetDates()
        elif period == self.week:
            self.OnWeek()
        elif period == self.month:
            self.OnMonth()
        elif period == self.year:
            self.OnYear() 
        self.SalesRecUpdate()
        self.ProductRecUpdate()
        
    #----------------------------------------------------------------------
    def ZeroBGone(self, date):
        '''Because the db.SalesRecords and db.ProducRecUpdate functions
        use the time.time() format, they require that the time format
        excludes preceding zeros (01/01/2011) from the date format. This
        function gets rid of those function.'''
        date = date.split('/')
        day, month = date[0], date[1]
        if day[0] == '0': day = day[-1]
        if month[0] == '0': month = month[-1]
        date[0], date[1] = day, month
        return '/'.join(date)
        
    #----------------------------------------------------------------------
    def SalesRecUpdate(self):
        stDate = self.ZeroBGone(self.st_date.GetValue())
        endDate = self.ZeroBGone(self.end_date.GetValue())
        sales_table = self.db.SalesRecords(stDate, endDate)
        # Add the records to the sales_lc
        self.sales_lc.DeleteAllItems()
        for i in range(len(sales_table)):
            self.sales_lc.InsertStringItem(i, str(sales_table[i][0]))
            self.sales_lc.SetStringItem(i, 1, sales_table[i][1])
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, sales_table[i][2])
            self.sales_lc.SetStringItem(i, 2, rslt)
            if i % 2 == 0:
                self.sales_lc.SetItemBackgroundColour(i, wx.LIGHT_GREY)
        self.sales_lc.SetFocus()
        
    #----------------------------------------------------------------------
    def ProductRecUpdate(self):
        stDate = self.ZeroBGone(self.st_date.GetValue())
        endDate = self.ZeroBGone(self.end_date.GetValue())
        prod_table = self.db.ProductRecUpdate(stDate, endDate)
        total =  0
        self.product_lc.DeleteAllItems()
        for i in range(len(prod_table)):
            self.product_lc.InsertStringItem(i, str(prod_table[i][0]))
            self.product_lc.SetStringItem(i, 1, unicode(prod_table[i][1]))
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, prod_table[i][2])
            self.product_lc.SetStringItem(i, 2, rslt)
            self.product_lc.SetStringItem(i, 3, str(prod_table[i][3]))
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, prod_table[i][4])
            self.product_lc.SetStringItem(i, 4, rslt)
            total += prod_table[i][4]
            if i%2==0:
                self.product_lc.SetItemBackgroundColour(i, wx.LIGHT_GREY)
        
        self.Total()
        
    #----------------------------------------------------------------------
    def OnSaleSelect(self, evt):
        'Populates the receipt lc when a specific sale is selected'
        # Get the selected sale's Id
        self.row = self.sales_lc.GetFocusedItem()
        item = self.sales_lc.GetItem(self.row, 0)
        id = item.GetText()
        # Pass the id to the database and get the sale receipt
        rec_table = self.db.ReceiptSelect(id)
        if rec_table:
            self.receipt_lc.DeleteAllItems()
            for i in range(len(rec_table)):
                self.receipt_lc.InsertStringItem(i, unicode(rec_table[i][0]))
                rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, rec_table[i][1])
                self.receipt_lc.SetStringItem(i, 1, rslt)
                self.receipt_lc.SetStringItem(i, 2, str(rec_table[i][2]))
                rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, rec_table[i][3])
                self.receipt_lc.SetStringItem(i, 3, rslt)
                if i % 2 == 0:
                    self.receipt_lc.SetItemBackgroundColour(i, wx.LIGHT_GREY)
    
    #----------------------------------------------------------------------                
    def OnSearch(self, evt):
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
            stDate = self.st_date.GetValue()
            endDate = self.end_date.GetValue()
            product_table = self.db.productRecordSearch\
                (stDate, endDate, self.search_text)
            
            total = 0
            self.product_lc.DeleteAllItems()
            for i in range(len(product_table)):
                self.product_lc.InsertStringItem(i, str(product_table[i][0]))
                self.product_lc.SetStringItem(i, 1, product_table[i][1])
                x = ('%s %.'+self.c_dec+'f')%(self.c_symbol, product_table[i][2])
                self.product_lc.SetStringItem(i, 2, x)
                self.product_lc.SetStringItem(i, 3, str(product_table[i][3]))
                x = ('%s %.'+self.c_dec+'f')%(self.c_symbol, product_table[i][4])
                self.product_lc.SetStringItem(i, 4, x)
                total =+ product_table[i][4]
                if i%2 == 0:
                    self.product_lc.SetItemBackgroundColour(i, wx.LIGHT_GREY)
        
        except IndexError, e: # This occurs when the search bar is empty
            self.ProductRecUpdate()
    
    #----------------------------------------------------------------------
    def EditSaleRec(self, evt):
        event_id = evt.GetId()
        if event_id == ID_EDIT_RECEIPT:
            evt.Skip()
    
    #----------------------------------------------------------------------
    def TSep(self, amount):
        'Adds in thousands separator, if toggled'
        if self.thous_sep:
            amount = amount.split(' ')
            pFix = amount[0]
            amount = amount[-1]
            if '.' in amount: 
                amount = amount.split('.')
                sfx = '.'+amount[-1]
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
    def Total(self):
        '''Finds the after-tax total and subtracts the base revenue to
        show an accurate subtotal, sales tax and total for the period.'''
        # Find the total amount sold during the period
        i_count = self.sales_lc.GetItemCount()
        total = 0
        for i in range(i_count):
            x = ((self.sales_lc.GetItem(i, 2)).GetText()).split(' ')
            total += float(x[-1])
            
        # Find the subtotal from the products sold during the period
        i_count = self.product_lc.GetItemCount()
        subtotal = 0
        for i in range(i_count):
            x = ((self.product_lc.GetItem(i, 4)).GetText()).split(' ')
            subtotal += float(x[-1])
        tax = total - subtotal
        
        # Enter the values into the sales summary info box
        x = self.TSep(('%s %.'+self.c_dec+'f') % (self.c_symbol, subtotal))
        self.subtotal_amount.SetValue(x)
        x = self.TSep(('%s %.'+self.c_dec+'f') % (self.c_symbol, tax))
        self.sTax_amount.SetValue(x)
        x = self.TSep(('%s %.'+self.c_dec+'f') % (self.c_symbol, total))
        self.total_amount.SetValue(x)
                
    #----------------------------------------------------------------------
    def ConfigUpdate(self):
        self.c_symbol = self.config.cCurrency()[0]
        self.c_dec = self.config.cCurrency()[1]
        self.thous_sep = self.config.ThousandsSep()
        
        # Update Period Sales Records List Control
        rCount = self.sales_lc.GetItemCount()
        for i in range(rCount):
            amount = ((self.sales_lc.GetItem(i, 2)).GetText()).split(' ')
            amount = float(amount[-1])
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, amount)
            self.sales_lc.SetStringItem(i, 2, rslt)
            
        rCount = self.receipt_lc.GetItemCount()
        for i in range(rCount):
            price = ((self.receipt_lc.GetItem(i, 1)).GetText()).split(' ')
            price = float(price[-1])
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, price)
            self.receipt_lc.SetStringItem(i, 1, rslt)
            
            amount = ((self.receipt_lc.GetItem(i, 3)).GetText()).split(' ')
            amount = float(amount[-1])
            rslt = ('%s %.'+self.c_dec+'f') % (self.c_symbol, amount)
            self.receipt_lc.SetStringItem(i, 3, rslt)
        self.OnSearch(None)
        self.Total()
        self.Language()
        self.Language2()
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the language.'
        objects = [self.sales_label, self.sales_box, self.sale_items_box,
                   self.edit_receipt_btn, self.sales_period_label,
                   self.st_date_btn, self.end_date_btn, self.summary_sbox,
                   self.subtotal_label, self.sTax_label, self.total_label,
                   self.product_sbox, self.search_label]
        ids = 2, 48, 49, 47, 50, 55, 56, 37, 38, 40, 39, 57, 33
        
        words = mpos_utility.lang(ids)
        for object, word in zip(objects, words):
            object.SetLabel(word)
        self.sTax_label.SetLabel(words[9] + ' (%)')
    
    def Language2(self):
        'Sets the language.'
        ids = 51, 52, 53, 54, 58, 62, 59, 60, 61
        words = mpos_utility.lang(ids)
        self.day, self.week, self.month, self.year = words[:4]
        self.d1, self.d2, self.w1, self.m1, self.t1 = words[4:]
        
    #----------------------------------------------------------------------
    def OnPrintProdList(self, evt):
        'Formats and prints the current list in the product list control.'
        stDate = self.st_date.GetValue()
        endDate = self.end_date.GetValue()
        output = '<h1>miniPOS - Product Sales Report</h1>'
        
        output += '<p>' + (76 * '-') + '</p>'
        output += '<p><pre>Start Date > ' + stDate + 28 * ' '
        output += 'End Date   > ' + endDate + '</pre></p>'
        
        output += '<p>' + (76 * '-') + '</p>'
        output += '<p><b>Period Sales Summary -</b></p>'
        output += '<p><pre> Sub-Total     > ' + self.subtotal_amount.GetValue() + '</pre></p>'
        output += '<p><pre> Sales Tax     > ' + self.sTax_amount.GetValue() + '</pre></p>'
        output += '<p>' + (76 * '-') + '</p>'
        output += '<p><pre><b> Total Sales   > ' + self.total_amount.GetValue() + '</b></pre></p>'
        output += '<p>' + (76 * '-') + '</p></br>'
        labels = '|ID', '|ITEM NAME', '|PRICE', '|QTY', '|AMOUNT'
        output += '<p>' + self.FormatProdItem(labels) + '</p>'
        output += '<p>' + 76 * '=' + '</p>'
        
        # Get the current product list 
        row_count = self.product_lc.GetItemCount()
        product_table = []
        for i in range(row_count):
            item = []
            item.append('|'+self.product_lc.GetItem(i, 0).GetText())
            item.append('|'+self.product_lc.GetItem(i, 1).GetText())
            item.append('|'+self.product_lc.GetItem(i, 2).GetText())
            item.append('|'+self.product_lc.GetItem(i, 3).GetText())
            item.append('|'+self.product_lc.GetItem(i, 4).GetText())
            product_table.append(item)
        
        for item in product_table:
            output += '<p>' + self.FormatProdItem(item) + '</p>'
        output += '<p>' + 76 * '=' + '</p>'
        
        self.printer = mpos_print.Printer()
        self.printer.PreviewText(output, '')

        
    #----------------------------------------------------------------------
    def FormatProdItem(self, prod_item):
        "Takes a tuple from the product list control and formats for printing."
        col_widths = 6, 36, 12, 10, 12
        output = ''
        for i in range(5):
            if len(prod_item[i]) < col_widths[i]:
                output += prod_item[i] + (col_widths[i]-len(prod_item[i]))*'.'
            else:
                output += prod_item[i][:col_widths[i]] 
        return output
    
    #----------------------------------------------------------------------
    def OnPrintReceipt(self, evt):
        "Prints a receipt."
        # Get Receipt Number
        x = self.sales_lc.GetFocusedItem()
        if x == -1: 
            wx.Bell()
            return False
        sale_num = self.sales_lc.GetItem(x, 0).GetText()
        sale_date = self.sales_lc.GetItem(x, 1).GetText()
        output = '<h1> miniPOS - Receipt # '+sale_num+'</h1>'
        output += '<p>' + sale_date + '</p>'
        output += '<p>'+(75 * '-')+'</p>'
        
        # Get Receipt Items and add to output
        row_count = self.receipt_lc.GetItemCount()
        receipt_list = []
        for i in range(row_count):
            item = []
            item.append('|'+self.receipt_lc.GetItem(i, 0).GetText())
            item.append('|'+self.receipt_lc.GetItem(i, 1).GetText())
            item.append('|'+self.receipt_lc.GetItem(i, 2).GetText())
            item.append('|'+self.receipt_lc.GetItem(i, 3).GetText())
            receipt_list.append(item)
         
        # Add Labels
        labels = '|Item Name', '|Price', '|QUANTITY', '|AMOUNT'
        output += '<p>'+self.FormatReceiptItem(labels)+'</p>'
        output += '<p>'+(75 * '=')+'</p>'
        
        # Add Items
        for item in receipt_list:
            output += '<p>'+self.FormatReceiptItem(item)+'</p>'
        
        output += '<p>'+(75 * '=')+'</p>'
        
        # Calculate subtotal, tax and total
        sub_total = self.CalculateSubTotal(receipt_list)
        total = float(self.sales_lc.GetItem(x, 2).GetText().split(' ')[-1])
        tax = total - sub_total
        # Format subtotal, tax and total
        sub_total = self.FormatCurrency(sub_total)
        tax = self.FormatCurrency(tax)
        total = self.FormatCurrency(total)
        # Put the subtotal, tax and total on the receipt
        output += '<p><pre><b>'+(35*' ')+'Sub-Total >     '+sub_total+'</b></pre></p>'
        output += '<p><pre><b>'+(35*' ')+'Sales Tax >     '+tax+'</b></pre></p>'
        output += '<p><pre><b>'+(35*' ')+(40*'-')+'</b></pre></p>'
        output += '<p><pre><b>'+(35*' ')+'Total     >     '+total+'</b></pre></p>'
        
        self.printer = mpos_print.Printer()
        self.printer.PreviewText(output, '')
        
    #----------------------------------------------------------------------
    def FormatReceiptItem(self, receipt_item):
        "Takes a tuple from the receipt list control and formats for printing."
        col_widths = 35, 15, 10, 15
        output = ''
        for i in range(4):
            if len(receipt_item[i]) < col_widths[i]:
                output += receipt_item[i] + (col_widths[i]-len(receipt_item[i]))*'.'
            else:
                output += receipt_item[i][:col_widths[i]]
        return output
    
    #---------------------------------------------------------------------
    def CalculateSubTotal(self, receipt_list):
        "Takes the amounts from a receipt and returns the subtotal."
        amounts = []
        for i in range(len(receipt_list)):
            amounts.append(float(receipt_list[i][-1].split(' ')[-1]))
        rslt = 0
        for amt in amounts:
            rslt += amt
        return rslt
    
    #----------------------------------------------------------------------
    def FormatCurrency(self, float_num):
        "Take a float and turn it into a unicode with the correct currency."
        return unicode(self.c_symbol, 'utf8')+" %.2f" % float_num
            