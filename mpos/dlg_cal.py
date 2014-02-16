#! /urs/bin/python

# encoding: -*- utf-8 -*-

# dlg_cal.py

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

# This calendar brings up the calendar dialog used when selecting periods
#       in the sales report panel

import wx
import wx.calendar as cal
import mpos_utility
import sys

class Calendar(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(Calendar, self).__init__(parent, *args, **kwargs)
        
        font_1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        self.Size = (275, 300)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #------------------------------------------------------------------
        calend = cal.CalendarCtrl(self, -1, wx.DateTime_Now(),
                                  style=cal.CAL_SEQUENTIAL_MONTH_SELECTION)
        sizer.Add(calend, 0, wx.EXPAND|wx.ALL, 10)
        
        #------------------------------------------------------------------
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.date = wx.StaticText(self, -1, 'Double Click to Select Date')
        self.date.SetFont(font_1)
        hbox1.Add(self.date, 1)
        sizer.Add(hbox1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
        
        #------------------------------------------------------------------
        hbox2 = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(hbox2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        sizer.Add((-1, 10))
        
        #------------------------------------------------------------------
        self.SetSizer(sizer)
        
        # Dialog Bindings
        #------------------------------------------------------------------
        self.Bind(cal.EVT_CALENDAR, self.OnDateSelected)
        
        #------------------------------------------------------------------
        self.Language()
        
    #----------------------------------------------------------------------
    #                             Dialog Functions                        
    #----------------------------------------------------------------------
    def OnDateSelected(self, evt):
        'This gets the date and puts it into the same format as the database'
        month_dic = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 
                     'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8',
                     'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        
        if sys.platform == 'win32':
            date = str(evt.GetDate()).split(' ')[0]
            date = date.split('/')
            date[2] = '20' + date[2]
            day, month = date[0], date[1]
            date[0], date[1] = month, day
            date = '/'.join(date)
            self.date.SetLabel(date)
        else:
            date = str(evt.GetDate()).split(' ')
            day = date[1]
            month = month_dic[date[2]]
            year = date[3]
            date = ('%s/%s/%s') % (day, month, year)
            self.date.SetLabel(date)
     
    #----------------------------------------------------------------------    
    def SendDate(self):
        'Returns the selected date to the calling panel'
        date = self.date.GetLabel()
        if sys.platform == "win32":
            if len(date) == 10:
                return date
            else:
                self.m1 = '-'
                self.t1 = '-'
                self.Language()
                wx.MessageBox(self.m1, self.t1)
                
                return False
        else:
            if len(date) == 9 or len(date) == 10:
                return date
            else:
                self.m1 = '-'
                self.t1 = '-'
                self.Language()
                wx.MessageBox(self.m1, self.t1)
                
                return False
    
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the correct language.'
        id_list = (10, 11, 12)
        words = mpos_utility.lang(id_list)
        
        self.date.SetLabel(words[0])
        self.m1 = words[1]
        self.t1 = words[2]
        
        
        