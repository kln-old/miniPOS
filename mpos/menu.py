#! /usr/bin/python

# encoding: -*- utf-8 -*-

# menu.py

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

import wx, mpos_utility

ID_LANG_CONF = wx.NewId()
ID_DB_RESET = wx.NewId()

class Menu(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(Menu, self).__init__(parent, *args, **kwargs)
        
        self.file = wx.Menu()
        self.edit = wx.Menu()
        self.help = wx.Menu()
        
        self.f1, self.f2, self.f3 = '', '', ''
        self.e1, self.e2, self.e3 = '', '', ''
        self.h1 = ''
        self.m1, self.m2, self.m3 = '', '', ''
        self.Language()
        
        self.file.Append(ID_DB_RESET, self.f1, 'Reset Database')
        self.file.Append(wx.ID_SAVE, 'Save Database')
        self.file.Append(wx.ID_OPEN, 'Open Database')
        self.file.AppendSeparator()
        self.file.Append(wx.ID_RESET, self.f3, 'Restart Program')
        self.file.Append(wx.ID_EXIT, self.f2, 'Exit Program')
        
        self.edit.Append(wx.ID_ADD, self.e1, 'Add Item')
        self.edit.AppendSeparator()
        self.edit.Append(wx.ID_SETUP, self.e2, 'Program Settings')
        self.edit.Append(ID_LANG_CONF, self.e3, 'Language Options')
        
        self.help.Append(wx.ID_ABOUT, self.h1, 'About Program')
        
        self.Append(self.file, self.m1)
        self.Append(self.edit, self.m2)
        self.Append(self.help, self.m3)
        
        self.Bind(wx.EVT_MENU, self.OnMenu)
        
    def OnMenu(self, evt):
        evt.Skip()
        
    def Language(self):
        'Sets the Language.'
        ids = (25, 5, 26, 27, 28, 29, 30, 31, 82, 83)
        words = mpos_utility.lang(ids)
        self.f2 = words[0]
        self.e1, self.e2, self.e3 = words[1:4]
        self.h1 = words[4]
        self.m1, self.m2, self.m3 = words[5:-2]
        self.f1 = words[-2]
        self.f3 = words[-1]
        