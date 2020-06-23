#/bin/bash
DOTPATH=$HOME/dotfiles
for f in .??*
do
    [ "$f" = ".git" ] && continue
    echo $f
    # ln -snfv "$DOTPATH/$f" "$HOME"/"$f"
done