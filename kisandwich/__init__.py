import sys, os
import traceback


class objview(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, val):
        self.__setitem__(attr, val)

    def copy(self):
        return objview(super().copy())

try:
    # expose_kicad_python()
    from kigadgets import kireload
    from kisandwich import action_plugin, core, gui_dialog
    kireload(action_plugin)
    kireload(core)
    kireload(gui_dialog)

    from .action_plugin import Kisandwich # Note the relative import!
    Kisandwich().register()  # Instantiate and register to Pcbnew
    from .core import *
except Exception as e:
    try:
        from kigadgets import notify
        notify('Kisandwich import failed\n' + traceback.format_exc())
    except Exception:
        pass


