# Setup software
if command -v thefuck &> /dev/null ; then
    eval $(thefuck --alias)
fi
if command -v brew &> /dev/null ; then
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
fi
alias bat='bat --color=always'

# Displaying files
if command -v eza &> /dev/null ; then
	alias ls='eza --icons --color=always --group-directories-first'
	alias la='eza --icons --color=always --group-directories-first --long --all --all --header --no-user'
fi

# Removing files
alias rm='echo "rm is disabled on this system, use remove or trash or /bin/rm instead."'
alias remove='trash -ir'

# Setup utilities
alias my_ip="neofetch public_ip; neofetch local_ip"
alias restart="sudo reboot"
alias fucking=sudo
alias please=sudo
alias did_i_fucking_stutter='sudo $(fc -ln -1)'
alias show=tycat

# Setup small programs
alias git_gud="~/dotfiles/git/git_gud.sh"
alias git_clone="~/dotfiles/git/git_clone.sh"
alias git_pull="~/dotfiles/git/git_pull.sh"

alias bon_matin="source ~/.zshrc"
alias update="~/dotfiles/zsh/run_updates.sh"

