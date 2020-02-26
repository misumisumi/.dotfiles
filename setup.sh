#/bin/bash
DOT_FILES=(.bash_profile .bashrc .gtkrc-2.0 .xinitrc .xprofile .xsessionrc .xmonad/xmonad.hs)
DOT_DIRS=(.config/alacritty .config/gtk-3.0 .config/polybar .config/rofi)

for file in ${DOT_FILES[@]}
do
    ln -s $HOME/dotfiles/$file $HOME/$file
done

for dir in ${DOT_DIRS[@]}
do
    ln -s $HOME/dotfiles/$dir $HOME/$dir
done