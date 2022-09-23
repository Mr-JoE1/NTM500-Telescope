#         *   @file  : main.py
#         *   @brief : wx.Frame to control both Mount and Dome of Telescope 
#         *   @author: Mohamed Maher 
#         *   @date  : 22.07.2020
#         *   @Co-author : 
#         *   @Copyrights: www.infinitytech.ltd
import wx
import wx.lib.newevent
import wx.adv
import time
from threading import Thread

import tcs 
import telPanel 
import domPanel 
import stell_server 


########################################################################
class headPanel(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent, size=(700,350))
        fname = domPanel.GetMonoFont()
        image_file = tcs.fileDir + '/sky1.png'
        bmp = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # image's upper left corner anchors at panel coordinates (0, 0)
        self.bitmap1 = wx.StaticBitmap(self, -1, bmp, (0, 0))



class MainFrame(wx.Frame):


    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title,
                                 style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, size=(700, 800))
        self.SetBackgroundColour('BLACK')
        #self.ShowFullScreen(True)
        # Add window icon
        icons = wx.IconBundle()
        #icons.AddIconFromFile(self._get_img_path('logo.ico'), wx.BITMAP_TYPE_ANY)
        icons.AddIcon(wx.Icon(tcs.fileDir + '/logo.ico'))
        tcs.maher.info('=====================================')
        tcs.maher.info('Cigar Telescope Remote Controller')
        tcs.maher.info('Developed By: Mohamed Maher')
        tcs.maher.info('www.infinitytech.ltd')
        tcs.maher.info('=====================================')
        tcs.maher.info('System Started')
        self.SetIcons(icons)

        self.panel1 = domPanel.domePanel(self,None)
        self.panel2 = telPanel.telPanel(self,None)
        self.panel3 = headPanel(self,None)
        self.panel4 = stell_server.stelPanel(self,"") 

        #frame sizer 
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        hsiz1=wx.BoxSizer(wx.HORIZONTAL)
        hsiz1.Add(self.panel3, 1, wx.ALIGN_CENTER)
        self.sizer.Add(hsiz1, wx.ALIGN_CENTER|wx.ALL)
        self.sizer.Add((-1, 1))

        hsiz2=wx.BoxSizer(wx.HORIZONTAL)

        hsiz2.Add(self.panel1, 1, wx.ALIGN_CENTER|wx.ALL)
        hsiz2.Add(self.panel2, 1, wx.ALIGN_CENTER|wx.ALL)

        self.sizer.Add(hsiz2, wx.ALIGN_CENTER|wx.ALL)
        self.sizer.Add((-1, 1))

        hsiz3=wx.BoxSizer(wx.HORIZONTAL)
        hsiz3.Add(self.panel4, 1, wx.ALIGN_CENTER|wx.ALL)

        self.sizer.Add(hsiz3, wx.ALIGN_CENTER|wx.ALL)
        self.sizer.Add((-1, 1))

        self.SetSizer(self.sizer)
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, 'Cigar: Telescope Remote Controller')
    frame.Show()
    app.MainLoop()