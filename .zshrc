# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

#
# Executes commands at the start of an interactive session.
#
# Authors:
#   Sorin Ionescu <sorin.ionescu@gmail.com>
#
# Customize to your needs...


autoload -Uz promptinit
promptinit
prompt off
if [ -n "${DOCKER_CONTAINER}" ]; then
  PROMPT="(${DOCKER_CONTAINER})%# "
fi

if [ -n "${DOCKER_CONTAINER}" ]; then
  PROMPT="(${DOCKER_CONTAINER})%# "
fi

# Source Prezto.
if [[ -s "${ZDOTDIR:-$HOME}/.zprezto/init.zsh" ]]; then
  source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"
fi

### Added by Zinit's installer
# if [[ ! -f $HOME/.zinit/bin/zinit.zsh ]]; then
#     print -P "%F{33}▓▒░ %F{220}Installing %F{33}DHARMA%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
#     command mkdir -p "$HOME/.zinit" && command chmod g-rwX "$HOME/.zinit"
#     command git clone https://github.com/zdharma-continuum/zinit "$HOME/.zinit/bin" && \
#         print -P "%F{33}▓▒░ %F{34}Installation successful.%f%b" || \
#         print -P "%F{160}▓▒░ The clone has failed.%f%b"
# fi
# 
# source "$HOME/.zinit/bin/zinit.zsh"
# autoload -Uz _zinit
# (( ${+_comps} )) && _comps[zinit]=_zinit
# 
# # Load a few important annexes, without Turbo
# # (this is currently required for annexes)
# zinit light-mode for \
#     zinit-zsh/z-a-as-monitor \
#     zinit-zsh/z-a-patch-dl \
#     zinit-zsh/z-a-bin-gem-node

if [[ ! -f $HOME/.zi/bin/zi.zsh ]]; then
    sh -c "$(curl -fsSL https://git.io/get-zi)" --
fi

source "$HOME/.zi/bin/zi.zsh"
### End of Zi's installer chunk
# Basic plugin
zi ice wait"0"; zi load zdharma-continuum/history-search-multi-word
zi ice wait"!0"; zi light zsh-users/zsh-autosuggestions
zi ice wait"!0"; zi light zdharma-continuum/fast-syntax-highlighting
zi ice wait"!0"; zi load momo-lab/zsh-abbrev-alias

zi snippet PZT::modules/helper/init.zsh
zi ice depth=1; zi light romkatv/powerlevel10k

zi ice silent; zi snippet PZT::modules/history
zi ice silent; zi snippet PZT::modules/pacman
zi ice silent; zi snippet PZT::modules/environment
zi ice silent; zi snippet PZT::modules/terminal
zi ice silent; zi snippet PZT::modules/editor
zi ice silent; zi snippet PZT::modules/directory
zi ice silent; zi snippet PZT::modules/spectrum
zi ice silent; zi snippet PZT::modules/utility
zi ice silent; zi snippet PZT::modules/completion
# zi snippet PZT::modules/prompt
#zi ice svn pick"init.zsh"
# zi snippet PZT::modules/git

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
### End of Zinit's installer chunk
#set -v

# Connect libvirt root system
alias ls="ls --color=auto"
alias tp="trash-put"
alias tls="trash-list"
alias tre="trash-restore"
alias temp="trash-empty"
alias trm="trash-rm"
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias gpus='NVIDIA_VISIBLE_DEVICE'
alias ssh='kitty +kitten ssh'
alias tty-clock='tty-clock -s -c -C 6'

export LIBVIRT_DEFAULT_URI="qemu:///system"
export FrameworkPathOverride=/lib/mono/4.8-api/
export PYENV_ROOT="$HOME/.pyenv"
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export PATH="$PYENV_ROOT/bin:/opt/Ryzen Controller:$PATH":$HOME/bin
export CHROME_PATH=$(which vivaldi-stable)
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# if [ -n "${SSH_CLIENT}" ]; then
#     export PULSE_SERVER=$SSH_CLIENT
# fi
HISTFILE=~/.zsh_history      # ヒストリファイルを指定
HISTSIZE=10000               # ヒストリに保存するコマンド数
SAVEHIST=10000               # ヒストリファイルに保存するコマンド数
setopt hist_ignore_all_dups  # 重複するコマンド行は古い方を削除
setopt hist_ignore_dups      # 直前と同じコマンドラインはヒストリに追加しない
setopt share_history         # コマンド履歴ファイルを共有する
setopt append_history        # 履歴を追加 (毎回 .zsh_history を作るのではなく)
setopt inc_append_history    # 履歴をインクリメンタルに追加
setopt hist_no_store         # historyコマンドは履歴に登録しない
setopt hist_reduce_blanks    # 余分な空白は詰めて記録
typeset -g POWERLEVEL9k_INSTANT_PROMPT=quiet
