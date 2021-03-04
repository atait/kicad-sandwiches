import traceback
from atait_scripting_support import reload, notify, expose_kicad_python

try:
    expose_kicad_python()
    from kisandwich import action_plugin, core, gui_dialog
    reload(action_plugin)
    reload(core)
    reload(gui_dialog)

    from .action_plugin import Kisandwich # Note the relative import!
    Kisandwich().register()  # Instantiate and register to Pcbnew
    from .core import *
except Exception as e:
    try:
        notify('Kisandwich import failed\n' + traceback.format_exc())
    except Exception:
        pass


class objview(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, val):
        self.__setitem__(attr, val)
