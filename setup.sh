#/bin/bash
DOTPATH=$HOME/.dotfiles
for f in .??*
do
    [ "$f" = ".git" ] && continue
    [ "$f" = ".config" ] && continue
    [ "$f" = "fonts.conf" ] && continue
    ln -snfv "$DOTPATH/$f" "$HOME/$f"
    # echo "$DOTPATH/$f"
    # echo "$HOME/$f"
done

# ln -snfv "$DOTPATH/.vimrc" "$HOME/.config/nvim/init.vim"

for f in $(ls $DOTPATH/.config)
do
    ln -snfv "$DOTPATH/.config/$f" "$HOME/.config/$f"
    # echo "$DOTPATH/.config/$f"
    # echo "$HOME/.conifg/$f"
done
