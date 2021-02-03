''' This is the simplest script that will be visible in the pcbnew plugin menu '''
import wx
import pcbnew
import os, sys

def notify(text):
    dialog = wx.MessageDialog(None, text, 'One Push debug output', wx.OK)
    sg = dialog.ShowModal()
    return sg


from . import kisandwich_core
from .kisandwich_core import sandwich_from_gui, process_all, base_to_default_boardfile
from . import kisandwich_GUI
from .kisandwich_GUI import KisandwichGUI as KisandwichGUI


class KisandwichDialog(KisandwichGUI):
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    def __init__(self, parent):
        super().__init__(parent)
        self.livepcb = pcbnew.GetBoard()
        pcbpath = self.livepcb.GetFileName()
        self.m_bitmap1.SetBitmap(wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'kisandwich_ico.png'), wx.BITMAP_TYPE_ANY
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

    # def OnChar(self, event):
    #     key = event.GetKeyCode()
    #     if key == wx.WXK_RETURN:
    #         self.execute(event)
    #     elif key == 0:
    #         pass
    #     else:
    #         event.Skip()

    # def OnQuit(self, event):
    #     os.path.remove(self.livefile)
    #     event.Skip()

    # def SetSizeHints(self, sz1, sz2):
    #     try:
    #         # wxPython 3
    #         self.SetSizeHintsSz(sz1, sz2)
    #     except TypeError:
    #         # wxPython 4
    #         super(ArchiveDialog, self).SetSizeHints(sz1, sz2)
    # def __init__(self, parent):
    #     archive_project_GUI.ArchiveGUI.__init__(self, parent)
    #     self.Fit()

    # def schematics_toggle(self, event):
    #     if self.m_chkbox_sch.GetValue():
    #         self.m_chkbox_pdf.Enable()
    #     else:
    #         self.m_chkbox_pdf.Disable()

    #     event.Skip()

class Kisandwich(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "kisandwich"
        self.category = "kisandwich"
        self.description = "Create multi-PCB projects"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(
                os.path.dirname(__file__), 'kisandwich_ico.png')

    def Run(self):
        from importlib import reload
        import kisandwich, kisandwich.kisandwich_core
        # reload(kisandwich)
        reload(kisandwich.kisandwich_core)

        # load board
        livepcb = pcbnew.GetBoard()
        # go to the project folder - so that log will be in proper place
        os.chdir(os.path.dirname(os.path.abspath(livepcb.GetFileName())))
        # find pcbnew frame
        _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]

        # show dialog
        main_dialog = KisandwichDialog(_pcbnew_frame)
        main_res = main_dialog.ShowModal()

        # sanitize values
        if main_dialog.m_chkbox_saving.GetValue():
            files = dict(
                TOP=os.path.abspath(main_dialog.m_filePicker_TOP.GetPath()),
                LOW=os.path.abspath(main_dialog.m_filePicker_LOW.GetPath())
            )
        else:
            files = dict(TOP=None, LOW=None)

        if main_res == wx.ID_OK:
            # notify('OK')
            pass
        else:
            # notify('CANCEL')
            return

        script_kw = dict(refresh=main_dialog.m_chkbox_updating.GetValue())
        if main_dialog.m_radioBtn_TOP.GetValue():
            sandwich_from_gui('TOP', outfile=files['TOP'], **script_kw)
        elif main_dialog.m_radioBtn_LOW.GetValue():
            sandwich_from_gui('LOW', outfile=files['LOW'], **script_kw)
        elif main_dialog.m_radioBtn_BOTH.GetValue():
            assert not script_kw['refresh']
            sandwich_from_gui('TOP', outfile=files['TOP'], **script_kw)
            sandwich_from_gui('LOW', outfile=files['LOW'], **script_kw)
