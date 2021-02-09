# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Feb  2 2021)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class KisandwichGUI
###########################################################################

class KisandwichGUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Kisandwich", pos = wx.Point( 100,100 ), size = wx.Size( 465,500 ), style = wx.DEFAULT_DIALOG_STYLE|wx.BORDER_THEME|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_bitmap1, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Wich board" ), wx.VERTICAL )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioBtn_TOP = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Top", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        self.m_radioBtn_TOP.SetMinSize( wx.Size( 100,-1 ) )

        bSizer3.Add( self.m_radioBtn_TOP, 0, wx.EXPAND, 5 )

        self.m_filePicker_TOP = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"/home/atait/Documents/git-research/github-various/wxFormBuilder/.gitignore", u"Select a file", u"*.kicad_pcb", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
        self.m_filePicker_TOP.SetMinSize( wx.Size( 320,-1 ) )

        bSizer3.Add( self.m_filePicker_TOP, 0, wx.ALL, 5 )


        sbSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioBtn_LOW = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Low", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioBtn_LOW.SetMinSize( wx.Size( 100,-1 ) )

        bSizer31.Add( self.m_radioBtn_LOW, 0, wx.EXPAND, 5 )

        self.m_filePicker_LOW = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"/home/atait/Documents/git-research/github-various/wxFormBuilder/.gitignore", u"Select a file", u"*.kicad_pcb", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
        self.m_filePicker_LOW.SetMinSize( wx.Size( 320,-1 ) )

        bSizer31.Add( self.m_filePicker_LOW, 0, wx.ALL, 5 )


        sbSizer1.Add( bSizer31, 1, wx.EXPAND, 5 )

        bSizer311 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioBtn_BOTH = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Both", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioBtn_BOTH.SetMinSize( wx.Size( 100,-1 ) )

        bSizer311.Add( self.m_radioBtn_BOTH, 0, wx.EXPAND, 5 )


        sbSizer1.Add( bSizer311, 1, wx.EXPAND, 5 )


        bSizer1.Add( sbSizer1, 1, wx.ALL|wx.EXPAND, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Processor Settings" ), wx.HORIZONTAL )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_optTracks = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Tracks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optTracks.SetValue(True)
        bSizer15.Add( self.m_optTracks, 0, wx.SHAPED, 5 )

        self.m_optDrawings = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Drawings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optDrawings.SetValue(True)
        bSizer15.Add( self.m_optDrawings, 0, wx.SHAPED, 5 )

        self.m_optModules = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Modules", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optModules.SetValue(True)
        bSizer15.Add( self.m_optModules, 0, wx.SHAPED, 5 )

        self.m_optVias = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Vias", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optVias.SetValue(True)
        bSizer15.Add( self.m_optVias, 0, wx.SHAPED, 5 )

        self.m_optZones = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Zones", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optZones.SetValue(True)
        bSizer15.Add( self.m_optZones, 0, wx.SHAPED, 5 )

        self.m_optZonesRemoveKeepouts = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Remove\nkeepouts", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.m_optZonesRemoveKeepouts, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )


        sbSizer2.Add( bSizer15, 1, wx.EXPAND, 5 )

        gSizer1 = wx.GridSizer( 3, 3, 0, 0 )

        self.m_staticText4 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Bond pad solder\nmask coverage", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        gSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.m_bpopt_maskCoverage = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"1.1", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_maskCoverage, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_staticText10 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Minima", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        gSizer1.Add( self.m_staticText10, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"BP diam. (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        gSizer1.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.m_bpopt_padCoerce = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"uniform", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_padCoerce, 0, wx.ALL, 5 )

        self.m_bpopt_padMinimum = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_padMinimum, 0, wx.ALL, 5 )

        self.m_staticText51 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"BP drill (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText51.Wrap( -1 )

        gSizer1.Add( self.m_staticText51, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.m_bpopt_drillCoerce = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"uniform", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_drillCoerce, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_bpopt_drillMinimum = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_drillMinimum, 0, wx.ALL, 5 )


        sbSizer2.Add( gSizer1, 1, 0, 5 )


        bSizer1.Add( sbSizer2, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_chkbox_updating = wx.CheckBox( self, wx.ID_ANY, u"Update window", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_chkbox_updating.SetValue(True)
        bSizer10.Add( self.m_chkbox_updating, 0, wx.ALL, 5 )

        self.m_chkbox_saving = wx.CheckBox( self, wx.ID_ANY, u"Save to file", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.m_chkbox_saving, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer10, 1, wx.ALIGN_CENTER, 5 )

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
        self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
        m_sdbSizer1.Realize();

        bSizer1.Add( m_sdbSizer1, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CHAR_HOOK, self.on_char )
        self.Bind( wx.EVT_CLOSE, self.execute )
        self.m_radioBtn_TOP.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_radioBtn_LOW.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_radioBtn_BOTH.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_chkbox_updating.Bind( wx.EVT_CHECKBOX, self.on_updating )
        self.m_chkbox_saving.Bind( wx.EVT_CHECKBOX, self.on_saving )
        self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.cancel )
        self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.execute )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def on_char( self, event ):
        event.Skip()

    def execute( self, event ):
        event.Skip()

    def on_radioboth( self, event ):
        event.Skip()



    def on_updating( self, event ):
        event.Skip()

    def on_saving( self, event ):
        event.Skip()

    def cancel( self, event ):
        event.Skip()



