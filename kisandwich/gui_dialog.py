# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Feb  2 2021)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class KisandwichGUI
###########################################################################

class KisandwichGUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Kisandwich", pos = wx.Point( 100,100 ), size = wx.Size( 465,700 ), style = wx.DEFAULT_DIALOG_STYLE|wx.BORDER_THEME|wx.TAB_TRAVERSAL )

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

        bSizer312 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioBtn_MID = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Mid", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioBtn_MID.SetMinSize( wx.Size( 100,-1 ) )

        bSizer312.Add( self.m_radioBtn_MID, 0, wx.EXPAND, 5 )

        self.m_filePicker_MID = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"/home/atait/Documents/git-research/github-various/wxFormBuilder/.gitignore", u"Select a file", u"*.kicad_pcb", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
        self.m_filePicker_MID.SetMinSize( wx.Size( 320,-1 ) )

        bSizer312.Add( self.m_filePicker_MID, 0, wx.ALL, 5 )


        sbSizer1.Add( bSizer312, 1, wx.EXPAND, 5 )

        bSizer313 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioBtn_STENCIL = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Stencil", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioBtn_STENCIL.SetMinSize( wx.Size( 100,-1 ) )

        bSizer313.Add( self.m_radioBtn_STENCIL, 0, wx.EXPAND, 5 )

        self.m_filePicker_STENCIL = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"/home/atait/Documents/git-research/github-various/wxFormBuilder/.gitignore", u"Select a file", u"*.kicad_pcb", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
        self.m_filePicker_STENCIL.SetMinSize( wx.Size( 320,-1 ) )

        bSizer313.Add( self.m_filePicker_STENCIL, 0, wx.ALL, 5 )


        sbSizer1.Add( bSizer313, 1, wx.EXPAND, 5 )

        bSizer311 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioBtn_ALL = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, u"All", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioBtn_ALL.SetMinSize( wx.Size( 100,-1 ) )

        bSizer311.Add( self.m_radioBtn_ALL, 0, wx.EXPAND, 5 )


        sbSizer1.Add( bSizer311, 1, wx.EXPAND, 5 )


        bSizer1.Add( sbSizer1, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_listbook1 = wx.Listbook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT|wx.BORDER_RAISED )
        self.panel_modules = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED|wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.m_optModules = wx.CheckBox( self.panel_modules, wx.ID_ANY, u"Modules", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optModules.SetValue(True)
        self.m_optModules.Enable( False )

        bSizer8.Add( self.m_optModules, 0, wx.SHAPED, 5 )

        self.m_modules_inside = wx.RadioButton( self.panel_modules, wx.ID_ANY, u"Inside of sandwich\n(Front FP -> LOW board, Back FP -> TOP board)", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        bSizer8.Add( self.m_modules_inside, 0, wx.ALL, 5 )

        self.m_modules_outside = wx.RadioButton( self.panel_modules, wx.ID_ANY, u"Outside of sandwich\n(Front FP -> TOP board, Back FP -> LOW board)", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_modules_outside, 0, wx.ALL, 5 )

        self.m_modules_none = wx.RadioButton( self.panel_modules, wx.ID_ANY, u"No action", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_modules_none, 0, wx.ALL, 5 )


        self.panel_modules.SetSizer( bSizer8 )
        self.panel_modules.Layout()
        bSizer8.Fit( self.panel_modules )
        self.m_listbook1.AddPage( self.panel_modules, u"Modules", True )
        self.panel_tracks = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED|wx.TAB_TRAVERSAL )
        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        self.m_optTracks = wx.CheckBox( self.panel_tracks, wx.ID_ANY, u"Process tracks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optTracks.SetValue(True)
        bSizer11.Add( self.m_optTracks, 0, wx.SHAPED, 5 )

        self.m_grid1 = wx.grid.Grid( self.panel_tracks, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.m_grid1.CreateGrid( 4, 2 )
        self.m_grid1.EnableEditing( True )
        self.m_grid1.EnableGridLines( True )
        self.m_grid1.EnableDragGridSize( False )
        self.m_grid1.SetMargins( 0, 0 )

        # Columns
        self.m_grid1.EnableDragColMove( False )
        self.m_grid1.EnableDragColSize( False )
        self.m_grid1.SetColLabelValue( 0, u"TOP" )
        self.m_grid1.SetColLabelValue( 1, u"LOW" )
        self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.m_grid1.EnableDragRowSize( False )
        self.m_grid1.SetRowLabelValue( 0, u"F.Cu" )
        self.m_grid1.SetRowLabelValue( 1, u"In1.Cu" )
        self.m_grid1.SetRowLabelValue( 2, u"In2.Cu" )
        self.m_grid1.SetRowLabelValue( 3, u"B.Cu" )
        self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.m_grid1.SetDefaultCellTextColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer11.Add( self.m_grid1, 0, wx.ALL, 5 )


        self.panel_tracks.SetSizer( bSizer11 )
        self.panel_tracks.Layout()
        bSizer11.Fit( self.panel_tracks )
        self.m_listbook1.AddPage( self.panel_tracks, u"Tracks", False )
        self.panel_drawings = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED|wx.TAB_TRAVERSAL )
        bSizer101 = wx.BoxSizer( wx.VERTICAL )

        self.m_optDrawings = wx.CheckBox( self.panel_drawings, wx.ID_ANY, u"Process drawings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optDrawings.SetValue(True)
        bSizer101.Add( self.m_optDrawings, 0, wx.SHAPED, 5 )

        self.m_drawings_bondMasks = wx.RadioButton( self.panel_drawings, wx.ID_ANY, u"Bond by flipping B.Mask and F.Mask", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        bSizer101.Add( self.m_drawings_bondMasks, 0, wx.ALL, 5 )

        self.m_drawings_bondMargin = wx.RadioButton( self.panel_drawings, wx.ID_ANY, u"Bond using Margin layer", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_drawings_bondMargin.Enable( False )

        bSizer101.Add( self.m_drawings_bondMargin, 0, wx.ALL, 5 )

        self.m_drawings_bondAdhes = wx.RadioButton( self.panel_drawings, wx.ID_ANY, u"Bond using F.Adhes layer", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer101.Add( self.m_drawings_bondAdhes, 0, wx.ALL, 5 )


        self.panel_drawings.SetSizer( bSizer101 )
        self.panel_drawings.Layout()
        bSizer101.Fit( self.panel_drawings )
        self.m_listbook1.AddPage( self.panel_drawings, u"Drawings", False )
        self.panel_pads = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED|wx.TAB_TRAVERSAL )
        bSizer12 = wx.BoxSizer( wx.VERTICAL )

        self.m_optVias = wx.CheckBox( self.panel_pads, wx.ID_ANY, u"Process THT vias to bond pads", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optVias.SetValue(True)
        bSizer12.Add( self.m_optVias, 0, wx.ALL, 5 )

        self.m_bpOpt_shrink = wx.CheckBox( self.panel_pads, wx.ID_ANY, u"Remove opposite side plating", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_bpOpt_shrink.SetValue(True)
        bSizer12.Add( self.m_bpOpt_shrink, 0, wx.ALL, 5 )

        self.m_bpOpt_surface = wx.CheckBox( self.panel_pads, wx.ID_ANY, u"Delete drill (bad idea)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_bpOpt_surface.Enable( False )

        bSizer12.Add( self.m_bpOpt_surface, 0, wx.ALL, 5 )

        gSizer1 = wx.GridSizer( 3, 3, 0, 0 )

        self.m_staticText4 = wx.StaticText( self.panel_pads, wx.ID_ANY, u"Bond pad solder\nmask coverage", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        gSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.m_bpopt_maskCoverage = wx.TextCtrl( self.panel_pads, wx.ID_ANY, u"1.1", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_maskCoverage, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_staticText10 = wx.StaticText( self.panel_pads, wx.ID_ANY, u"Minima", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        gSizer1.Add( self.m_staticText10, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( self.panel_pads, wx.ID_ANY, u"BP diam. (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        gSizer1.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.m_bpopt_padCoerce = wx.TextCtrl( self.panel_pads, wx.ID_ANY, u"uniform", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_padCoerce, 0, wx.ALL, 5 )

        self.m_bpopt_padMinimum = wx.TextCtrl( self.panel_pads, wx.ID_ANY, u"minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_padMinimum, 0, wx.ALL, 5 )

        self.m_staticText51 = wx.StaticText( self.panel_pads, wx.ID_ANY, u"BP drill (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText51.Wrap( -1 )

        gSizer1.Add( self.m_staticText51, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.m_bpopt_drillCoerce = wx.TextCtrl( self.panel_pads, wx.ID_ANY, u"uniform", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_drillCoerce, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_bpopt_drillMinimum = wx.TextCtrl( self.panel_pads, wx.ID_ANY, u"minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_bpopt_drillMinimum, 0, wx.ALL, 5 )


        bSizer12.Add( gSizer1, 1, wx.EXPAND, 5 )


        self.panel_pads.SetSizer( bSizer12 )
        self.panel_pads.Layout()
        bSizer12.Fit( self.panel_pads )
        self.m_listbook1.AddPage( self.panel_pads, u"Bond pads", False )
        self.panel_zones = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED|wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_optZones = wx.CheckBox( self.panel_zones, wx.ID_ANY, u"Process zones", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_optZones.SetValue(True)
        bSizer9.Add( self.m_optZones, 0, wx.ALL|wx.SHAPED, 5 )

        self.m_optZonesRemoveKeepouts = wx.CheckBox( self.panel_zones, wx.ID_ANY, u"Remove keepouts", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_optZonesRemoveKeepouts, 0, wx.ALL, 5 )


        self.panel_zones.SetSizer( bSizer9 )
        self.panel_zones.Layout()
        bSizer9.Fit( self.panel_zones )
        self.m_listbook1.AddPage( self.panel_zones, u"Zones", False )
        self.panel_stencil = wx.Panel( self.m_listbook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED|wx.TAB_TRAVERSAL )
        bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText13 = wx.StaticText( self.panel_stencil, wx.ID_ANY, u"Fill radius ratio\nR = x R_pad + (1-x) R_drill", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        bSizer91.Add( self.m_staticText13, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.m_staticText131 = wx.StaticText( self.panel_stencil, wx.ID_ANY, u"... x=", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText131.Wrap( -1 )

        bSizer91.Add( self.m_staticText131, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_stencil_fill = wx.TextCtrl( self.panel_stencil, wx.ID_ANY, u"0.6", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer91.Add( self.m_stencil_fill, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        self.panel_stencil.SetSizer( bSizer91 )
        self.panel_stencil.Layout()
        bSizer91.Fit( self.panel_stencil )
        self.m_listbook1.AddPage( self.panel_stencil, u"Stencil", False )

        bSizer1.Add( self.m_listbook1, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_chkbox_updating = wx.CheckBox( self, wx.ID_ANY, u"Update window", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_chkbox_updating.SetValue(True)
        bSizer10.Add( self.m_chkbox_updating, 0, wx.ALL, 5 )

        self.m_chkbox_saving = wx.CheckBox( self, wx.ID_ANY, u"Save to file", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.m_chkbox_saving, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer10, 1, wx.ALIGN_CENTER, 5 )

        terminal_choice = wx.StdDialogButtonSizer()
        self.terminal_choiceOK = wx.Button( self, wx.ID_OK )
        terminal_choice.AddButton( self.terminal_choiceOK )
        self.terminal_choiceCancel = wx.Button( self, wx.ID_CANCEL )
        terminal_choice.AddButton( self.terminal_choiceCancel )
        terminal_choice.Realize();

        bSizer1.Add( terminal_choice, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CHAR_HOOK, self.on_char )
        self.Bind( wx.EVT_CLOSE, self.execute )
        self.m_radioBtn_TOP.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_radioBtn_LOW.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_radioBtn_MID.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_radioBtn_STENCIL.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_radioBtn_ALL.Bind( wx.EVT_RADIOBUTTON, self.on_radioboth )
        self.m_chkbox_updating.Bind( wx.EVT_CHECKBOX, self.on_updating )
        self.m_chkbox_saving.Bind( wx.EVT_CHECKBOX, self.on_saving )
        self.terminal_choiceCancel.Bind( wx.EVT_BUTTON, self.cancel )
        self.terminal_choiceOK.Bind( wx.EVT_BUTTON, self.execute )

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



