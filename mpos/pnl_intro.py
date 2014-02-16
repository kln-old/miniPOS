#!/usr/bin/python

# encoding: -*- utf-8 -*-

# pnl_intro

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
import lang_utility

ID_INTRO_ADD = wx.NewId()
ID_INTRO_EDIT = wx.NewId()
ID_INTRO_CANCEL = wx.NewId()  

class IntroPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(IntroPanel, self).__init__(parent, *args, **kwargs)
        
        # Panel Style Elements
        #------------------------------------------------------------------
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(wx.WHITE)
        #------------------------------------------------------------------
        # Box Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Label and Static Line
        #------------------------------------------------------------------
        self.pLabel = wx.StaticText(self, -1, 'Language Options')
        self.pLabel.SetFont(font2)
        sizer.Add(self.pLabel, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        # Edit Language Static Text and ComboBox
        #------------------------------------------------------------------
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.editLabel = wx.StaticText(self, -1, 'Edit Language'+': ')
        self.editLabel.SetFont(font1)
        self.editChoice = wx.ComboBox(self, -1, style=wx.CB_READONLY)
        self.edit_btn = wx.Button(self, id=ID_INTRO_EDIT, label='Edit')
        hbox1.Add(self.editLabel, 1, wx.TOP|wx.RIGHT, 5)
        hbox1.Add(self.editChoice, 1, wx.RIGHT, 20)
        hbox1.Add(self.edit_btn, 0)
        sizer.Add(hbox1, 0, wx.EXPAND|wx.ALL, 20)
        
        # Add Language Label and Static Line
        #------------------------------------------------------------------
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        self.addLabel = wx.StaticText(self, -1, 'Add New Language')
        self.addLabel.SetFont(font3)
        sizer.Add(self.addLabel, 0, wx.TOP|wx.LEFT|wx.RIGHT, 5)
        
        # Add Language Static Text and TextControl entry
        #------------------------------------------------------------------
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.nameLabel = wx.StaticText(self, -1, 'New Language Name'+': ')
        self.nameLabel.SetFont(font1)
        self.nameInput = wx.TextCtrl(self, -1)
        hbox2.Add(self.nameLabel, 1, wx.TOP|wx.RIGHT, 5)
        hbox2.Add(self.nameInput, 1)
        sizer.Add(hbox2, 0, wx.EXPAND|wx.ALL, 20)
        
        # From Language Label and Combo Box
        #------------------------------------------------------------------
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.fromLabel = wx.StaticText(self, -1, 'From'+': ')
        self.fromLabel.SetFont(font1)
        self.fromChoice = wx.ComboBox(self, -1)
        self.add_btn = wx.Button(self, ID_INTRO_ADD, label='Add')
        hbox3.Add(self.fromLabel, 1, wx.TOP|wx.RIGHT, 5)
        hbox3.Add(self.fromChoice, 2, wx.RIGHT, 20)
        hbox3.Add(self.add_btn, 0)
        sizer.Add(hbox3, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        # Cancel Button
        #------------------------------------------------------------------
        self.cancel_btn = wx.Button(self, ID_INTRO_CANCEL, label='Cancel')
        sizer.Add(self.cancel_btn, 0, wx.ALL, 20)
        
        self.SetSizer(sizer)
        
        # Bindings
        #------------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        
        # Function Calls
        #------------------------------------------------------------------
        self.Init()
        
    #----------------------------------------------------------------------
    # FUNCTIONS
    #----------------------------------------------------------------------
    def Init(self):
        'Initializes the Language Options menu.'
        self.SetLangs()
        self.Language()
    
    #----------------------------------------------------------------------
    def SetLangs(self):
        'Sets the existing languages to the two combo boxes'
        langs = self.LangFiles()
        for lang in langs:
            self.editChoice.Append(lang)
            self.fromChoice.Append(lang)
            
    #----------------------------------------------------------------------
    def OnButton(self, evt):
        if evt.GetId() == ID_INTRO_ADD:
            if self.NewLangCheck():
                evt.Skip()
        else:
            evt.Skip()
        
    #----------------------------------------------------------------------
    def LangPath(self):
        'Get the correct path to the lang directory.'
        if hasattr(sys, 'frozen'):
            path = 'resources'
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources')
        return path
    
    #----------------------------------------------------------------------
    def LangFiles(self):
        'Get the existing language csv files'
        path = self.LangPath()
        langs = [f for f in os.listdir(path) if '.csv' in f]
        for i in range(len(langs)):
            langs[i] = langs[i].split('.')[0]
        langs = [l for l in langs if len(l) != 0 and l != 'config']
        return langs
    
    #----------------------------------------------------------------------
    def NewLangCheck(self):
        'Checks to see if the new language does not already exist.'
        langs = self.LangFiles()
        for i in range(len(langs)):
            langs[i] = langs[i].lower()
        newLang = self.nameInput.GetValue().lower()
        if newLang in langs:
            self.m1, self.t1 = '', ''
            self.Language()
            wx.MessageBox(self.m1, self.t1)
            return False
        elif newLang == '':
            self.m2, self.t2 = 'Enter a name for the new language.', 'Fail'
            self.Language()
            wx.Bell()
            wx.MessageBox(self.m2, self.t2)
            return False
        else:
            return True
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the language.'
        objects = [self.pLabel, self.editLabel, self.edit_btn, 
                   self.addLabel, self.nameLabel, self.fromLabel,
                   self.add_btn]
        id = 27, 69, 30, 70, 72, 73, 70
        words = lang_utility.lang(id)
        for object, word in zip(objects, words):
            object.SetLabel(word)
        # Special Cases
        self.add_btn.SetLabel(words[-1])
        self.editLabel.SetLabel(words[1]+':')
        self.nameLabel.SetLabel(words[4]+':')
