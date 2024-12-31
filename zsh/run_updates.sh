#!/bin/bash

# run apt updates
if command -v apt-get &> /dev/null ; then
	sudo apt-get update
	sudo apt-get upgrade -y
	sudo apt-get dist-upgrade -y
	sudo apt-get autoremove
	sudo apt-get autoclean
fi

if command -v pacman &> /dev/null ; then
	sudo pacman -Syu
fi

if command -v yay &> /dev/null ; then
	yay -Syu
fi

# other updates
if command -v snap &> /dev/null ; then
    sudo snap refresh
fi

if command -v brew &> /dev/null ; then
    brew upgrade
fi

if command -v npm &> /dev/null ; then
    npm update
fi

if command -v pveam &> /dev/null ; then
    pveam update
fi
