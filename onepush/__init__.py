import sys, os
import traceback
sys.path.append(os.path.dirname(__file__))


try:
    from .action_onepush import OnePush
    OnePush().register() # Instantiate and register to Pcbnew
except Exception as e:
    try:
        notify('OnePush import failed\n' + traceback.format_exc())
    except Exception:
        pass
