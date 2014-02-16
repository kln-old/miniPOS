#! /usr/bin/python

# encoding: -*- utf-8 -*-

# lc_mpos.py

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
import mpos_utility

class ProductLC(wx.ListCtrl):
    '''
    The List Control for Product Search dialogs
    '''
    
    def __init__(self, parent, *args, **kwargs):
        super(ProductLC, self).__init__(parent, *args, **kwargs)
        
        self.w1 = 'Product Id'
        self.w2 = 'Product'
        self.w3 = 'Price'
        self.Language()
        
        self.InsertColumn(0, self.w1)
        self.SetColumnWidth(0, 100)
        
        self.InsertColumn(1, self.w2)
        self.SetColumnWidth(1, 250)
        
        self.InsertColumn(2, self.w3)
        self.SetColumnWidth(2, 200)    #Sets width to end of ListCtrl
        
    def Language(self):
        'Sets the Language.'
        ids = 17, 18, 7
        words = mpos_utility.lang(ids)
        self.w1, self.w2, self.w3 = words

###########################################################################

class ReceiptLC(wx.ListCtrl):
    '''
    The List Control for the receipt.
    This class includes editable list cells for the price and QT fields
    '''
    
    def __init__(self, parent, *args, **kwargs):
        super(ReceiptLC, self).__init__(parent, *args, **kwargs)
        
        default = '', '', '', '', ''
        self.w1, self.w2, self.w3, self.w4, self.w5 = default
        self.Language()
        
        self.InsertColumn(0, self.w1)
        self.SetColumnWidth(0, 40)
        
        self.InsertColumn(1, self.w2)
        self.SetColumnWidth(1, 200)
        
        self.InsertColumn(2, self.w3)
        self.SetColumnWidth(2, 80)
        
        self.InsertColumn(3, self.w4)
        self.SetColumnWidth(3, 60)
        
        self.InsertColumn(4, self.w5)
        self.SetColumnWidth(4, 500)
    
    def Language(self):
        'Sets the Language.'
        ids = 19, 18, 7, 20, 21
        words = mpos_utility.lang(ids)
        self.w1, self.w2, self.w3, self.w4, self.w5 = words
        
###########################################################################

class SalesLC(wx.ListCtrl):
    '''
    This List Control goes on the Sales_Panel.
    '''
    def __init__(self, parent, *args, **kwargs):
        super(SalesLC, self).__init__(parent, *args, **kwargs)
        
        default = '', '', ''
        self.w1, self.w2, self.w3 = default
        self.Language()
        
        self.InsertColumn(0, self.w1)
        self.SetColumnWidth(0, 75)
        
        self.InsertColumn(1, self.w2)
        self.SetColumnWidth(1, 300)
        
        self.InsertColumn(2, self.w3)
        self.SetColumnWidth(2, 300)
        
    def Language(self):
        'Sets the Language.'
        ids = 22, 23, 24
        words = mpos_utility.lang(ids)
        self.w1, self.w2, self.w3 = words
###########################################################################

class RecReviewLC(wx.ListCtrl):
    '''
    This List Control displays the sales receipt for sales records
    '''
    
    def __init__(self, parent, *args, **kwargs):
        super(RecReviewLC, self).__init__(parent, *args, **kwargs)
        
        default = '', '', '', ''
        self.w1, self.w2, self.w3, self.w4 = default
        self.Language()
        
        self.InsertColumn(0, self.w1)
        self.SetColumnWidth(0, 250)
        
        self.InsertColumn(1, self.w2)
        self.SetColumnWidth(1, 100)
        
        self.InsertColumn(2, self.w3)
        self.SetColumnWidth(2, 80)
        
        self.InsertColumn(3, self.w4)
        self.SetColumnWidth(3, 150)
    
    def Language(self):
        'Sets the Language.'
        ids = 6, 7, 20, 21
        words = mpos_utility.lang(ids)
        self.w1, self.w2, self.w3, self.w4 = words
