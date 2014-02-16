#! /usr/bin/python

# encoding: -*- utf-8 -*-

# prefs.py

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

# The preferences configuration menu for Mini POS.

import wx
import config
import string
import os, sys
import mpos_utility

class Prefs(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(Prefs, self).__init__(parent, *args, **kwargs)
        
        # Get a list of available languages
        #------------------------------------------------------------------
        if hasattr(sys, 'frozen'):
            path = 'resources'
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources')
        languages = [f for f in os.listdir(path) if '.csv' in f]
        for i in range(len(languages)):
            languages[i] = (languages[i].split('.'))[0]
        languages = [l for l in languages if l != '' and l != 'config']
        
        # Get the current Configuration Settings
        #------------------------------------------------------------------
        # [1]-Lang, [2]-currSym, [3]-currDec, [4]-ToggleThousSep
        # [5]-Toggle Sales Tax, [6]-SalesTax
        self.config = config.Configuration()
        self.settings = self.config.ConfigSettings()
        self.StartLang = self.settings[1]
        
        # Style Elements
        #------------------------------------------------------------------
        font1 = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.Size= ((450, 450))
        
        #------------------------------------------------------------------
        #                       BOX SIZER
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title = wx.StaticText(self, -1, 'Program Settings')
        self.title.SetFont(font1)
        sizer.Add(self.title, 0, wx.LEFT|wx.TOP, 5)
        
        #--# 
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.lang_label = wx.StaticText(self, -1, 'Language'+': ', size=(180, -1))
        self.lang_label.SetFont(font2)
        self.lang_choice = wx.ComboBox(self, -1, choices=languages, 
                                       style=wx.CB_READONLY)
        hbox1.Add(self.lang_label, 0, wx.RIGHT|wx.TOP, 5)
        hbox1.Add(self.lang_choice, 1)
        sizer.Add(hbox1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sym_label = wx.StaticText(self, -1, 'Currency Symbol'+': ',
                                       size=(180, -1))
        self.sym_label.SetFont(font2)
        self.sym_input = wx.TextCtrl(self, -1, style=wx.TE_CENTER)
        hbox2.Add(self.sym_label, 0, wx.TOP|wx.RIGHT, 5)
        hbox2.Add(self.sym_input, 1)
        sizer.Add(hbox2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        #--#
        sizer.Add((-1, 10))
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.dec_label = wx.StaticText(self, -1, 'Currency Decimals'+': ',
                                       size=(180, -1))
        self.dec_label.SetFont(font2)
        self.dec_input = wx.ComboBox(self, -1, 
                                     choices=('0', '1', '2', '3'),
                                     style = wx.CB_READONLY)
        hbox3.Add(self.dec_label, 0, wx.RIGHT|wx.TOP, 5)
        hbox3.Add(self.dec_input, 1)
        sizer.Add(hbox3, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.tSep_check = wx.CheckBox(self, -1, 'Thousands Separator')
        self.tSep_check.SetFont(font2)
        hbox4.Add(self.tSep_check, 0)
        sizer.Add(hbox4, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.sTax_check = wx.CheckBox(self, -1, 'Sales Tax')
        self.sTax_check.SetFont(font2)
        hbox5.Add(self.sTax_check, 0)
        sizer.Add(hbox5, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        #--#
        sizer.Add((-1, 10))
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.sTax_label = wx.StaticText(self, -1, 'Sales Tax Rate'+ ' (%):',
                                       size=(180, -1))
        self.sTax_label.SetFont(font2)
        self.sTax_input = wx.TextCtrl(self, -1, style = wx.TE_CENTER)
        hbox6.Add(self.sTax_label, 0, wx.RIGHT|wx.TOP, 5)
        hbox6.Add(self.sTax_input, 1)
        sizer.Add(hbox6, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        self.SetSizer(sizer)
        
        #--#
        sizer.Add((-1, 10))
        hbox7 = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(hbox7, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        
        # Functions
        #------------------------------------------------------------------
        self.Init()
        self.Language()
        
        # Bindings
        #------------------------------------------------------------------
        self.sTax_check.Bind(wx.EVT_CHECKBOX, self.OnTSep)
        self.sTax_input.Bind(wx.EVT_KEY_UP, self.OnSTax)
        self.sTax_input.Bind(wx.EVT_KILL_FOCUS, self.CleanTax)
        
    #----------------------------------------------------------------------
    #                           FUNCTIONS
    #----------------------------------------------------------------------
    def Init(self):
        'Initializes input fields with values from config file'
        self.lang_choice.SetValue(self.settings[1])
        self.sym_input.SetValue(self.settings[2])
        self.dec_input.SetValue(self.settings[3])
        if self.settings[4] == '1':
            self.tSep_check.SetValue(True)
        else:
            self.tSep_check.SetValue(False)
        if self.settings[5] == '1':
            self.sTax_check.SetValue(True)
            x = ('%2.2f' ) % (float(self.settings[6]), )
            self.sTax_input.SetValue(x)
        else:
            self.sTax_check.SetValue(False)
            self.sTax_input.SetValue('0.0')
    
    #----------------------------------------------------------------------
    def OnTSep(self, evt):
        'Disables the sales tax input if sales tax is deselected'
        if not self.sTax_check.GetValue():
            self.sTax_input.Disable()
        else:
            self.sTax_input.Enable()
            
    #----------------------------------------------------------------------
    def OnSTax(self, evt):
        'Verifies the sales tax entered by the user.'
        try:
            num = float(self.sTax_input.GetValue())
        except ValueError:
            self.sTax_input.SetValue('0.00')
        try:
            num = self.sTax_input.GetValue()
            if num[-1] not in string.digits+'.':
                wx.Bell()
                self.sTax_input.SetValue(num[:-1])
                self.sTax_input.SetInsertionPointEnd()
        except IndexError:
            pass
        
    #----------------------------------------------------------------------
    def CleanTax(self, evt):
        'Cleans up the sales tax entered by the user'
        tax = self.sTax_input.GetValue()
        x = '%2.2f' % float(tax)
        self.sTax_input.SetValue(x)
    
    #----------------------------------------------------------------------     
    def ReturnVals(self):
        vals = []
        vals.append(self.lang_choice.GetValue().encode('utf8'))
        vals.append(self.sym_input.GetValue().encode('utf8'))
        vals.append(self.dec_input.GetValue())
        
        if self.tSep_check.GetValue():
            vals.append(1)
        else:
            vals.append(0)
        
        if self.sTax_check.GetValue():
            vals.append(1)
        else:
            vals.append(0)
        
        vals.append(self.sTax_input.GetValue())
        
        return vals
    
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the Language'
        objects = [self.title, self.lang_label, self.sym_label, 
                   self.dec_label, self.tSep_check, self.sTax_check,
                   self.sTax_label]
        ids = 26, 63, 64, 65, 66, 40, 67
        words = mpos_utility.lang(ids)
        for object, word in zip(objects, words):
            object.SetLabel(word)
        self.sTax_label.SetLabel(words[-1]+' (%)')
        
    #----------------------------------------------------------------------
    def StartingLang(self):
        'Returns the starting language'
        return self.StartLang
        

        
        