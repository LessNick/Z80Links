# Z80Links
Plugin for Sublime Text 2. Adds the ability to move using ctrl + mouse click,  to the ASM(z80) source files, and scroll to place where the label is defined.

# Install #
Simple copy files into your package Sublime Text 2 directory:

    Sublime Text 2/Data/Packages/z80links/

Z80Links menu item will appear in the top panel after installation.

# Usage #

The plugin uses the "labelsList.json" cache file, placed in the project folder, next to the "* .sublime-project" and "* .sublime-workspace" files.

Click the "Rebuild links" menu item to create a "labelsList.json".

This operation is performed once and then the "labelsList.json" file is updated automatically when saving files with the "* .asm" extension

# Licence #

BSD 3-Clause "New" or "Revised" License

# Credits #

2021 © Written by breeze\fishbone crew

