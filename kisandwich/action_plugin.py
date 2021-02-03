''' This is the simplest script that will be visible in the pcbnew plugin menu '''
import wx
import pcbnew
import os, sys
from atait_scripting_support import notify, reload

from . import core
from .core import sandwich_from_gui, process_all, base_to_default_boardfile
from . import gui_dialog
from .gui_dialog import KisandwichGUI


class KisandwichDialog(KisandwichGUI):
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    def __init__(self, parent):
        super().__init__(parent)
        self.livepcb = pcbnew.GetBoard()
        pcbpath = self.livepcb.GetFileName()
        self.m_bitmap1.SetBitmap(wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'icons/sandwich-32.png'), wx.BITMAP_TYPE_ANY
        ))
        # self.livefile = base_to_default_boardfile(pcbpath, 'temp')
        # self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.m_sdbSizer1OK.SetDefault()
        self.m_filePicker_TOP.SetPath(base_to_default_boardfile(pcbpath, 'TOP', subdirectory='kisandwich-out'))
        self.m_filePicker_LOW.SetPath(base_to_default_boardfile(pcbpath, 'LOW', subdirectory='kisandwich-out'))

    def on_radioboth( self, event ):
        if self.m_radioBtn_BOTH.GetValue():
            self.m_chkbox_saving.SetValue(True)
            self.m_chkbox_saving.Disable()
            self.m_chkbox_updating.SetValue(False)
            self.m_chkbox_updating.Disable()
        else:
            self.m_chkbox_saving.Enable()
            self.m_chkbox_updating.Enable()

        event.Skip()

    def on_saving( self, event ):
        if self.m_chkbox_saving.GetValue():
            self.m_chkbox_vrmling.Enable()
        else:
            self.m_chkbox_vrmling.SetValue(False)
            self.m_chkbox_vrmling.Disable()
        event.Skip()

    def on_updating( self, event ):
        event.Skip()

    def get_user_selections(self):
        sel = dict()
        if self.m_radioBtn_TOP.GetValue():
            sel['wich'] = 'TOP'
        elif self.m_radioBtn_LOW.GetValue():
            sel['wich'] = 'LOW'
        elif self.m_radioBtn_BOTH.GetValue():
            sel['wich'] = 'BOTH'
        sel['files'] = dict(
            TOP=os.path.abspath(self.m_filePicker_TOP.GetPath()),
            LOW=os.path.abspath(self.m_filePicker_LOW.GetPath())
        )
        sel['saving'] = bool(self.m_chkbox_saving.GetValue())
        sel['refreshing'] = bool(self.m_chkbox_updating.GetValue())
        return sel


class Kisandwich(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "kisandwich"
        self.category = "kisandwich"
        self.description = "Create multi-PCB projects"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(
                os.path.dirname(__file__), 'icons/sandwich-32.png')

    def Run(self):
        import kisandwich.core
        reload(kisandwich.core)

        # load board
        livepcb = pcbnew.GetBoard()
        # go to the project folder - so that log will be in proper place
        os.chdir(os.path.dirname(os.path.abspath(livepcb.GetFileName())))
        # find pcbnew frame
        _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]

        # show dialog
        main_dialog = KisandwichDialog(_pcbnew_frame)
        main_res = main_dialog.ShowModal()

        if main_res == wx.ID_OK:
            # notify('OK')
            pass
        else:
            # notify('CANCEL')
            return

        # sanitize values
        sel = main_dialog.get_user_selections()
        if sel['saving']:
            files = sel['files']
        else:
            files = dict(TOP=None, LOW=None)

        script_kw = dict(refresh=sel['refreshing'])
        if sel['wich'] == 'TOP':
            sandwich_from_gui('TOP', outfile=files['TOP'], **script_kw)
        elif sel['wich'] == 'LOW':
            sandwich_from_gui('LOW', outfile=files['LOW'], **script_kw)
        elif sel['wich'] == 'BOTH':
            assert not script_kw['refresh']
            sandwich_from_gui('TOP', outfile=files['TOP'], **script_kw)
            sandwich_from_gui('LOW', outfile=files['LOW'], **script_kw)
