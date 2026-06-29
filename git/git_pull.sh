# Run ssh-agent and add key. Kill ssh agent if it was previously running
# (I'm sure killing the agent is never going to bite me in the ass in the future...)
SSH_AGENT_PID=$(pidof ssh-agent) ssh-agent -k
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/ed25519

git pull
