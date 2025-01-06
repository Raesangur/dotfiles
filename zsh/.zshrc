# Clear screen
clear

# Path to your oh-my-zsh installation.
export ZSH=~/.oh-my-zsh
#ZSH_THEME="agnoster"
source ~/dotfiles/zsh/prompt

# Disable % eof
unsetopt prompt_cr prompt_sp

# Date format
HIST_STAMPS="yyyy-mm-dd"

# zsh plugins
plugins=(
	zsh-syntax-highlighting
)

# Apply zsh config
source $ZSH/oh-my-zsh.sh


# User configuration
PATH=${PATH}:~/.local/bin

export PATH=/usr/lib/ccache:$PATH

export DISPLAY=:0

PATH=${PATH}:~/.local/bin:~/scripts
PATH=${PATH}:~/.cargo/bin
export PATH


# Make history longer
export HISTFILE="$HOME/.zsh_history"
export HISTSIZE=1000000000
export SAVEHIST=1000000000
setopt EXTENDED_HISTORY


# Set Software Aliases
source ~/dotfiles/zsh/alias.sh

# Setup ctrl+backspace & ctrl+delete to work in terminal
bindkey '^H' backward-kill-word
bindkey '5~' kill-word

# Adding function pathadd to add a folder to path if it doesn't already exists
# https://superuser.com/a/39995
pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

# Start hyprland on startup
if uwsm check may-start; then
	exec systemd-cat -t uwsm_start uwsm start default
fi

# Display welcome message on shell startup
~/dotfiles/zsh/welcome.sh
#source ~/dotfiles/zsh/updates
