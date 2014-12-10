set nocompatible
filetype off

set rtp+=~/.vim/bundle/vundle
call vundle#rc()

"let Vundle manage Vundle
"required!
Bundle 'gmarik/vundle'
Bundle 'bling/vim-airline'
Bundle 'scrooloose/nerdtree'
Bundle 'nvie/vim-flake8'
Bundle 'Valloric/YouCompleteMe'

"The bundles you install list
"airline configure
set laststatus=2
set noshowmode
let g:airline_powerline_fonts=1
let g:airline_theme='powerlineish'
let g:airline_enable_syntastic=1

"nerdtree configure
map <F2> :NERDTreeToggle<CR>

filetype plugin indent on
"rest config here
augroup vimrc_autocmds
	autocmd!
	autocmd FileType python highlight Excess ctermbg=DarkGrey guibg=Black
	autocmd FileType python match Excess /\%81v.*/
	autocmd FileType python set nowrap
augroup END

set history=50
set ruler
set nu
set tabstop=4
set shiftwidth=4
set autoindent
set nobackup
set noswapfile

map <c-j> <c-w>j
map <c-k> <c-w>k
map <c-l> <c-w>l
map <c-h> <c-w>h
