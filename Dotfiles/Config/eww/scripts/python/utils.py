# juminai @ github

import json
import os
import gi
import subprocess
import sys

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

cache = os.path.expandvars("$XDG_CACHE_HOME/eww")
cache_apps = os.path.join(cache, "apps")
cache_notifications = os.path.join(cache, "notifications")
cache_mpris = os.path.join(cache, "mpris")
apps_file = os.path.join(cache_apps, "apps.json")
dock_file = os.path.join(cache_apps, "dock.json")
frequency_file = os.path.join(cache_apps, "frequency.json")
notifications_file = os.path.join(cache_notifications, "notifications.json")

for file in [cache, cache_apps, cache_notifications, cache_mpris]:
    os.makedirs(file, exist_ok=True)

def get_themed_icon(icon_name):
    theme = Gtk.IconTheme.get_default()

    if "Screenshot" in icon_name:
        icon_name = "com.github.maoschanz.DynamicWallpaperEditor"

    if "Color Picker" in icon_name:
        icon_name = "gcolor3"

    if "Kotatogram" in icon_name:
        icon_name = "Kotatogram"

    if "Telegram Desktop" in icon_name:
        icon_name = "Telegram"

    icon_name = [icon_name, icon_name.lower(), icon_name.capitalize()]

    for name in icon_name:
        icon = theme.lookup_icon(name, 128, 0)
        if icon:
            return icon.get_filename()
    return None


def get_file(name):
    if name == "apps":
        file = apps_file

    if name == "dock":
        file = dock_file

    if name == "notifications":
        file = notifications_file
    
    if name == "frequency":
        file = frequency_file

    return file


def load(file):

    file = get_file(file)

    try:
        with open(file, "r") as log:
            return json.load(log)
    except (FileNotFoundError, json.JSONDecodeError):

        if file == notifications_file:
            return {
                "dnd": False, 
                "notifications": [],
                "popups": []
            }

        if file == frequency_file:
            return {}

        if file in [dock_file, apps_file]:
            return []


def update_eww(var, content):
    subprocess.run([
        "eww", "update", f"{var}={json.dumps(content)}"
    ])


def write_file(file, content):
    file = get_file(file)

    with open(file, "w") as log:
        json.dump(content, log, indent=2)


def generate(content):
    sys.stdout.write(json.dumps(content) + "\n")
    sys.stdout.flush()