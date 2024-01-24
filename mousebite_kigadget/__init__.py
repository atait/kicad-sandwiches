import traceback

import sys, os
sys.path.append(os.path.dirname(__file__))

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
        from kigadgets import notify
        notify('Mousebite import failed\n' + traceback.format_exc())
    except Exception:
        pass

