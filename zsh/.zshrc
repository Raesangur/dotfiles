# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

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
# plugins softwares
docker
git
mvn
node
npm
python


# plugins tools
emoji
web-search

# plugins misc
sudo
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

# Set Software Aliases
source ~/dotfiles/zsh/alias

# Setup ctrl+backspace & ctrl+delete to work in terminal
#bindkey '^H' backward-kill-word
#bindkey '5~' kill-word

# Adding function pathadd to add a folder to path if it doesn't already exists
# https://superuser.com/a/39995
pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

# Display welcome message on shell startup
#~/scripts/welcome.sh
fastfetch
#source ~/dotfiles/zsh/welcome
#source ~/dotfiles/zsh/updates
