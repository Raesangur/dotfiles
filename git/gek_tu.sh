#!/bin/bash

# Get destination
if [ ! $1 ] ; then
    echo "Enter repository name:"
    read destPath
    destPath=ssh://git@git.raesangur.internal:2221/raesangur/${destPath}.git
else
    destPath=ssh://git@git.raesangur.internal:2221/raesangur/$1.git
fi

git remote add raesangur $destPath
