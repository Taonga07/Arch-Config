# Arch Config
This repository contains dotfiles for ... It allso hosts a local arch user repsoistory

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


https://github.com/taylor85345/hyprland-dotfiles

|Distro|[Arch](https://archlinux.org/)|
|:---:|:---:|
|Window Manager|[Hyprland](https://hyprland.org/)|
|Widgets|[ElKowars wacky widgets ](https://github.com/elkowar/eww)|
|File Manager|[Thunar](https://archlinux.org/packages/extra/x86_64/thunar/)|
|Shell|[Zsh](https://archlinux.org/packages/extra/x86_64/zsh/)|
|Teminal Multiplexer|[Tmux}(https://github.com/tmux/tmux)|


pulseaudio pipewire wirelumber xwaylandvideobridge hyprland xdg-desktop-portal xdg-desktop-portal-gtk thunar flatpak

## Shortcuts

```

```

## Widgets




## Instalation

The script creates a fresh installation 

```
```

## updates

updates are run using pacman hooks so just update nomaly and he dotfiles will too

##### notes


https://github.com/anufrievroman/waypaper


Windows can be pinned (if floating)
can float and maximize and fullscreen

## EWW wigets

desktop files / computer stats 

get current workspace id 
```
hyprctl activeworkspace -j | jq '.id
```

switch workspace to id
```
hyprctl workspace $id
```

- transperent windows
-	blur for visiblity
- no x11
- right click on desktop
- google drive intergration
- show files on desktop
- auto-open thunar desktop folder when no apps on workspace
- eww settings for wifi, bluetoof, sound, wallpaper, flapaks, updates, transparency, keyboard brightness, screen brightness

```

kitty wofi -G -n --show drun &

# make command run quicker
# do not start by splitting app
# detect wether app active (mouse over) if not then exit
# make it start in the top left hand corner

```

(deflisten workspace "scripts/workspace")

workspace widget allows renaming of workspaces

no wolfi but eww equivilent

```
chsh -s $(which zsh)
```



packages

pipewire - sound
wireplumber - scrensharing
dunst - dotification daemon

#

make home-folder readonly but the the folder within read and write so no more files are added

```
chmod 500 /home/$user
```

.cache, .config, .local, .var, Documents, Downloads, Music, Pictures

add zsh directory for .cache and .config

## zshrc 


# Lines configured by zsh-newuser-install
HISTFILE=~/.cache/zsh/histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/thomas/.zshrc'


autoload -Uz compinit
compinit
# End of lines added by compinstall
