#!/usr/bin/env python3
import wx
import wx.lib.newevent
import wx.adv
import time
import socket
from bitstring import BitArray, BitStream, ConstBitStream
from threading import Thread
import coords
import struct
import math
import tcs 
import os
#sra=''
#sdec=''
#stime=''
DHOST = '192.168.1.100' # dome server ip
DPORT = 10081           # dome server port
SHOST = '127.0.0.1'  # Standard loopback interface address (localhost)
SPORT = 10001        # Port to listen on (non-privileged ports are > 1023)
def GetMonoFont():

    if os.name == 'nt':
        fname = 'Consolas'
        return fname

    # unknown OS
    else:
        fname = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT) #'helvetica'
        return fname


def createDomeTCP():
    global d
    d= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        d.connect((DHOST,DPORT))
        tcs.maher.info('Dome client connected over :%s', str(DPORT))
        return True
    except socket.error:
        tcs.maher.error('Dome Controller does not reply:%s', str(socket.error))
        d.close()
        return False

    



def domeClient(command):
    data = command
    d.sendall(data)
    tcs.maher.info('Cigar commanded Dome with : %s',data)


def domeGotoTCP(h_angle):
    cmd=b'AA'
    domeClient(cmd)
    angle= int(h_angle)
    val=struct.pack('!i', angle)
    tcs.maher.info('Dome requested to goto angle(%s)',str(angle))
    d.send(val)



