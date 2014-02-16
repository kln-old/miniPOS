#!/usr/bin/python

# encoding: -*- utf-8 -*-

# lang.py

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

# Manages the language editing and adding functions for the program

import wx
import csv
import os, sys
from pnl_intro import *
import pnl_lang

ID_P1 = wx.NewId()
ID_P2 = wx.NewId()
ID_P3 = wx.NewId()
ID_P4 = wx.NewId()
ID_P5 = wx.NewId()
ID_P6 = wx.NewId()
ID_P7 = wx.NewId()
ID_P8 = wx.NewId()
ID_P9 = wx.NewId()

###########################################################################        
#--------------------------------------------------------------------------
class LangFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(LangFrame, self).__init__(parent, *args, **kwargs)
        
        # Set the frame icon
        #------------------------------------------------------------------
        if hasattr(sys, 'frozen'):
            path = os.path.join('resources', 'miniPOS.png')
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources', 'miniPOS.png')
        icon = wx.Icon(path, type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        
        # Set Size and Add Panels
        #------------------------------------------------------------------
        self.Size = ((500, 340))
        self.introPanel = IntroPanel(self, -1)
        self.lang_1 = pnl_lang.LangDlg(self, ID_P1)
        self.lang_2 = pnl_lang.LangDlg(self, ID_P2)
        self.lang_3 = pnl_lang.LangDlg(self, ID_P3)
        self.lang_4 = pnl_lang.LangDlg(self, ID_P4)
        self.lang_5 = pnl_lang.LangDlg(self, ID_P5)
        self.lang_6 = pnl_lang.LangDlg(self, ID_P6)
        self.lang_7 = pnl_lang.LangDlg(self, ID_P7)
        self.lang_8 = pnl_lang.LangDlg(self, ID_P8)
        self.lang_9 = pnl_lang.LangDlg(self, ID_P9)
        
        # Add Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.introPanel, 1, wx.EXPAND)
        #--#
        sizer.Add(self.lang_1, 1, wx.EXPAND)
        self.lang_1.Hide()
        #--#
        sizer.Add(self.lang_2, 1, wx.EXPAND)
        self.lang_2.Hide()
         #--#
        sizer.Add(self.lang_3, 1, wx.EXPAND)
        self.lang_3.Hide()
         #--#
        sizer.Add(self.lang_4, 1, wx.EXPAND)
        self.lang_4.Hide()
         #--#
        sizer.Add(self.lang_5, 1, wx.EXPAND)
        self.lang_5.Hide()
         #--#
        sizer.Add(self.lang_6, 1, wx.EXPAND)
        self.lang_6.Hide()
         #--#
        sizer.Add(self.lang_7, 1, wx.EXPAND)
        self.lang_7.Hide()
         #--#
        sizer.Add(self.lang_8, 1, wx.EXPAND)
        self.lang_8.Hide()
        #--#
        sizer.Add(self.lang_9, 1, wx.EXPAND)
        self.lang_9.Hide()
        
        self.SetSizer(sizer)
        
        # Utility 
        #------------------------------------------------------------------
        self.lPnls = [self.lang_1, self.lang_2, self.lang_3, self.lang_4,
                 self.lang_5, self.lang_6, self.lang_7, self.lang_8, 
                 self.lang_9]
        
        self.current_langPnl = 99 # 99 denotes the introPanel
        self.edit_mode = False
        
        # Bindings
        #------------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        
    #======================================================================
    #                              FUNCTIONS
    #======================================================================
    def OnButton(self, evt):
        # Buttons pnl_intro.py
        if evt.GetId() == ID_INTRO_ADD:
            self.OnAdd()
        elif evt.GetId() == ID_INTRO_EDIT:
            self.OnEdit()
        elif evt.GetId() == ID_INTRO_CANCEL:
            self.Destroy()
        
        # Buttons from the pnl_lang.py
        elif evt.GetId() == wx.ID_CANCEL:
            self.OnCancel()
        elif evt.GetId() == wx.ID_SAVE:
            self.OnSave()
        elif evt.GetId() == wx.ID_BACKWARD:
            self.OnBack()
        elif evt.GetId() == wx.ID_FORWARD:
            self.OnNext()
    
    #----------------------------------------------------------------------
    # INTRO PANEL FUNCTIONS        
    #----------------------------------------------------------------------    
    def OnAdd(self):
        'Switches to and initializes the lang Panel.'
        if self.introPanel.fromChoice.GetValue() and self.introPanel.toChoice.GetValue():
            self.introPanel.Hide()
            # Ensure edit mode is false
            self.edit_mode = False
            # Get From Language
            self.fromLang = self.introPanel.fromChoice.GetValue() + '.csv'
            # Get to language
            self.toLang = self.introPanel.nameInput.GetValue() + '.csv'
            # Initialize all lang_panels
            p = 1
            for panel in self.lPnls:
                panel.Init(self.fromLang, self.toLang, p, self.edit_mode)
                p += 1
            # Switch to lang_1
            self.Size=((550, 550))
            self.Centre()
            self.lang_1.Show()
            self.Layout()
            # Set self.current_langPnl
            self.current_langPnl = 0
        else:
            wx.Bell()
    #----------------------------------------------------------------------
    def OnEdit(self):
        'Switiches to and initializes the lang panel to edit a language.'
        
        if self.introPanel.editChoice.GetValue():
            self.introPanel.Hide()
            self.edit_mode = True
            self.fromLang = self.introPanel.editChoice.GetValue() + '.csv'
            self.toLang = self.introPanel.editChoice.GetValue() + '.csv'
            p = 1
            for panel in self.lPnls:
                panel.Init(self.fromLang, self.toLang, p, self.edit_mode)
                p += 1
            self.Size=((550, 550))
            self.Centre()
            self.lang_1.Show()
            self.Layout()
            self.current_langPnl = 0
        else:
            wx.Bell()
        
    #----------------------------------------------------------------------
    # LANGUAGE PANEL FUNCTIONS
    #----------------------------------------------------------------------
    def OnCancel(self):
        'Destroys the dialog'
        self.Destroy()
    
    #----------------------------------------------------------------------    
    def OnNext(self):
        'Switches to the next language panel page'
        self.current_langPnl += 1
        pnl = self.lPnls[self.current_langPnl]
        # Switch panels
        self.lPnls[self.current_langPnl-1].Hide()
        self.lPnls[self.current_langPnl].Show()
        self.Layout()
        
    #----------------------------------------------------------------------
    def OnBack(self):
        'Switches to the previous panel page'
        self.current_langPnl -= 1
        pnl = self.lPnls[self.current_langPnl] 
        # Switch panels
        self.lPnls[self.current_langPnl + 1].Hide()
        self.lPnls[self.current_langPnl].Show()
        self.Layout()
    
    #----------------------------------------------------------------------
    def OnSave(self):
        '''Adds all of the terms that have already been translated to a new
        list. For terms that aren't translated, adds the corresponding words 
        from the From Language to the same list. Saves the list to a new csv
        file with the provided language name.'''
        newLang_list = []
        
        new_lang = []
        for panel in self.lPnls:
            new_words = panel.GetOutputFields()
            for word in new_words:
                new_lang.append(word)
        
        file = self.PathMaker(self.toLang)
        file = open(file, 'wb')
        writer = csv.writer(file, dialect='excel')
        writer.writerow(['Language']+[self.toLang.encode('utf8')])
        writer.writerow(['From'] + [self.fromLang.encode('utf8')])
        
        i = 1
        for word in new_lang:
            try:
                writer.writerow([i]+[word])
                i += 1
            except UnicodeEncodeError:
                writer.writerow([i]+['!'])
        
        file.close()

    #----------------------------------------------------------------------
    def PathMaker(self, filename):
        'Writes the correct path to the lang directory for the filename'
        if hasattr(sys, 'frozen'):
            path = os.path.join('resources', filename)
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources', filename)
        return path


###########################################################################
#--------------------------------------------------------------------------
class xApp(wx.App):
    def OnInit(self):
        self.frame = LangFrame(None, -1, title='Language Options')
        self.SetTopWindow(self.frame)
        self.frame.Center()
        self.frame.Show()
        return True
    
    
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# TESTING SCRIPT
#__________________________________________________________________________
if __name__ == '__main__':
    app = xApp(False)
    app.MainLoop()
        
