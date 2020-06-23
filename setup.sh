#/bin/bash
DOTPATH=$HOME/.dotfiles
for f in .??*
do
    [ "$f" = ".git" ] && continue
    [ "$f" = ".zplug" ] && continue
    [ "$f" = ".config" ] && continue
    ln -snfv "$DOTPATH/$f" "$HOME/$f"
    # echo "$DOTPATH/$f"
    # echo "$HOME/$f"
done

for f in $(ls $DOTPATH/.config)
do
    ln -snfv "$DOTPATH/.config/$f" "$HOME/.config/$f"
    # echo "$DOTPATH/.config/$f"
    # echo "$HOME/.conifg/$f"
done
