" Set your leader key (change it if you prefer another key)
let mapleader = "\<Space>"

" Plugins
call plug#begin('~/.config/nvim/plugged')

" nvim-tree
Plug 'kyazdani42/nvim-tree.lua'

call plug#end()

" nvim-tree settings
nnoremap <leader>e :NvimTreeToggle<CR>

" Terminal configuration
" Open terminal in a new horizontal split
nnoremap <leader>t :term<CR>
