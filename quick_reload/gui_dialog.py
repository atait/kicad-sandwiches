# -*- coding: utf-8 -*-

import wx
import wx.xrc

class QuickReloadGUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer17 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"This script automatically reloads the file of the board in the current without asking whether it is saved. Use with caution. \n\nAre you sure you want to continue?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( 400 )

        bSizer17.Add( self.m_staticText11, 0, wx.ALL, 5 )


        bSizer17.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_checkBox_hidefuture = wx.CheckBox( self, wx.ID_ANY, u"Don't show warning again until Application is restarted", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer17.Add( self.m_checkBox_hidefuture, 0, wx.ALL, 5 )

        m_sdbSizer3 = wx.StdDialogButtonSizer()
        self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
        self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
        m_sdbSizer3.Realize();

        bSizer17.Add( m_sdbSizer3, 1, wx.ALL, 5 )


        self.SetSizer( bSizer17 )
        self.Layout()
        bSizer17.Fit( self )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass
