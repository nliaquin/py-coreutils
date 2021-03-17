#!/bin/bash

##Just a heads up: this script will not overwrite your GNU coreutils
# It will move the coreutils that I have rewritten to have a prefix 'u' for each program
# For instance, the GNU ls will become uls (unix ls), and ls.py will become ls
# There is an uninstall script that moves the programs back from the 'u' prefix to their original names

sudo mv /bin/ls /bin/uls && echo "successfully moved GNU ls to uls"
sudo cp ls.py /bin/ls && echo "successfully moved ls.py to /bin/lsi"
