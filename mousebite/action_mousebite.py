''' Entry point for onepush_script.py
    On OSX, you can hotkey the corresponding menu item: "One Push"
'''
from atait_scripting_support import reload, notify
import pcbnew
import os, sys

class MouseBite(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "MouseBite"  # it is important that this matches the shortcut
        self.category = "Fabrication"
        self.description = ("MouseBites on Eco1")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__),
            "icons/photon-32.png")

    def Run(self):
        # The entry function of the plugin that is executed on user action
        import mousebite_script
        reload(mousebite_script)

