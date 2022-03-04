"Use 24-bit (true-color) mode in Vim/Neovim when outside tmux.
"If you're using tmux version 2.2 or later, you can remove the outermost $TMUX check and use tmux's 24-bit color support
"(see < http://sunaku.github.io/tmux-24bit-color.html#usage > for more information.)
if (empty($TMUX))
  if (has("nvim"))
    "For Neovim 0.1.3 and 0.1.4 < https://github.com/neovim/neovim/pull/2198 >
    let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  endif
  "For Neovim > 0.1.5 and Vim > patch 7.4.1799 < https://github.com/vim/vim/commit/61be73bb0f965a895bfb064ea3e55476ac175162 >
  "Based on Vim patch 7.4.1770 (`guicolors` option) < https://github.com/vim/vim/commit/8a633e3427b47286869aa4b96f2bfc1fe65b25cd >
  " < https://github.com/neovim/neovim/wiki/Following-HEAD#20160511 >
  if (has("termguicolors"))
    set termguicolors
  endif
endif

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
set fileencodings=utf-8,iso-2022-jp,euc-jp,sjis
" $BA43QJ8;z$O(B2$BJ8;z;H$&(B
set ambiwidth=double
set incsearch
"$B2~9T%3!<%I$N<+F0H=JL(B
set fileformats=unix,dos,mac
set mouse=a
set list "$B@)8fJ8;z$NI=<((B
set splitbelow


"Fern
let g:fern#default_hidden=1

"fzf
"let g:fzf_layout={'down': '40%'}
let g:fzf_action={
  \ 'ctrl-t': 'tab split',
  \ 'ctrl-h': 'split',
  \ 'ctrl-v': 'vsplit' }