class stelPanel(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id, **kwgs):
        # create the panel
        wx.Panel.__init__(self, parent, size=(700,150), **kwgs)
        fname = GetMonoFont()

        #start Stellarium GoTo server 
        self.GotoThread= Thread(target=self.GotoServer, args=())

        shbox = wx.BoxSizer(wx.HORIZONTAL)

        svbox1 = wx.BoxSizer(wx.VERTICAL)
        self.txtTerm = wx.TextCtrl(self, -1,
                "Hello Astronomy Geek,\nPress 'GoTo' to connect with Stellarium Software!\nSelect a sky object then Press Ctrl+1 for auto GoTo Observation. ",
                size=(500, 80), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.txtTerm.SetForegroundColour('yellow')
        self.txtTerm.SetBackgroundColour('black')
        self.txtTerm.SetFont(wx.Font(12, 75, 90, 90, faceName=fname))

        svbox1.Add(self.txtTerm, proportion=1, border=8)
        shbox.Add(svbox1, proportion=1, flag=wx.LEFT |wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)
        shbox.Add((-1, 5))


        svbox2 = wx.BoxSizer(wx.VERTICAL)
        self.sbtn1= wx.Button(self, label='GoTo', size=((100,40)))
        self.sbtn1.SetForegroundColour('black')
        self.sbtn1.SetBackgroundColour('#B22222')
        self.sbtn1.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        svbox2.Add(self.sbtn1, proportion=1, flag=wx.LEFT |wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)


        self.sbtn2= wx.Button(self, label='About', size=((100,40)))
        self.sbtn2.SetForegroundColour('black')
        self.sbtn2.SetBackgroundColour('#B22222')
        self.sbtn2.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        svbox2.Add(self.sbtn2, proportion=1, flag=wx.LEFT |wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)

        self.sbtn3= wx.Button(self, label='Close', size=((100,40)))
        self.sbtn3.SetForegroundColour('black')
        self.sbtn3.SetBackgroundColour('#B22222')
        self.sbtn3.SetFont(wx.Font(16, 75, 90, 90, faceName=fname))
        svbox2.Add(self.sbtn3, proportion=1, flag=wx.LEFT |wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)


        shbox.Add(svbox2, proportion=1, flag=wx.LEFT |wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)
        self.SetSizer(shbox)   



        ################################################
        ### Events binding and handelers
        ###############################################

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.sbtn2.Bind(wx.EVT_BUTTON, self.OnAbout)
        self.sbtn3.Bind(wx.EVT_BUTTON, self.OnCloseWindow)
        self.sbtn1.Bind(wx.EVT_BUTTON, self.stelThread)



    def stelThread(self,evt):
        self.GotoThread.start()
        #self.GotoThread.join()



    def GotoServer(self):
        global sra
        global sdec
        global stime
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SHOST, SPORT))
            try:
                s.listen(5)
                conn, addr = s.accept()
            except socket.error :
                tcs.maher.error('Stellarium Connection ERORR: :%s', str(socket.error))
                self.txtTerm.AppendText('Stellarium Connection ERORR ! \n')
                s.close()
            with conn:
                tcs.maher.info('Stellarium broker is Connected Over Port: %s', str(conn[1]))
                self.txtTerm.Clear()
                self.txtTerm.Clear()
                self.txtTerm.AppendText('Stellarium Connected Over Port:'+ str(addr[1]))
                #self.txtTerm.AppendText(', Port:'+str(addr[1]))
                self.txtTerm.AppendText('\n')
                while True:

                    data0 = conn.recv(160)
                    #print("REC DATA="+str(data0))
                    if data0:            
                        data = ConstBitStream(bytes=data0, length=160)
                        #print(str(data)+'\n')
                        #print "All: %s" % data.bin
                        
                        msize = data.read('intle:16')
                        mtype = data.read('intle:16')
                        mtime = data.read('intle:64')
                        #print("mtime="+str(mtime))
                        
                        # RA: 
                        ant_pos = data.bitpos
                        ra = data.read('hex:32')
                        data.bitpos = ant_pos
                        ra_uint = data.read('uintle:32')
                        #print("RA="+str(ra_uint))
                        
                        # DEC:
                        ant_pos = data.bitpos
                        dec = data.read('hex:32')  
                        data.bitpos = ant_pos
                        dec_int = data.read('intle:32')
                        #print("DEC="+str(dec_int))
                        (sra, sdec, stime) = coords.eCoords2str(float("%f" % ra_uint), float("%f" % dec_int), float("%f" %  mtime))
                        self.txtTerm.AppendText("Object Time="+stime+'\n')
                        #self.txtTerm.AppendText("Object RA="+sra+'\n')
                        #self.txtTerm.AppendText("Object DEC="+sdec+'\n')
                        dome_h_ang= round(((coords.hourStr_2_rad(sra) * 180)/math.pi),0)
                        dec_ang_degree= round(((coords.hourStr_2_rad(sdec) * 180)/math.pi),0) 
                        self.txtTerm.AppendText(" Object RA="+str(dome_h_ang) +'\n')
                        self.txtTerm.AppendText(" Object DEC="+str(dec_ang_degree) +'\n')
                        self.txtTerm.AppendText(">>>>Updating DOME/MOUNT Position\n")
                        tcs.maher.info('Updating DOME Position : %s ', str(dome_h_ang))
                        cs.maher.info('Updating MOUNT Position RA:%s, DEC: %s ', str(dome_h_ang), str(dec_ang_degree))

                        #domeGotoTCP( dome_h_ang)
                        #self.txtTerm.AppendText("in red DEC="+str(coords.degStr_2_rad(sdec)))
                        time.sleep(1)    


    def OnAbout(self, e):

        description = """
        Cigar is an open source tool developed by Mohamed Maher,  
        to control astronomy Telescope systems (Dome/Mount)
        with support of GoTo observation using Stellaruim Software.
        Connect to dome and mount driver over TCP.
        Refer to Stellarium Documentation for details GoTo Function.
        """

        licence = """
        Cigar: Telescope Remote Controller is open source tool,
        Developed by : Mohamed Maher. feel free to copy and distribute this 
        souce code which avaliable on https://github.com/Mr-JoE1.
         """

        info = wx.adv.AboutDialogInfo()
        # info.SetBackgroundColour('DIM GREY')
        info.SetIcon(wx.Icon('logo.ico', wx.BITMAP_TYPE_ANY))
        info.SetName('Cigar: Telescope Remote Controller')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetLicence(licence)
        info.SetCopyright('(C) 2011 - 2021 ')
        info.AddDeveloper('Mohamed Maher')
        info.SetWebSite('https://infinitytech.ltd')
        wx.adv.AboutBox(info)


    def OnCloseWindow(self, e):
        dial = wx.MessageDialog(self, 'Are you sure to quit?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT |wx.ICON_EXCLAMATION)

        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            wx.Exit()
        else:
            e.Skip()
