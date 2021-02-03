# -*- coding: utf-8 -*-


import wx.xrc

###########################################################################
## Class KisandwichGUI
###########################################################################

class KisandwichGUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Kisandwich", pos = wx.DefaultPosition, size = wx.Size( 300,400 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Some text:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )

        # self.radio_sch = wx.RadioButton( self, wx.ID_ANY, u"Radio", wx.DefaultPosition, wx.DefaultSize, 0, style = wx.RB_GROUP )
        lblList = ['Top board (T)', 'Lower board (L)', 'Both']
        self.rb_boardsel = wx.RadioBox(self, wx.ID_ANY, u'RadioBox', wx.DefaultPosition, wx.DefaultSize, choices = lblList ,
           majorDimension = 1, style = wx.RA_SPECIFY_COLS)
        bSizer4.Add( self.rb_boardsel, 0, wx.ALL, 5 )

        self.chkbox_displaying = wx.CheckBox( self, wx.ID_ANY, u"Display in window (Ctrl-Z works)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkbox_displaying.SetValue(True)
        bSizer4.Add( self.chkbox_displaying, 0, wx.ALL, 5 )

        self.chkbox_saving = wx.CheckBox( self, wx.ID_ANY, u"Save to file", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkbox_saving.SetValue(False)
        bSizer4.Add( self.chkbox_saving, 0, wx.ALL, 5 )

        self.chkbox_vrmling = wx.CheckBox( self, wx.ID_ANY, u"Save VRML", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkbox_vrmling.SetValue(False)
        bSizer4.Add( self.chkbox_vrmling, 0, wx.ALL, 5 )

        self.diag = wx.DirPickerCtrl(self, size=wx.DefaultSize)
        bSizer4.Add(self.diag, 0, wx.ALL, 5)

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button3 = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button3, 0, wx.ALL, 5 )

        self.m_button4 = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button4, 0, wx.ALL, 5 )


        bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer4 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.rb_boardsel.Bind( wx.EVT_RADIOBOX, self.radio_toggle )
        self.chkbox_displaying.Bind( wx.EVT_CHECKBOX, self.displaying_toggle )
        self.chkbox_saving.Bind( wx.EVT_CHECKBOX, self.saving_toggle )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def radio_toggle( self, event ):
        event.Skip()

    def saving_toggle( self, event ):
        event.Skip()

    def displaying_toggle( self, event ):
        event.Skip()



