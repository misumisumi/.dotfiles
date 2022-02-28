
set termguicolors

" vi$B8_49F0:n$rL58z(B($B$[$\$*$^$8$J$$!"(Bneovim$B$@$H%3%^%s%IL5$$(B)
if &compatible
  set nocompatible
  filetype plugin on
  runtime macros/matchit.vim
endif

"$B%/%j%C%W%\!<%I$X$N%d%s%/(B
if has("clipboard")
  set clipboard=unnamed
endif

set helplang=ja,en "help$B$NF|K\8lI=<((B
filetype plugin indent on
syntax enable
" $B%3!<%I%3%T!<;~$K%$%s%G%s%H$9$k$7$J$$$N%H%0%k(B(neovim$B$@$H%G%U%)$G$7$J$$@_Dj$K$J$C$F$k(B?)
set pastetoggle=<f5>;
set cmdheight=2
set hidden
set number
set clipboard+=unnamedplus
set title
set smartindent
set expandtab
set tabstop=4
set shiftwidth=4
set nrformats=
set splitright
set history=200
set wildmenu
set wildmode=full "ex$B%3%^%s%I$NJd40%-!<A`:n$r(Bzsh$B%i%$%/$K$9$k(B
set splitbelow "$B2<B&$K(Bsplit
set splitright "$B1&B&$K(Bsplit
set smartcase
"$BJ8;z%3!<%I$N<+F0H=JL(B
set encoding=utf-8
set fileencodings=iso-2022-jp,euc-jp,sjis,utf-8
" $BA43QJ8;z$O(B2$BJ8;z;H$&(B
set ambiwidth=double
set incsearch
"$B2~9T%3!<%I$N<+F0H=JL(B
set fileformats=unix,dos,mac
set mouse=a
set list "$B@)8fJ8;z$NI=<((B


"Fern
let g:fern#default_hidden=1
