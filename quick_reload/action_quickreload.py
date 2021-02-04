''' Entry point for onepush_script.py
    On OSX, you can hotkey the corresponding menu item: "Quick Reload"
'''
import pcbnew
import wx
import os, sys
from .gui_dialog import QuickReloadGUI

hidefuture_life_of_application = False
class QuickReload(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Quick Reload"  # it is important that this matches the shortcut
        self.category = "Macro speedup"
        self.description = "Unsafe, instant reload of current board from file."
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__),
            "icons/reload-32.png")

    def Run(self):
        # The entry function of the plugin that is executed on user action
        global hidefuture_life_of_application
        if not hidefuture_life_of_application:
            _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
            main_gui = QuickReloadGUI(_pcbnew_frame)
            main_res = main_gui.ShowModal()
            if main_res == wx.ID_OK:
                pass
            else:
                return

            if main_gui.m_checkBox_hidefuture.GetValue():
                hidefuture_life_of_application = True

        pcb = pcbnew.GetBoard()
        file = pcb.GetFileName()
        pcbnew.LoadBoard(file)
        pcbnew.Refresh()
