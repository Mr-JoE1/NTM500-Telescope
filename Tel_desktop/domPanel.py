
#         *   @file   domPanel.py
#         *   @brief  wx.Panel class for all functions related to Dome TCP Control 
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
        fname = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT) #'helvetica'
        return fname



dome_mode='manual'
dome_pos = 0

class domePanel(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id, **kwgs):
        # create the panel
        wx.Panel.__init__(self, parent, size=(350,250))
        fname = GetMonoFont()

        #tcpThread= Thread(target=self.domeTcpMon, args=())
        #tcpThread.start()

        dvbox = wx.BoxSizer(wx.VERTICAL)
        
        ## network connection 
        dhbox1 = wx.BoxSizer(wx.HORIZONTAL)
        dtxt1 = wx.StaticText(self, label="Connection:", style=wx.TE_CENTRE)
        dtxt1.SetForegroundColour('white')
        dtxt1.SetFont(wx.Font(16,75, 90, 90, faceName=fname))
        dhbox1.Add(dtxt1, flag=wx.LEFT, border=8)

        self.ddata1 = wx.TextCtrl(
                self, wx.ID_ANY, "Offline", size=(140, 30), style=wx.TE_CENTRE)
        self.ddata1.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        self.ddata1.SetForegroundColour('yellow')
        self.ddata1.SetBackgroundColour('black')
        dhbox1.Add(self.ddata1, flag=wx.LEFT, border=8)

        dvbox.Add(dhbox1, flag=wx.EXPAND|wx.LEFT|wx.TOP, border=5)

        dvbox.Add((-1, 10))

        # postion station 
        dhbox2 = wx.BoxSizer(wx.HORIZONTAL)

        dtxt2 = wx.StaticText(self, label="Position  :")
        dtxt2.SetForegroundColour('white')
        dtxt2.SetFont(wx.Font(16,75, 90, 90, faceName=fname))
        dhbox2.Add(dtxt2, flag=wx.LEFT, border=8)

        self.ddata2 = wx.TextCtrl(
                self, wx.ID_ANY, "--", size=(140, 30), style=wx.TE_CENTRE)
        self.ddata2.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        self.ddata2.SetForegroundColour('yellow')
        self.ddata2.SetBackgroundColour('black')
        dhbox2.Add(self.ddata2, flag=wx.LEFT, border=8)

        dvbox.Add(dhbox2, flag=wx.EXPAND|wx.LEFT|wx.TOP, border=5)

        dvbox.Add((-1, 10))

        dhbox3 = wx.BoxSizer(wx.HORIZONTAL)
        dtxt3 = wx.StaticText(self, label='Shutter   :')
        dtxt3.SetForegroundColour('white')
        dtxt3.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        dhbox3.Add(dtxt3, flag=wx.LEFT, border=8)

        self.ddata3 = wx.TextCtrl(
                self, wx.ID_ANY, "--", size=(140, 30), style=wx.TE_CENTRE)
        self.ddata3.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        self.ddata3.SetForegroundColour('yellow')
        self.ddata3.SetBackgroundColour('black')
        dhbox3.Add(self.ddata3, flag=wx.LEFT, border=8)

        dvbox.Add(dhbox3, flag=wx.EXPAND|wx.LEFT|wx.TOP, border=5)

        dvbox.Add((-1, 10))



        ######################################
        # Touch Control Buttons
        ######################################
        dhbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.dbtn1 = wx.Button(self, label='Open', size=(70,50))
        self.dbtn1.SetForegroundColour('black')
        self.dbtn1.SetBackgroundColour('#0873FF')
        self.dbtn1.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        dhbox5.Add(self.dbtn1, flag=wx.LEFT, border=8)

        self.dbtn2 = wx.Button(self, label='Right', size=(70,50))
        self.dbtn2.SetForegroundColour('black')
        self.dbtn2.SetBackgroundColour('#0873FF')
        self.dbtn2.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        dhbox5.Add(self.dbtn2,flag=wx.LEFT, border=8)

        self.dbtn5 = wx.Button(self, label='Auto', size=((80,50)))
        self.dbtn5.SetForegroundColour('black')
        self.dbtn5.SetBackgroundColour('red')
        self.dbtn5.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        dhbox5.Add(self.dbtn5, flag=wx.LEFT, border=8)


        dvbox.Add(dhbox5, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        dvbox.Add((-1, 5))
        dhbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.dbtn4 = wx.Button(self, label='Close', size=((70,50)))
        self.dbtn4.SetForegroundColour('black')
        self.dbtn4.SetBackgroundColour('#0873FF')
        self.dbtn4.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        dhbox6.Add(self.dbtn4, flag=wx.LEFT, border=8)
        self.dbtn3 = wx.Button(self, label='Left', size=(70,50))
        self.dbtn3.SetForegroundColour('black')
        self.dbtn3.SetBackgroundColour('#0873FF')
        self.dbtn3.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))
        dhbox6.Add(self.dbtn3, flag=wx.LEFT, border=8)

        self.dbtn6 = wx.Button(self, label='HOME', size=(80,50))
        self.dbtn6.SetForegroundColour('black')
        self.dbtn6.SetBackgroundColour('green')
        self.dbtn6.SetFont(wx.Font(14, 75, 90, 90, faceName=fname))


        dhbox6.Add(self.dbtn6,flag=wx.LEFT, border=8)
        dvbox.Add(dhbox6, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.SetSizer(dvbox)

        self.dome_mode='Manual'

        # binding events for gui buttons 

        self.dbtn1.Bind(wx.EVT_BUTTON, self.OnOpen)
        self.dbtn2.Bind(wx.EVT_BUTTON, self.OnRight)
        self.dbtn3.Bind(wx.EVT_BUTTON, self.OnLeft)
        self.dbtn4.Bind(wx.EVT_BUTTON, self.OnClose)
        self.dbtn5.Bind(wx.EVT_BUTTON, self.OnAuto)
        self.dbtn6.Bind(wx.EVT_BUTTON, self.OnHome)


    def OnHome(self, event):
        data=b'MH'
        stell_server.domeClient(data)

    def OnAuto(self, event):
        err=stell_server.createDomeTCP()
        if err == False :
            self.ddata1.AppendText('Offline')
            self.ddata3.Clear()
            self.ddata3.AppendText('XX')
            self.ddata2.Clear()
            self.ddata2.AppendText('XX')

    def OnOpen(self, event):
        data=b'MO'
        stell_server.domeClient(data)

    def OnClose(self, event):
        data=b'MC'
        stell_server.domeClient(data)

    def OnLeft(self, event):
        data=b'ML'
        stell_server.domeClient(data)

    def OnRight(self, event):
        data=b'MR'
        stell_server.domeClient(data)



    def update_data(self,event):
        dome_pos= int(data[0]+data[1],16)
        self.ddata1.Clear()
        self.ddata1.AppendText(str(dome_pos))

    def domeTcpMon(self):    
        data=''
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.168.1.4'
        port = 10080
        #ThreadCount = 0
        try:
            ServerSocket.bind((host, port))
            tcs.maher.info('Dome monitor server created - Port(%s)', str(port))
        except socket.error as e:
            ServerSocket.close()
            tcs.maher.error('Dome monitor server Failed :%s', str(e))
        try:
            ServerSocket.listen(5)
            Client, address = ServerSocket.accept()
            self.ddata1.Clear()
            self.ddata1.AppendText('Online')
        except:
            ServerSocket.close()
            self.ddata1.Clear()
            self.ddata1.AppendText('Offline')
            self.ddata3.Clear()
            self.ddata3.AppendText('X')
            self.ddata2.Clear()
            self.ddata2.AppendText('X')
            tcs.maher.error('Dome Controller Connection ERORR: :%s', str(socket.error))

        while True:
            try:
                dome_data= Client.recv(3)
                if dome_data != '':
                    dome_dd= ':'.join('{:02x}'.format(x) for x in dome_data)
                    #print(dome_dd)
                    #00:00:01:00 -- frame example door:home:sign:angle
                    #dome_pos= int(dome_dd[0]+dome_dd[1],16)
                    
                    if dome_dd[4]=='1' :
                        self.ddata2.Clear()
                        self.ddata2.AppendText('Home');
                    else: 
                            dome_pos= Client.recv(4)
                            ang= ''.join('{:02x}'.format(x) for x in dome_pos )
                            ang= int(ang,16)
                            print(ang)
                            if dome_dd[7] == '1':
                                self.ddata2.Clear()
                                self.ddata2.AppendText('L:'+str(ang))
                            else:
                                self.ddata2.Clear()
                                self.ddata2.AppendText('R:'+str(ang))
                    if dome_dd[1]=='1':
                        self.ddata3.Clear()
                        self.ddata3.AppendText('L-Open')
                    elif dome_dd[1]=='2':
                        self.ddata3.Clear()
                        self.ddata3.AppendText('M-Open')
                    elif dome_dd[1]=='3':
                        self.ddata3.Clear()
                        self.ddata3.AppendText('H-Open')
                    elif dome_dd[1]=='4':
                        self.ddata3.Clear()
                        self.ddata3.AppendText('F-Open')
                    else:
                        self.ddata3.Clear()
                        self.ddata3.AppendText('Closed')
                    time.sleep(1)
                elif dome_data == '':
                    self.ddata1.Clear()
                    self.ddata1.AppendText('Offline')

            except socket.error:
                self.ddata1.Clear()
                self.ddata1.AppendText('Offline')
                self.ddata3.Clear()
                self.ddata3.AppendText('X')
                self.ddata2.Clear()
                self.ddata2.AppendText('X')
                tcs.maher.error('Dome Controller Connection ERORR: :%s', str(socket.error))
            #print(dome_data)
            