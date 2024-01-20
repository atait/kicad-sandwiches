A simple example of entry point development based on kigadgets. 
Made by Alex Tait

GUI: move this directory to .../kicad/scripting, restart, then click the button

CLI: `python mousebite_script.py mousebite_example.kicad_pcb`


MacOS and KiCAD v7

`_pcbnew.so` will not import in regular pythons as of v7. They are still working on fixing that. What you need to do is:

alias kipython="/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3"
# put this in your ~/.profile or use a symlink to /usr/local/bin instead

kipython -m pip install kigadgets
# or for developer version
kipython -m pip install -e /path/to/kicad-python

kipython mousebite_script.py mousebite_example.kicad_pcb
