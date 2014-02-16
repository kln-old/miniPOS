#! /usr/bin/python

# encoding: -*- utf-8 -*-

# app_main.py

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

# The main wx.App class for miniPOS

import wx
import lang
import os, sys, stat
from frame_main import *
from menu import *
import mpos_utility

class MainApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, -1, title = 'miniPOS')
        self.SetTopWindow(self.frame)
        self.frame.Maximize()
        self.frame.Centre()
        self.frame.Show()
        
#        if not mpos_utility.CheckPath():
#            mpos_utility.DirFailWarning()
        
        self.Bind(wx.EVT_MENU, self.OnMenu)
        
        return True
    
#--------------------------------------------------------------------------
    def OnMenu(self, evt):
        if evt.GetId() == ID_LANG_CONF:
            self.lang = lang.LangFrame(self.frame, -1, title='Language Options')
            self.SetTopWindow(self.lang)
            self.lang.Centre()
            self.lang.Show()
        else:
            self.SetTopWin()

#--------------------------------------------------------------------------
    def SetTopWin(self):
        self.SetTopWindow(self.frame)
    
 #-------------------------------------------------------------------------
    
if __name__ == '__main__':
    app = MainApp(False)
    app.MainLoop()
    
def run():
    app = MainApp(False)
    app.MainLoop()