#!/bin/bash

# Run ssh-agent and add key if it isn't already running
ssh_pid=$(pidof ssh-agent)

if [ "$ssh_pid" = "" ]; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/ed25519
else
    SSH_AGENT_PID=$(ssh_pid) ssh-agent -k
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/ed25519
fi

# Add all files
git add -A

# Get commit message
if [ $# -eq 0 ] ; then
    echo 'Enter the commit message:'
    read commitMessage
else
    commitMessage=$1
fi

# Commit and sign
git commit -S -m "$commitMessage"

# Push to server
git push

#read
