
#         *   @file   telPanel.py
#         *   @brief  wx.Panel class for all functions related to Telescope Mount TCP Control 
#         *   @author Mohamed Maher 
#         *   @date   22.07.2020
#         *   @Co-author 
#         *   @Copyrights: www.infinitytech.ltd


import wx
import sys
import os
import wx.lib.newevent
import wx.adv
import time
from threading import Thread
import socket
import binascii
import stell_server 
import struct
import tcs

def GetMonoFont():

    if os.name == 'nt':
        fname = 'Consolas'
        return fname

    # unknown OS
    else:
        fname = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        return fname


class telPanel(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent,size=(300,250))

        fname = GetMonoFont()

       
        #telThread= Thread(target=self.mounTcpMon, args=())
        #telThread.start()

        vbox = wx.BoxSizer(wx.VERTICAL)
	    
        ## network connection 
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        txt1 = wx.StaticText(self, label="Connection:", style=wx.TE_CENTRE)
        txt1.SetForegroundColour('white')
        txt1.SetFont(wx.Font(16,75, 90, 90, faceName=fname))
        hbox1.Add(txt1, flag=wx.LEFT, border=8)

        self.data1 = wx.TextCtrl(
                self, wx.ID_ANY, "Offline", size=(140, 30), style=wx.TE_CENTRE)
        self.data1.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        self.data1.SetForegroundColour('yellow')
        self.data1.SetBackgroundColour('black')
        hbox1.Add(self.data1, flag=wx.LEFT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.TOP, border=5)

        vbox.Add((-1, 10))

        # postion station 
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        txt2 = wx.StaticText(self, label="Pos_RA    :")
        txt2.SetForegroundColour('white')
        txt2.SetFont(wx.Font(16,75, 90, 90, faceName=fname))
        hbox2.Add(txt2, flag=wx.LEFT, border=8)

        self.data2 = wx.TextCtrl(
                self, wx.ID_ANY, "--", size=(140, 30), style=wx.TE_CENTRE)
        self.data2.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        self.data2.SetForegroundColour('yellow')
        self.data2.SetBackgroundColour('black')
        hbox2.Add(self.data2, flag=wx.LEFT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.TOP, border=5)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        txt3 = wx.StaticText(self, label='Pos_DEC   :')
        txt3.SetForegroundColour('white')
        txt3.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        hbox3.Add(txt3, flag=wx.LEFT, border=8)

        self.data3 = wx.TextCtrl(
                self, wx.ID_ANY, "--", size=(140, 30), style=wx.TE_CENTRE)
        self.data3.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        self.data3.SetForegroundColour('yellow')
        self.data3.SetBackgroundColour('black')
        hbox3.Add(self.data3, flag=wx.LEFT, border=8)

        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.TOP, border=5)

        vbox.Add((-1, 10))

        ######################################
        # Touch Control Buttons
        ######################################
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(self, label='RA++', size=(70,50))
        btn1.SetForegroundColour('black')
        btn1.SetBackgroundColour('#0873FF')
        btn1.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        hbox5.Add(btn1, flag=wx.LEFT, border=8)

        btn2 = wx.ToggleButton(self, label='DEC+', size=(70,50))
        btn2.SetForegroundColour('black')
        btn2.SetBackgroundColour('#0873FF')
        btn2.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        hbox5.Add(btn2,flag=wx.LEFT, border=8)

        self.btn5 = wx.Button(self, label='Brake', size=((80,50)))
        self.btn5.SetForegroundColour('black')
        self.btn5.SetBackgroundColour('red')
        self.btn5.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        hbox5.Add(self.btn5, flag=wx.LEFT, border=8)


        vbox.Add(hbox5, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        vbox.Add((-1, 5))
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn4 = wx.Button(self, label='RA--', size=((70,50)))
        self.btn4.SetForegroundColour('black')
        self.btn4.SetBackgroundColour('#0873FF')
        self.btn4.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        hbox6.Add(self.btn4, flag=wx.LEFT, border=8)
        btn3 = wx.Button(self, label='DEC-', size=(70,50))
        btn3.SetForegroundColour('black')
        btn3.SetBackgroundColour('#0873FF')
        btn3.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        hbox6.Add(btn3, flag=wx.LEFT, border=8)

        self.telMode = wx.Choice(self, -1,choices=['Auto','Manual'], size=(80,45))
        self.telMode.SetStringSelection('Auto')

        hbox6.Add(self.telMode,flag=wx.LEFT, border=8)
        vbox.Add(hbox6, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.SetSizer(vbox)



    def mounTcpMon(self):
        mount_data=''
        mountSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mhost = '192.168.1.4'
        mport = 10050
        #ThreadCount = 0
        try:
           mountSocket.bind((mhost, mport))
           tcs.maher.info('Mount monitor server created - Port(%s)', str(mport))
        except socket.error as e:
            tcs.maher.error('Mount monitor server Failed :%s', str(e))
        try:
            mountSocket.listen(5)
            mountClient, mountaddress = mountSocket.accept()
            self.data1.Clear()
            self.data1.AppendText('Online')
        except socket.error as e:
            tcs.maher.error('Mount Controller does not reply :%s', str(e))
            # self.data1.Clear()
            # self.data1.AppendText('Offline')
            # self.data3.Clear()
            # self.data3.AppendText('X')
            # self.data2.Clear()
            # self.data2.AppendText('X')
            mountSocket.close()
        while True:
            try:
                mount_data= mountClient.recv(4)
                mount_dd= ':'.join('{:02x}'.format(x) for x in mount_data)

            except socket.error:
                # self.data1.Clear()
                # self.data1.AppendText('Offline')
                # self.data3.Clear()
                # self.data3.AppendText('X')
                # self.data2.Clear()
                # self.data2.AppendText('X')
                tcs.maher.error('Mount monitor Connection ERORR: :%s', str(socket.error))
