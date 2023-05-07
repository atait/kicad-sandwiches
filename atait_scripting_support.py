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

# Broaden paths
path_kisandwiches = os.path.dirname(__file__)
if path_kisandwiches not in sys.path:
    sys.path.append(path_kisandwiches)

path_kicad_user_plugins = os.path.dirname(path_kisandwiches)
path_kicad_user_scripting = os.path.dirname(path_kicad_user_plugins)
if path_kicad_user_scripting not in sys.path:
    sys.path.append(path_kicad_user_scripting)

# Expose pcbnew if not in application context
try:
    import pcbnew
except ImportError:
    path_pcbnew_pymodule = os.environ.get('PCBNEW_PATH', None)
    if path_pcbnew_pymodule:
        if os.path.basename(path_pcbnew_pymodule) != 'pcbnew.py':
            raise EnvironmentError(
                'Incorrect location for \'PCBNEW_PATH\' ({}).'
                ' It should point to a file called pcbnew.py'.format(path_pcbnew_pymodule))
        if not os.path.isfile(path_pcbnew_pymodule):
            raise EnvironmentError(
                'Incorrect location for \'PCBNEW_PATH\' ({}).'
                ' File does not exist'.format(path_pcbnew_pymodule))
        sys.path.insert(0, os.path.dirname(path_pcbnew_pymodule))
        import pcbnew
    else:
        pcbnew = None

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
