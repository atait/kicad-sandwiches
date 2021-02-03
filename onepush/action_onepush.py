''' Entry point for onepush_script.py
    Hotkey the corresponding menu item: "One Push"
'''
from atait_scripting_support import reload
import pcbnew
import os, sys

class OnePush(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "One Push"  # it is important that this matches the shortcut
        self.category = "Macro speedup"
        self.description = ("Run a script like a macro at the touch of a button. "
                           "Edit the script at " + os.path.join(os.path.dirname(__file__), "onepush_script.py"))
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__),
            "icons/photon-32.png")

    def Run(self):
        # The entry function of the plugin that is executed on user action
        import onepush_script
        reload(onepush_script)

OnePush().register() # Instantiate and register to Pcbnew
