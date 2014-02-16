#!/usr/bin/python

# coding: -*- utf8 -*-

# mpos_print.py

# Contains the print functions for miniPOS
# Developmental

import wx.html
from wx.html import HtmlEasyPrinting
import sys

class Printer(HtmlEasyPrinting):
    def __init__(self):
        HtmlEasyPrinting.__init__(self)
        
    def PreviewText(self, text, title):
        self.SetHeader(title, pg=wx.html.PAGE_ALL)
        if sys.platform == 'win32':
            self.SetFonts('Courier New','monospace', [8, 9, 9, 10, 12, 14, 16])
        else:
            self.SetFonts('Courier New', 'monospace')
        try:
            HtmlEasyPrinting.PreviewText(self, text)
        except:
            pass
        

