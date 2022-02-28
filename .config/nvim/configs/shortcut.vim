" カスタムショートカット
"リーダーをspaceに
let mapleader = "\<Space>"
" when normal mode
nnoremap <C-n> :Fern . -reveal=% -drawer -toggle<CR>
nnoremap <silent> <C-l> :<C-u>nohlsearch<CR><C-l>
nnoremap <Leader>s :source "~/.config/nvim/init.vim"<CR>
nnoremap <Leader><Enter> :Term<CR>
" For fzf.vim
nnoremap <Leader>a :<C-u>Ag<CR>
nnoremap <Leader>f :<C-u>Files<CR>
nnoremap <Leader>b :<C-u>Buffers<CR>
nnoremap <Leader>h :<C-u>History<CR>
" when insert mode
inoremap <silent> jj <ESC>    
" when terminal
" Terminal起動時ESC or jjでcmd modeに戻れるようにする
tnoremap <silent> <Esc> <C-\><C-n>
tnoremap <silent> jj <C-\><C-n>
