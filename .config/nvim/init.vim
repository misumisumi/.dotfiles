"Use 24-bit (true-color) mode in Vim/Neovim when outside tmux.
"If you're using tmux version 2.2 or later, you can remove the outermost $TMUX check and use tmux's 24-bit color support
"(see < http://sunaku.github.io/tmux-24bit-color.html#usage > for more information.)

if (empty($TMUX))
  if (has("nvim"))
    "For Neovim 0.1.3 and 0.1.4 < https://github.com/neovim/neovim/pull/2198 >
    let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  endif
endif

set termguicolors
let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum" " 文字色
let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum" " 背景色

if &compatible
  set nocompatible
  filetype plugin on
  runtime macros/matchit.vim
endif

" Add the dein installation directory into runtimepath
set runtimepath+=~/.cache/dein/repos/github.com/Shougo/dein.vim

if dein#load_state('~/.cache/dein')
  call dein#begin('~/.cache/dein')

" プラグインリストを収めた TOML ファイル
  " 予め TOML ファイル（後述）を用意しておく
  let g:rc_dir    = expand('~/.config/nvim')
  let s:toml      = g:rc_dir . '/dein.toml'
  let s:lazy_toml = g:rc_dir . '/dein_lazy.toml'

  call dein#load_toml(s:toml,	   {'lazy':0})
  call dein#load_toml(s:lazy_toml, {'lazy':0})
  call dein#end()
  call dein#save_state()
endif

if dein#check_install()
    call dein#install()
endif

set helplang=ja,en "helpの日本語表示
filetype plugin indent on
syntax enable

autocmd BufRead,BufNewFile *.md  setfiletype markdown
autocmd BufRead,BufNewFile *.ipynb  setfiletype jupyternotebook

inoremap <silent> jj <ESC>    
set pastetoggle=<f5>;
" Terminal起動時ESCでcmd modeに戻れるようにする
tnoremap <silent> <Esc> <C-\><C-n>
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
set fileencodings=iso-2022-jp,euc-jp,sjis,utf-8set incsearch
"改行コードの自動判別
set fileformats=unix,dos,mac
nnoremap <silent> <C-l> :<C-u>nohlsearch<CR><C-l>
cnoremap <C-p> <Up>
cnoremap <C-n> <Down>
"sudo(これは消す)
cnoremap <expr> %% getcmdtype() == ':' ? expand('%:h') . '/' : '%%'
cmap w!! w !sudo tee > /dev/null %
"括弧の補完
inoremap { {}<LEFT>
inoremap [ []<LEFT>
inoremap ( ()<LEFT>
inoremap " ""<LEFT>
inoremap ' ''<LEFT>
