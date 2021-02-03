import sys
try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except ImportError:
        try:
            _ = reload
        except NameError as err:
            raise NameError('Could not determine reload command\nPython: ' + sys.version)

def notify(text):
    try:
        import wx
    except ImportError:
        print(text)
    else:
        dialog = wx.MessageDialog(None, text, 'One Push debug output', wx.OK)
        sg = dialog.ShowModal()
        return sg

try:
    import pcbnew
    from kisandwich import action, core, gui
    reload(action)
    reload(core)
    reload(gui)
    from .action import Kisandwich # Note the relative import!
    Kisandwich().register()  # Instantiate and register to Pcbnew
except Exception as e:
    try:
        notify('Kisandwich import failed\n' + str(e))
    except Exception:
        pass

from .core import *
