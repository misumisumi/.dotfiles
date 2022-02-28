
set termguicolors

" vi互換動作を無効(ほぼおまじない、neovimだとコマンド無い)
if &compatible
  set nocompatible
  filetype plugin on
  runtime macros/matchit.vim
endif

"クリップボードへのヤンク
if has("clipboard")
  set clipboard=unnamed
endif

set helplang=ja,en "helpの日本語表示
filetype plugin indent on
syntax enable
" コードコピー時にインデントするしないのトグル(neovimだとデフォでしない設定になってる?)
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
set wildmode=full "exコマンドの補完キー操作をzshライクにする
set splitbelow "下側にsplit
set splitright "右側にsplit
set smartcase
"文字コードの自動判別
set encoding=utf-8
set fileencodings=iso-2022-jp,euc-jp,sjis,utf-8
" 全角文字は2文字使う
set ambiwidth=double
set incsearch
"改行コードの自動判別
set fileformats=unix,dos,mac
set mouse=a
set list "制御文字の表示


"Fern
let g:fern#default_hidden=1
