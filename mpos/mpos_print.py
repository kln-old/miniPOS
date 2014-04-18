#!/usr/bin/python

# coding: -*- utf8 -*-

# mpos_print.py

# Contains the print functions for miniPOS
# Developmental

import wx.html
from wx.html import HtmlEasyPrinting
import sys
import cups
from xhtml2pdf import pisa

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
        
class PrinterCups():
	def __init__(self):
		#pisa.__init_(self)
		print "initializing pisa in printer..."

	def PrintText(self, text, title):
		#tmp file for printing
		filename = "/tmp/print.pdf"

		pdf = pisa.CreatePDF(text, file(filename, "w"))
                if not pdf.err:
                        # close pdf file else we can't read later
                        pdf.dest.close()

                        # print the file using cups
                        conn = cups.Connection()
                        # get a list of all printers
                        printers = conn.getPrinters()
                        for printer in printers:
                                # print name of printers to stdout
                                print printer, printers[printer]["device-uri"]
                        
                        #get first printer from the printer list
                        printer_name = printers.keys()[0]
                        conn.printFile(printer_name, filename, "python_status_print",{})
                else:
                        print "unable to create pdf file"
