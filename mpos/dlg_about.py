#!/usr/bin/python

# encoding: -*- utf-8 -*-

# dlg_about.py

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
import config
import mpos_utility

class AboutDlg(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(AboutDlg, self).__init__(parent, *args, **kwargs)
        
        font1 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        # Box Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        self.title = wx.StaticText(self, -1, 'About'+' miniPOS')
        self.title.SetFont(font1)
        sizer.Add(self.title, 0, wx.LEFT|wx.TOP, 10)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        # Credits
        cred_txt = 'Author: Gregory Wilson, 2011'
        self.cred = wx.StaticText(self, -1, cred_txt)
        self.cred.SetFont(font2)
        sizer.Add(self.cred, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        
        # Contact
        contact = 'gwilson.sq1@gmail.com'
        self.contact = wx.StaticText(self, -1, contact)
        sizer.Add(self.contact, 0, wx.ALIGN_CENTER|wx.BOTTOM, 20)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        # Summary and legal
        text = self.GetAboutTxt()
        self.about_txt = wx.TextCtrl(self, -1, 
                                     style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.about_txt.SetValue(text)
        sizer.Add(self.about_txt, 1, wx.EXPAND|wx.ALL, 10)
        
        # Ok Button
        btn = self.CreateButtonSizer(wx.OK)
        sizer.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        # Set Sizer
        self.SetSizer(sizer)
        
        #------------------------------------------------------------------
        self.LangConfig()
    
    #======================================================================
    # FUNCTION
    #======================================================================
    def GetAboutTxt(self):
        'Gets the text from the about.txt file in the mpos directory.'
        if hasattr(sys, 'frozen'):
            path = os.path.join('resources', 'about.txt')
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources', 'about.txt')
        file = open(path, 'r')
        text = ''
        for line in file:
            text += line

        return text
    
    #----------------------------------------------------------------------
    def LangConfig(self):
        'Sets up the language.'
        id_list = [28]
        word = mpos_utility.lang(id_list)
        self.title.SetLabel(word[0]+' miniPOS')
        


