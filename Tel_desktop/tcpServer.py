import socket
import os
import wx.lib.newevent
import wx
import wx.adv


(UpdateDome, EVT_UPDATE_DOME) = wx.lib.newevent.NewEvent()

class TcpThread:

    def __init__(self, win):
        self.win = win 

    def tcp_init(self):
        data=''
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.168.1.4'
        port = 10080
        #ThreadCount = 0
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Waitiing for a Connection..')
        ServerSocket.listen(5)
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        while True:
            dome_data= Client.recv(4)
            dome_dd= ':'.join('{:02x}'.format(x) for x in dome_data)
            wx.PostEvent(wx.ID_ANY, UpdateDome(data=dome_dd))

    