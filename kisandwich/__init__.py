import traceback

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.1.0"

class objview(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, val):
        self.__setitem__(attr, val)

    def copy(self):
        return objview(super().copy())

try:
    # expose_kicad_python()
    from kigadgets.util import kireload, in_GUI
    from kisandwich import core
    kireload(core)
    if in_GUI():
        from kisandwich import action_plugin, gui_dialog
        kireload(action_plugin)
        kireload(gui_dialog)

        from kisandwich.action_plugin import Kisandwich # Note the relative import!
        Kisandwich().register()  # Instantiate and register to Pcbnew
    from kisandwich.core import *
except Exception as e:
    try:
        from kigadgets import notify
        notify('Kisandwich registration failed\n' + traceback.format_exc())
    except Exception:
        pass
