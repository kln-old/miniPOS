#!/usr/bin/python

# encoding: -*- utf-8 -*-

# pnl_lang.py

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
import os, sys
import csv
import lang_utility

class LangDlg(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(LangDlg, self).__init__(parent, *args, **kwargs)
        
        font1 = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.SetBackgroundColour(wx.WHITE)
        
        # Box Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Language
        #------------------------------------------------------------------
        self.w1, self.w2, self.w3, self.w4, self.w5 = '', '', '', '', '' 
        
        # Title -----------------------------------------------------------
        self.title = wx.StaticText(self, -1, self.w1)
        self.title.SetFont(font1)
        sizer.Add(self.title, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        # Controls --------------------------------------------------------
        self.page_num = wx.StaticText(self, -1, self.w2)
        self.page_num.SetFont(font2)
        self.back_btn = wx.Button(self, wx.ID_BACKWARD, self.w3)
        self.next_btn = wx.Button(self, wx.ID_FORWARD, self.w4)
        self.save_btn = wx.Button(self, wx.ID_SAVE, self.w5)
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.page_num, 1, wx.LEFT|wx.TOP, 5)
        hbox1.Add(self.cancel_btn, 1, wx.RIGHT, 10)
        hbox1.Add(self.back_btn, 1, wx.RIGHT, 10)
        hbox1.Add(self.next_btn, 1, wx.RIGHT, 10)
        hbox1.Add(self.save_btn, 1)
        sizer.Add(hbox1, 0, wx.EXPAND|wx.ALL, 10)
        
        # Input Titles ----------------------------------------------------
        self.from_lang = wx.TextCtrl(self, -1, 
                                     style=wx.TE_READONLY|wx.TE_CENTER)
        self.from_lang.SetFont(font3)
        self.from_lang.SetForegroundColour(wx.WHITE)
        self.from_lang.SetBackgroundColour(wx.BLACK)
        self.to_lang = wx.TextCtrl(self, -1, 
                                  style=wx.TE_READONLY|wx.TE_CENTER)
        self.to_lang.SetFont(font3)
        self.to_lang.SetForegroundColour(wx.WHITE)
        self.to_lang.SetBackgroundColour(wx.BLACK)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.from_lang, 1, wx.RIGHT, 10)
        hbox2.Add(self.to_lang, 1)
        sizer.Add(hbox2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        # Input Fields ----------------------------------------------------
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.f1 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t1 = wx.TextCtrl(self, -1)
        hbox3.Add(self.f1, 1, wx.RIGHT, 10)
        hbox3.Add(self.t1, 1)
        sizer.Add(hbox3, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.f2 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t2 = wx.TextCtrl(self, -1)
        hbox4.Add(self.f2, 1, wx.RIGHT, 10)
        hbox4.Add(self.t2, 1)
        sizer.Add(hbox4, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.f3 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t3 = wx.TextCtrl(self, -1)
        hbox5.Add(self.f3, 1, wx.RIGHT, 10)
        hbox5.Add(self.t3, 1)
        sizer.Add(hbox5, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.f4 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t4 = wx.TextCtrl(self, -1)
        hbox6.Add(self.f4, 1, wx.RIGHT, 10)
        hbox6.Add(self.t4, 1)
        sizer.Add(hbox6, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.f5 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t5 = wx.TextCtrl(self, -1)
        hbox7.Add(self.f5, 1, wx.RIGHT, 10)
        hbox7.Add(self.t5, 1)
        sizer.Add(hbox7, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        self.f6 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t6 = wx.TextCtrl(self, -1)
        hbox8.Add(self.f6, 1, wx.RIGHT, 10)
        hbox8.Add(self.t6, 1)
        sizer.Add(hbox8, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox9 = wx.BoxSizer(wx.HORIZONTAL)
        self.f7 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t7 = wx.TextCtrl(self, -1)
        hbox9.Add(self.f7, 1, wx.RIGHT, 10)
        hbox9.Add(self.t7, 1)
        sizer.Add(hbox9, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        self.f8 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t8 = wx.TextCtrl(self, -1)
        hbox10.Add(self.f8, 1, wx.RIGHT, 10)
        hbox10.Add(self.t8, 1)
        sizer.Add(hbox10, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        self.f9 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t9 = wx.TextCtrl(self, -1)
        hbox11.Add(self.f9, 1, wx.RIGHT, 10)
        hbox11.Add(self.t9, 1)
        sizer.Add(hbox11, 0, wx.EXPAND|wx.ALL, 5)
        
        hbox12 = wx.BoxSizer(wx.HORIZONTAL)
        self.f10 = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.t10 = wx.TextCtrl(self, -1)
        hbox12.Add(self.f10, 1, wx.RIGHT, 10)
        hbox12.Add(self.t10, 1)
        sizer.Add(hbox12, 0, wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------------------------
        self.SetSizer(sizer)
        self.edit_mode = False
        self.Language()
        
        # Bindings
        #------------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnButton)

        
    #----------------------------------------------------------------------
    # FUNCTIONS
    #----------------------------------------------------------------------
    def OnButton(self, evt):
        evt.Skip()
        
    #----------------------------------------------------------------------
    def Init(self, fromLang, toLang, pNum = 1, edit = False):
        'Sets up the panel'
        # Set Title (Add or Edit)
        if edit:
            self.edit_mode = True
        self.Language()
        self.title.SetLabel(self.w1)
        # Set Page Number
        text = self.w2 +' '+ str(pNum)
        self.page_num.SetLabel(text)
        # Toggle Back / Next buttons if necessary
        if pNum == 1: self.back_btn.Disable()
        if pNum == 9: self.next_btn.Disable()
        # Add in the From and To language labels
        self.from_lang.SetValue(fromLang.split('.')[0])
        self.to_lang.SetValue(toLang.split('.')[0])
        # Get Edit/From language:
        self.GetInputFields(fromLang, pNum)
    
    #----------------------------------------------------------------------
    def PathSet(self, lang_file):
        'Creates the correct path to the desired lang_file'
        if hasattr(sys, 'frozen'):
            path = os.path.join('resources', lang_file)
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources', lang_file)
        return path
    
    #----------------------------------------------------------------------
    def GetInput(self, lang_file):
        'Opens the input language file and puts it into a list.'
        path = self.PathSet(lang_file)
        self.infile = open(path, 'rb')
        reader = csv.reader(self.infile, dialect='excel')
        input_list = []
        for term in reader:
            id_num, phrase = term[0], unicode(term[1].decode('utf8'))
            input_list.append((id_num, phrase,))
            
        self.infile.close()
        return input_list

    #----------------------------------------------------------------------
    def GetInputFields(self, lang_file, page_num):
        '''Takes the input list and selects the correct slice for the 
        current page.'''
        lang_list = self.GetInput(lang_file)
        dic = {1: (2, 12), 2: (12, 22), 3: (22, 32), 4: (32, 42),
               5: (42, 52), 6: (52, 62), 7: (62, 72), 8: (72, 82),
               9: (82, 85)}
        slice = lang_list[dic[page_num][0]:dic[page_num][1]]
        
        field_list = [self.f1, self.f2, self.f3, self.f4, self.f5,
                      self.f6, self.f7, self.f8, self.f9, self.f10]
        # Initialize the first 8 pages
        if page_num < 9:
            for i in range(10):
                field_list[i].SetValue(slice[i][0] + ' - ' + slice[i][1])
        # Initialize the last page
        else:
            for i in range(3):
                field_list[i].SetValue(slice[i][0] + ' - ' + slice[i][1])
            for i in range(3, 10):
                field_list[i].Disable()
            
            t_list = [self.t4, self.t5,self.t6, self.t7, 
                      self.t8, self.t9, self.t10]
            for i in range(len(t_list)):
                t_list[i].Disable()
            
    #----------------------------------------------------------------------
    def GetOutputFields(self):
        'Returns all of the input fields, using the from fields if needed.'
        f_list = [self.f1, self.f2, self.f3, self.f4, self.f5,
                  self.f6, self.f7, self.f8, self.f9, self.f10]
        t_list = [self.t1, self.t2, self.t3, self.t4, self.t5,
                  self.t6, self.t7, self.t8, self.t9, self.t10]
        rslt = []
        for i in range(10):
            if t_list[i].GetValue() != '':
                value = t_list[i].GetValue()
                value = value.encode('utf8')
                rslt.append(value)
            else:
                value = f_list[i].GetValue()
                if '-' in value:
                    value = value[value.index('-')+2:]
                value = value.encode('utf8')
                rslt.append(value)
        return rslt
                    
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the Language.'
        ids = 80, 77, 78, 79, 69, 70
        words = lang_utility.lang(ids)
        self.w2, self.w3, self.w4, self.w5 = words[:4]
        if self.edit_mode:
            self.w1 = words[4]
        else:
            self.w1 = words[5]
        self.back_btn.SetLabel(words[1])
        self.next_btn.SetLabel(words[2])
        self.save_btn.SetLabel(words[3])
        
    