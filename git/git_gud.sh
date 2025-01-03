#!/bin/bash

# Run ssh-agent and add key. Kill ssh agent if it was previously running
# (I'm sure killing the agent is never going to bite me in the ass in the future...)
SSH_AGENT_PID=$(pidof ssh-agent) ssh-agent -k
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/ed25519

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
