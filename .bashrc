#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

export EDITOR=nvim
 recovery-pacman() {
    sudo pacman "$@"  \
    --log /dev/null   \
    --noscriptlet     \
    --dbonly          \
    --overwrite "*"   \
    --nodeps          \
    --needed
}

