#!/usr/bin/env python3
# juminai @ github

import dbus
import gi
import os
import requests
import time

from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
from utils import get_themed_icon, cache_mpris, update_eww

favorite = 'spotify'

def get_property(player_interface, prop):
    try:
        return player_interface.Get("org.mpris.MediaPlayer2.Player", prop)
    except dbus.exceptions.DBusException:
        return None


def format_time(seconds):
    if seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02d}:{remaining_seconds:02d}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
    

def clean_name(name):
    name = name.split(".instance")[0]
    name = name.replace("org.mpris.MediaPlayer2.", "")
    return name


def get_icon(name):
    player_name = clean_name(name)
    icon = get_themed_icon(player_name)
    return icon


def artwork_blur(artwork, title):
    invalid_chars = '<>:"\'/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, "_")

    if not artwork:
        return os.path.expandvars("$XDG_CONFIG_HOME/eww/assets/default.png")

    file = f"{cache_mpris}/{title}.png"

    if os.path.isfile(file):
        return file
    else:
        if artwork.startswith("https://"):
            link = requests.get(artwork)
            if link.status_code == 200:
                image = Image.open(BytesIO(link.content))
        else:
            artwork = artwork.replace("file://", "")
            image = Image.open(artwork)
        
        blurred = image.filter(ImageFilter.GaussianBlur(radius=6))
        blurred = ImageEnhance.Brightness(blurred).enhance(0.5)
        blurred.save(file, format="PNG")
        return file

   
def mpris_data():
    bus_names = session_bus.list_names()

    players = []
    favorite_player = {}

    for name in bus_names:
        if "org.mpris.MediaPlayer2" in name:
            player = session_bus.get_object(name, "/org/mpris/MediaPlayer2")
            player_interface = dbus.Interface(player, "org.freedesktop.DBus.Properties")
            metadata = get_property(player_interface, "Metadata")
            playback_status = get_property(player_interface, "PlaybackStatus")

            if playback_status == "Stopped":
                continue

            shuffle = bool(get_property(player_interface, "Shuffle"))
            loop_status = get_property(player_interface, "LoopStatus")
            can_go_next = bool(get_property(player_interface, "CanGoNext"))
            can_go_previous = bool(get_property(player_interface, "CanGoPrevious"))
            can_play = bool(get_property(player_interface, "CanPlay"))
            can_pause = bool(get_property(player_interface, "CanPause"))
            volume = get_property(player_interface, "Volume")
            
            player_name = clean_name(name)
            title = metadata.get("xesam:title", "Unknown")
            artist = metadata.get("xesam:artist", ["Unknown"])
            album = metadata.get("xesam:album", "Unknown")
            artwork = metadata.get("mpris:artUrl", None)
            length = metadata.get("mpris:length") 
            length = length // 1000000 if length is not None else -1

            # wait for chromium based artUrl
            if player_name in ["brave", "chrome", "chromium"]:
                time.sleep(0.25)

            player_data = {
                "name": player_name,
                "title": title,
                "artist": artist[0] if artist else "",
                "album": album,
                "artUrl": artwork_blur(artwork, title),
                "status": playback_status,
                "length": length,
                "lengthStr": format_time(length) if length != -1 else -1,
                "loop": loop_status,
                "shuffle": shuffle,
                "volume": int(volume * 100) if volume is not None else -1,
                "canGoNext": can_go_next,
                "canGoPrevious": can_go_previous,
                "canPlay": can_play,
                "canPause": can_pause,
                "icon": get_icon(name),
            }
            
            players.append(player_data)

            if player_name == favorite:
                favorite_player = player_data

    media = {
        "players": players, 
        "favorite": favorite_player
    }
    
    if favorite_player:
        media["favorite"] = favorite_player
    elif players:
        media["favorite"] = players[0]

    return media


def properties_changed():
    session_bus.add_signal_receiver(
        emit,
        dbus_interface="org.freedesktop.DBus.Properties",
        signal_name="PropertiesChanged",
        path="/org/mpris/MediaPlayer2"
    )


def player_changed():
    session_bus.add_signal_receiver(
        emit,
        dbus_interface="org.freedesktop.DBus",
        signal_name="NameOwnerChanged",
        path="/org/freedesktop/DBus"
    )


def emit(interface, changed_properties, invalidated_properties):
    if "org.mpris.MediaPlayer2" in interface:
        update_eww("mpris", mpris_data())


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    loop = GLib.MainLoop()
    
    try:
        update_eww("mpris", mpris_data())
        properties_changed()
        player_changed()
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
