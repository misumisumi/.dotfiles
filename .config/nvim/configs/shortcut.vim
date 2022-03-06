" カスタムショートカット
" リーダーをspaceに
let mapleader = "\<Space>"

" when normal mode
nmap <silent> <C-l> :<C-u>nohlsearch<CR><C-l>
nmap <Leader>n :Fern . -reveal=% -drawer -toggle<CR>
nmap <Leader>ss :source "~/.config/nvim/init.vim"<CR>
nmap <Leader><Enter> :25Term<CR>
au FileType quickrun,fzf nmap <silent><buffer>q :q<CR>
au FileType fern nmap <silent><buffer>E <Plug>(fern-action-open:vsplit)
imap <silent> jj <C-\><C-n>


nmap <Leader>qq :q<CR>
nmap <Leader>wq :wq<CR>

" For Buffer
nmap <silent> [b :bnext
nmap <silent> ]b :bprevious

" For Tab
nmap <Tab> gt
nmap <S-Tab> gT
nmap <Leader><Tab> :tabnew<CR>


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
nmap <Leader>ch :<C-u>History:<CR>
nmap <Leader>sh :<C-u>History/<CR>
nmap <Leader>map :<C-u>Maps<CR>
nmap <Leader>com :<C-u>Commit<CR>

" For quickrun
let g:quickrun_no_default_key_mappings = 1
au FileType python nmap <Leader>p :write<CR>:QuickRun -mode n<CR>      
au FileType nmap <expr><silent> <C-c> quickrun#is_running() ? quickrun#sweep_sessions() : "\<C-c>"

" For Markdown Preview
au FileType markdown nmap <Leader>p <Plug>MarkdownPreviewToggle

" when terminal
" Terminal起動時ESC or jjでcmd modeに戻れるようにする
tmap <silent> <Esc> <C-\><C-n>
tmap <silent> jj <C-\><C-n>

" Airline
nmap <C-p> <Plug>AirlineSelectPrevTab
nmap <C-n> <Plug>AirlineSelectNextTab

" For fugitive
nmap <Leader>ga :Gwrite<CR>
nmap <Leader>gc :Git commit<CR>
nmap <Leader>gs :Git<CR>
nmap <Leader>gd :Git diff<CR>


" For vim-gitgutter
nmap <Leader>ha <Plug>GitGutterStageHunk
nmap <Leader>hu <Plug>GitGutterRevertHunk
