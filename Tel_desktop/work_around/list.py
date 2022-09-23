import wx

app = wx.App( redirect = False )
wnd = wx.Frame( parent = None )
widget = wx.ListCtrl( parent = wnd, style = wx.LC_REPORT )
widget.InsertColumn( 0, "items" )
widget.InsertStringItem( 0, "foo" )
widget.InsertStringItem( 1, "bar" )
widget.InsertStringItem( 2, "baz" )
widget.Select( 1 )
wnd.Show()
app.MainLoop()
