" カスタムショートカット
" リーダーをspaceに
let mapleader = "\<Space>"

" when normal mode
nmap <silent> <C-l> :<C-u>nohlsearch<CR><C-l>
nmap <Leader>n :Fern . -reveal=% -drawer -toggle<CR>
nmap <Leader>S :source "~/.config/nvim/init.vim"<CR>
nmap <Leader><Enter> :Term<CR>

nmap <Leader>qq :q<CR>
nmap <Leader>wq :wq<CR>

" For fzf.vim
nmap <Leader>f :<C-u>Files<CR>
nmap <Leader>b :<C-u>Buffers<CR>
nmap <Leader>w :<C-u>Windows<CR>
nmap <Leader>m :<C-u>Marks<CR>
nmap <Leader>h :<C-u>History<CR>
nmap <Leader>a :<C-u>Ag<CR>
nmap <Leader>r :<C-u>Rg<CR>
nmap <Leader>c :<C-u>Command<CR>
nmap <Leader>gf :<C-u>GFiles<CR>
nmap <Leader>map :<C-u>Maps<CR>
nmap <Leader>com :<C-u>Commit<CR>

" when terminal
" Terminal起動時ESC or jjでcmd modeに戻れるようにする
tnoremap <silent> <Esc> <C-\><C-n>
tnoremap <silent> jj <C-\><C-n>

" Airline
nmap <C-p> <Plug>AirlineSelectPrevTab
nmap <C-n> <Plug>AirlineSelectNextTab
