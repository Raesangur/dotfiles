#!/bin/bash

# Run ssh-agent and add key. Kill ssh agent if it was previously running
# (I'm sure killing the agent is never going to bite me in the ass in the future...)
SSH_AGENT_PID=$(pidof ssh-agent) ssh-agent -k
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/ed25519

# Get repo URL (needs to end with `.git`)
if [ $# -eq 0 ] ; then
    echo "Enter the git repository:"
    read gitRepo
else
    gitRepo=$1
fi

# Get destination
if [ ! $2 ] ; then
    echo "Enter destination path:"
    read destPath
#    destPath=$(readlink -m ${destPath})
else
    destPath=$2
fi

# Extract and reconstitute the ssh-formatted URI from the inputted string
# Important: the inputted URI needs the end with `.git`

# Check if already formatted as ssh
if [[ ! "$gitRepo" =~ [a-zA-Z0-9_\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\:[a-zA-Z0-9_\-]+\/[a-zA-Z0-9_\-]+.git$ ]] ; then
    # Check if formatted with https://
    if [[ "$gitRepo" =~ .*[\/\.]([a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+)\/([a-zA-Z0-9_\-]+\/[a-zA-Z0-9_\-]+.git$) ]] ; then
        gitRepo="git@${BASH_REMATCH[1]}:${BASH_REMATCH[2]}"
    else
        # Check if simply a name/repo.git, in which case, default to `github`
        if [[ "$gitRepo" =~ ([a-zA-Z0-9_\-]+\/[a-zA-Z0-9_\-]+.git$) ]] ; then
            gitRepo="git@github.com:${BASH_REMATCH[1]}"
        else
            echo "Not a proper git repository (dont forget the .git at the end)"
            exit 0
        fi
    fi
fi

# Clone the repository recursively
git clone $gitRepo ${destPath} --recurse-submodules
