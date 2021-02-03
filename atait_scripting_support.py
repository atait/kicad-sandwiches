''' Some useful tools when scripting for pcbnew
    This module makes itself visible to all of pcbnew scope when pcbnew is opened

    Use `import reload` to get a module reloader. When pcbnew refreshes scripts, it only reimports.
    When editing the plugins and libraries, changes will not be reflected unless they are explicitly reloaded.
    - To reload when "refresh plugins" is pressed, call the command in an __init__.py file in the "plugins" directory
    - To reload every time an action plugin is run, put the command in its "Run" method

'''
from functools import wraps
import sys, os
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

# Fix paths
path_kisandwiches = os.path.dirname(__file__)
if path_kisandwiches not in sys.path:
    sys.path.append(path_kisandwiches)

path_kicad_user_plugins = os.path.dirname(path_kisandwiches)
path_kicad_user_scripting = os.path.dirname(path_kicad_user_plugins)
if path_kicad_user_scripting not in sys.path:
    sys.path.append(path_kicad_user_scripting)


def in_pcbnew_interpreter():
    try:
        import pcbnew
    except ImportError:
        return False
    else:
        return True


def expose_kicad_python():
    if not in_pcbnew_interpreter():
        raise ImportError(
            'kicad-python can only be used within the scope of pcbnew,'
            'which is not available on command line'
        )
    try:
        import kicad
    except ImportError:
        pass
    else:
        return
    sys.path.append(os.path.join(path_kicad_user_scripting, 'kicad-python'))
    sys.path.append(os.path.join(path_kicad_user_plugins, 'kicad-python'))
    try:
        import kicad
    except ImportError:
        raise ImportError(
            'kicad-python not found. '
            'Download from "https://github.com/KiCad/kicad-python" with\n'
            'cd {}\ngit clone git@github.com:KiCad/kicad-python.git'.format(path_kicad_user_scripting)
        )

def requires_kicad_python(*possiblefunc, autoreload=False):
    if len(possiblefunc) == 0:
        return lambda func: requires_kicad_python(func, autoreload=autoreload)
    elif len(possiblefunc) == 1 and callable(possiblefunc[0]):
        func = possiblefunc[0]
        @wraps(func)
        def wrapped(*args, **kwargs):
            expose_kicad_python()
            if autoreload:
                from kicad.pcbnew import drawing, module, board, layer
                reload(drawing)
                reload(module)
                reload(board)
                reload(layer)
            return func(*args, **kwargs)
        return wrapped
    else:
        raise ValueError('Invalid number of arguments')


# Messages
def notify(*args):
    text = ' '.join(str(arg) for arg in args)
    try:
        import wx
    except ImportError:
        print(text)
    else:
        dialog = wx.MessageDialog(None, text, 'kisandwich debug output', wx.OK)
        sg = dialog.ShowModal()
        return sg
