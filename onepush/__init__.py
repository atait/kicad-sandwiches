import sys, os
import traceback

sys.path.append(os.path.dirname(__file__))
from atait_scripting_support import notify
try:
    from .action_onepush import OnePush
    OnePush().register() # Instantiate and register to Pcbnew
except Exception as e:
    try:
        # from kigadgets import notify
        notify('OnePush import failed\n' + traceback.format_exc())
    except Exception:
        pass
