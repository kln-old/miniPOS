#! /usr/bin/python

# encoding: -*- utf-8 -*-

# mainFrame.py

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

# This is the main wx.Frame class for the Mini POS program.

import wx
from lc_mpos import *
from pnl_pos import *
from pnl_sales import *
from pnl_inv import *
import mpos_db
from menu import *
import prefs
import sys, os
import dlg_about
import mpos_utility
import time
import sqlite3

idKeyF1 = wx.NewId()

class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainFrame, self).__init__(parent, *args, **kwargs)
        
        # Set the frame icon
        #------------------------------------------------------------------
        if hasattr(sys, 'frozen'):
            path = os.path.join('resources', 'miniPOS.png')
        else:
            path = os.path.split(__file__)[0]
            path = os.path.join(path, 'resources', 'miniPOS.png')
        icon = wx.Icon(path, type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        
        # Set the basic style for the frame
        #------------------------------------------------------------------
        self.SetBackgroundColour(wx.LIGHT_GREY)
        self.Size = (1000, 700)
        
        #------------------------------------------------------------------
        font_1 = wx.Font(25, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        
        # Menu
        #------------------------------------------------------------------
        self.menu = Menu(-1)
        self.SetMenuBar(self.menu)
        
        accel_tbl = wx.AcceleratorTable(
                                        [(wx.ACCEL_NORMAL, wx.WXK_F1, idKeyF1)]
                                        )
        self.SetAcceleratorTable(accel_tbl)
        
        #------------------------------------------------------------------
        # Create the notebook for the application
        #------------------------------------------------------------------
        self.notebook = wx.Notebook(self)
        
        
        # Create the notebook pages 
        #------------------------------------------------------------------
        self.pos_page = POS_Panel(self.notebook)
        self.sales_page = Sales_Panel(self.notebook)
        self.inventory_page = Inventory_Panel(self.notebook)
        
        self.tab1 = 'Point of Sale'
        self.tab2 = 'Sales Records'
        self.tab3 = 'Inventory'
        self.Language()
        
        self.notebook.AddPage(self.pos_page, self.tab1)
        self.notebook.AddPage(self.sales_page, self.tab2)
        self.notebook.AddPage(self.inventory_page, self.tab3)
        
        
        # Put the notebook in a box sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        
        # Complimentary objects
        #------------------------------------------------------------------
        self.db = mpos_db.MPOS_DB()
        self.config = config.Configuration()
        
        # Put in bindings for panel changes
        #-----------------------------------------------------------------
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnChange)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_MENU, self.OnKeyF1, id=idKeyF1)
         
    #######################################################################
    def OnChange(self, evt):
        self.sales_page.SalesRecUpdate()
        self.sales_page.ProductRecUpdate()
        self.pos_page.PListRefresh()
    
    #----------------------------------------------------------------------    
    def OnButton(self, evt):
        'Handles events that pass between pages'
        event_id = evt.GetId()
        
        if event_id == ID_EDIT_RECEIPT:
            # Used for editing a sales record
            
            # Get the sale id
            row = self.sales_page.sales_lc.GetFocusedItem()
            if row == -1: row = 0
            item = self.sales_page.sales_lc.GetItem(row, 0)
            id = item.GetText()
            
            # Pass the sale id to the database and get the receipt
            receipt_table = self.db.ReceiptRecall(id)
            
            # Set the POS page to edit mode
            self.pos_page.EditModeToggle(id, receipt_table)
            
            self.notebook.SetSelection(0)
    
    #----------------------------------------------------------------------
    # All of the menu related functions        
    #----------------------------------------------------------------------
    def OnMenu(self, evt):
        'Handles Menu Events'
        evtId = evt.GetId()
        if evtId == wx.ID_SETUP:
            restart = self.PrefGo()
            if restart:
                self.restart_program()
                evt.Skip()
            
        elif evtId == wx.ID_EXIT:
            sys.exit()
        
        elif evtId == wx.ID_ADD:
            self.notebook.SetSelection(2)
            self.inventory_page.OnAdd(None)
        
        elif evtId == ID_LANG_CONF:
            evt.Skip()
            
        elif evtId == wx.ID_ABOUT:
            self.dlg_l1 = 'About'
            self.Language()
            dlg = dlg_about.AboutDlg(self, -1, title=self.dlg_l1+' miniPOS',
                                     size=(500, 500))
            rslt = dlg.ShowModal()
            if rslt == wx.ID_OK:
                dlg.Destroy()
        
        elif evtId == ID_DB_RESET:
            self.DB_Reset()
            evt.Skip()
        
        elif evtId == wx.ID_RESET:
            self.restart_program()
            evt.Skip()
            
        elif evtId == wx.ID_SAVE:
            self.SaveDB()
        
        elif evtId == wx.ID_OPEN:
            self.OpenDB()
            
    #----------------------------------------------------------------------
    def PrefGo(self):
        'Launches the preferences dialog'
        self.dlg_l2 = 'Preferences'
        self.Language()
        dlg = prefs.Prefs(self, -1, title='miniPOS - '+self.dlg_l2)
        x = dlg.ShowModal()
        restart = False
        if x != wx.ID_CANCEL:
            vals = dlg.ReturnVals()
            st_lang = dlg.StartingLang()
            self.config.SetConfig(vals)
            if st_lang != vals[0]:
                # self.restart_program()
                restart = True
            self.pos_page.ConfigUpdate()
            self.sales_page.ConfigUpdate()
            self.inventory_page.ConfigUpdate()
            self.Language()
        return restart
    
    #----------------------------------------------------------------------
    def DB_Reset(self):
        'Deletes all records from the mpos_db.db file'
        text = 'Are you sure you want to delete all database records?'
        dlg = wx.MessageDialog(self, text, 'Database Reset', wx.OK|wx.CANCEL)
        rslt = dlg.ShowModal()
        if rslt == wx.ID_OK:
            self.db.ResetDB()
            self.pos_page.PListRefresh()
            self.pos_page.OnCancel(None)
            self.sales_page.sales_lc.DeleteAllItems()
            self.sales_page.product_lc.DeleteAllItems()
            self.sales_page.receipt_lc.DeleteAllItems()
            self.inventory_page.product_lc.DeleteAllItems()
            self.restart_program()
        
    #----------------------------------------------------------------------
    def Language(self):
        'Sets the language'
        ids = (1, 2, 3, 28, 4)
        words = mpos_utility.lang(ids)
        self.tab1 = words[0]
        self.tab2 = words[1]
        self.tab3 = words[2]
        self.dlg_l1 = words[3]
        self.dlg_l2 = words[4]
        
    #----------------------------------------------------------------------
    def restart_program(self):
        'Restarts the program'
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    #----------------------------------------------------------------------
    def SaveDB(self):
        'Saves the database file'
        if sys.platform == 'win32':
            f_name = self.BackupFilename()
            wildcard = "Database files (*.db)|*.db"
        else:
            f_name = self.BackupFilename() + '.db'
            wildcard = '*'
            
        dlg = wx.FileDialog(self, message="Backup Database File...",
                            defaultDir='',
                            defaultFile=f_name,
                            wildcard = wildcard,
                            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            dst_path = dlg.GetPaths()[0]
            src_path = self.ResourcePath('pos_data.db')
            import shutil
            shutil.copyfile(src_path, dst_path)
                
    #----------------------------------------------------------------------
    def ResourcePath(self, filename):
        'Returns the relative path to any file in the resources directory.'
        if hasattr(sys, 'frozen'):
            filepath = os.path.join('resources', filename)
        else:
            filepath = os.path.join(os.path.split(__file__)[0], 'resources', 
                                    filename)
        return filepath
    
    #----------------------------------------------------------------------
    def BackupFilename(self):
        'Returns a valid backup filename for the database'
        date = time.localtime()[:3]
        f_name = "miniPOS_DB_%d-%d-%d" % date
        return f_name
        
    #----------------------------------------------------------------------
    def OpenDB(self):
        'Lets the user choose a backup database file to restore.'
        if sys.platform == 'win32':
            wildcard = 'Database files (*.db)|*.db'
        else:
            wildcard = '*'
        dlg = wx.FileDialog(self, message="Select a Database File",
                            defaultDir=os.curdir, defaultFile='',
                            wildcard=wildcard,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            if sys.platform != 'win32' and path[-3:] != '.db':
                wx.Bell()
                return False
                
            self.DBRestore(path)
            
    #----------------------------------------------------------------------
    def DBRestore(self, filename):
        'Takes a backup DB file and restores it to the programs main folder'
        import shutil
        src_path = filename
        dst_path = self.ResourcePath('pos_data.db')
        shutil.copyfile(src_path, dst_path)
        self.restart_program()
        
    #----------------------------------------------------------------------
    def OnKeyF1(self, evt):
        '''If the POS panel is focused, then call the 
        self.pos_page.OnSearchCancel function.'''
        if self.notebook.GetCurrentPage() == self.pos_page:
            self.pos_page.OnSearchCancel(None)
        elif self.notebook.GetCurrentPage() == self.inventory_page:
            self.inventory_page.OnSearchCancel(None)
        