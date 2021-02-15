''' This is the simplest script that will be visible in the pcbnew plugin menu '''
import wx
import pcbnew
import os, sys
from atait_scripting_support import notify, reload

from . import core
from .core import sandwich_from_gui, process_all, base_to_default_boardfile, objview
from . import gui_dialog
from .gui_dialog import KisandwichGUI


class KisandwichDialog(KisandwichGUI):
    _previous_selections = None

    # hack for new wxFormBuilder generating code incompatible with old wxPython
    def __init__(self, parent):
        super(KisandwichDialog, self).__init__(parent)
        self.m_bitmap1.SetBitmap(wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'icons/sandwich-32.png'), wx.BITMAP_TYPE_ANY
        ))
        self.terminal_choiceOK.SetDefault()

        self.setup_GUI_selections(type(self)._previous_selections)

    # hack for new wxFormBuilder generating code incompatible with old wxPython
    def SetSizeHints(self, sz1, sz2):
        try:
            # wxPython 3
            self.SetSizeHintsSz(sz1, sz2)
        except TypeError:
            # wxPython 4
            super(KisandwichDialog, self).SetSizeHints(sz1, sz2)

    def on_radioboth( self, event ):
        if self.m_radioBtn_BOTH.GetValue():
            self.m_chkbox_saving.SetValue(True)
            self.m_chkbox_saving.Disable()
            self.m_chkbox_updating.SetValue(False)
            self.m_chkbox_updating.Disable()
        else:
            self.m_chkbox_saving.Enable()
            self.m_chkbox_saving.SetValue(False)
            self.m_chkbox_updating.Enable()
            self.m_chkbox_updating.SetValue(True)

        event.Skip()

    def on_saving( self, event ):
        event.Skip()

    def on_updating( self, event ):
        event.Skip()

    def get_user_selections(self):
        # Process files and which boards will be done
        sel = objview()
        if self.m_radioBtn_TOP.GetValue():
            sel['wich'] = 'TOP'
        elif self.m_radioBtn_LOW.GetValue():
            sel['wich'] = 'LOW'
        elif self.m_radioBtn_BOTH.GetValue():
            sel['wich'] = 'BOTH'
        sel['files'] = objview(
            TOP=os.path.abspath(self.m_filePicker_TOP.GetPath()),
            LOW=os.path.abspath(self.m_filePicker_LOW.GetPath())
        )
        sel['saving'] = bool(self.m_chkbox_saving.GetValue())
        sel['refresh'] = bool(self.m_chkbox_updating.GetValue())

        # Process options
        sel['proc_opts'] = objview()
        sel['proc_opts']['enable'] = objview(
            tracks=bool(self.m_optTracks.GetValue()),
            drawings=bool(self.m_optDrawings.GetValue()),
            modules=bool(self.m_optModules.GetValue()),
            vias=bool(self.m_optVias.GetValue()),
            zones=bool(self.m_optZones.GetValue())
        )

        sel.proc_opts.vias = objview(
            coverage_ratio=float(self.m_bpopt_maskCoverage.GetValue()),
            # surface=bool(self.m_bpOpt_surface.GetValue())
        )
        def default_float(textctrl, key):
            if textctrl.GetValue() not in ['uniform', 'minimum']:
                sel.proc_opts.vias[key] = float(textctrl.GetValue())
        default_float(self.m_bpopt_maskCoverage, 'coverage_ratio')
        default_float(self.m_bpopt_padCoerce, 'diameter_override')
        default_float(self.m_bpopt_padMinimum, 'diameter_minimum')
        default_float(self.m_bpopt_drillCoerce, 'drill_override')
        default_float(self.m_bpopt_drillMinimum, 'drill_minimum')

        sel.proc_opts.zones = objview(
            remove_keepouts=bool(self.m_optZonesRemoveKeepouts.GetValue())
        )

        if self.m_modules_inside.GetValue():
            sel.proc_opts.sandwich_type = 'inside'
        if self.m_modules_outside.GetValue():
            sel.proc_opts.sandwich_type = 'outside'
        if self.m_modules_none.GetValue():
            sel.proc_opts.sandwich_type = 'none'

        sel.proc_opts.drawings = objview()
        if self.m_drawings_bondMasks.GetValue():
            sel.proc_opts.drawings.bond_masks = True
        elif self.m_drawings_bondMargin.GetValue():
            sel.proc_opts.drawings.bond_masks = False

        type(self)._previous_selections = sel

        return sel

    def setup_GUI_selections(self, sel=None):
        if sel is None:
            livepcb = pcbnew.GetBoard()
            pcbpath = livepcb.GetFileName()
            self.m_filePicker_TOP.SetPath(base_to_default_boardfile(pcbpath, 'TOP', subdirectory='kisandwich-out'))
            self.m_filePicker_LOW.SetPath(base_to_default_boardfile(pcbpath, 'LOW', subdirectory='kisandwich-out'))
            return
        else:
            self.m_filePicker_TOP.SetPath(sel.files.TOP)
            self.m_filePicker_LOW.SetPath(sel.files.LOW)

            self.m_radioBtn_TOP.SetValue(sel.wich == 'TOP')
            self.m_radioBtn_LOW.SetValue(sel.wich == 'LOW')
            self.m_radioBtn_BOTH.SetValue(sel.wich == 'BOTH')
            self.m_chkbox_saving.SetValue(sel.saving)
            self.m_chkbox_updating.SetValue(sel.refresh)

            self.m_modules_inside.SetValue(sel.proc_opts.sandwich_type == 'inside')
            self.m_modules_outside.SetValue(sel.proc_opts.sandwich_type == 'outside')
            self.m_modules_none.SetValue(sel.proc_opts.sandwich_type == 'none')

            self.m_optTracks.SetValue(sel.proc_opts.enable.tracks)
            self.m_optDrawings.SetValue(sel.proc_opts.enable.drawings)
            self.m_optModules.SetValue(sel.proc_opts.enable.modules)
            self.m_optVias.SetValue(sel.proc_opts.enable.vias)
            self.m_optZones.SetValue(sel.proc_opts.enable.zones)

            def default_str(textctrl, key):
                if key in sel.proc_opts.vias:
                    textctrl.SetValue('{:.3f}'.format(sel.proc_opts.vias[key]))
            default_str(self.m_bpopt_maskCoverage, 'coverage_ratio')
            default_str(self.m_bpopt_padCoerce, 'diameter_override')
            default_str(self.m_bpopt_padMinimum, 'diameter_minimum')
            default_str(self.m_bpopt_drillCoerce, 'drill_override')
            default_str(self.m_bpopt_drillMinimum, 'drill_minimum')

            self.m_optZonesRemoveKeepouts.SetValue(sel.proc_opts.zones.remove_keepouts)

            self.m_drawings_bondMasks.SetValue(sel.proc_opts.drawings.bond_masks is True)
            self.m_drawings_bondMargin.SetValue(sel.proc_opts.drawings.bond_masks is False)


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
        sel = main_dialog.get_user_selections()

        if main_res == wx.ID_OK:
            # notify('OK')
            pass
        else:
            # notify('CANCEL')
            return

        # sanitize values
        if sel['saving']:
            files = sel['files']
        else:
            files = dict(TOP=None, LOW=None)

        script_kw = dict(refresh=sel['refresh'], proc_opts=sel['proc_opts'])
        if sel['wich'] == 'TOP':
            sandwich_from_gui('TOP', outfile=files['TOP'], **script_kw)
        elif sel['wich'] == 'LOW':
            sandwich_from_gui('LOW', outfile=files['LOW'], **script_kw)
        elif sel['wich'] == 'BOTH':
            assert not script_kw['refresh']
            sandwich_from_gui('TOP', outfile=files['TOP'], **script_kw)
            sandwich_from_gui('LOW', outfile=files['LOW'], **script_kw)
