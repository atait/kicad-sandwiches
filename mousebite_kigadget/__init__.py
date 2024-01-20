import traceback
from kicad.exceptions import notify

class objview(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, val):
        self.__setitem__(attr, val)

    def copy(self):
        return objview(super().copy())

try:
    from .action_mousebite import MouseBite
    MouseBite().register() # Instantiate and register to Pcbnew
except Exception as e:
    try:
        notify('Mousebite import failed\n' + traceback.format_exc())
    except Exception:
        pass

