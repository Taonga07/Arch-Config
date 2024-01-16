#!/bin/bash


# copy files over

# add custom package repo 

## detect wether to install from local repo or github

# install packages

while IFS= read -r package; do
	sudo pacman -S --no-confirm "$package"
done < packages.txt


#plymouth setup

rm -r -f .config && ln -s /home/thomas/Documents/dotfiles/Setup/Config ~/.config

ln -s Dotfiles/Local/wallpapers ~/.local/walpapers

