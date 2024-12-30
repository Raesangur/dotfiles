#!/bin/bash
if command -v fastfetch &> /dev/null ; then
        width=$(tput cols)
        height=$(tput lines)
        if (($width > 60)) && (($height > 25)) ; then
        	echo ""
        	fastfetch --config ~/.config/fastfetch/config.jsonc
        elif (($height > 15)); then
        	fastfetch --config ~/.config/fastfetch/config-small.jsonc
       	fi;
fi;
