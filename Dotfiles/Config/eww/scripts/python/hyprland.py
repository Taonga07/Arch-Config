#!/usr/bin/env python3
# juminai @ github

import json
import os
import subprocess

from utils import load, update_eww, generate

SIGNATURE = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")

apps = load("apps")


def run_command(command):
    result = subprocess.check_output(command, text=True)
    return json.loads(result)


def fix_name(app_name):
    app_name = app_name.lower()
    if "kotatogram" in app_name:
        app_name = "kotatogram"

    if "telegram" in app_name:
        app_name = "telegram"

    if "thunar" in app_name:
        app_name = "thunar"

    if "foot" in app_name:
        app_name = "foot"

    if "code" in app_name:
        app_name = "code"

    if "brave" in app_name:
        app_name = "brave"

    if "transmission" in app_name:
        app_name = "transmission"

    if "pavucontrol" in app_name:
        app_name = "pulse"

    return app_name


def get_workspaces():
    clients = run_command(["hyprctl", "clients", "-j"])
    data = {i: [] for i in range(1, 7)}

    for client in clients:
        workspace_id = client["workspace"]["id"]
        mapped = client["mapped"]
        window_class = client["class"]

        if window_class == "" or not mapped:
            continue

        app_name = fix_name(window_class)
        app_icon = None
        app_id = None

        for app in apps:
            if app_name.lower() in app["name"].lower():
                app_name = app["name"]
                app_icon = app["icon"]
                app_id = app["id"]
                break

        window = {
            "class": app_name,
            "icon": app_icon,
            "id": app_id,
            "address": client["address"],
            "at": client["at"],
            "size": client["size"]
        }

        data[workspace_id].append(window)

    workspaces = [
        {
            "id": workspace_id,
            "windows": windows
        } for workspace_id, windows in data.items()
    ]

    return workspaces


def get_dock_apps(workspaces):
    dock = load("dock")
    dock_apps = {
        "favorite": [], 
        "impostor": []
    }

    for app in apps:
        if app["id"] in dock:
            dock_apps["favorite"].append(
                {
                    "name": app["name"],
                    "icon": app["icon"],
                    "id": app["id"],
                    "address": None
                }
            )

    for workspace in workspaces:
        if workspace["windows"]:
            for window in workspace["windows"]:
                for app in dock_apps["favorite"]:
                    if app["id"] in window["id"]:
                        app["address"] = window["address"]
                        break   

                if window["id"] not in dock:
                    dock_apps["impostor"].append(
                        {
                            "name": window["class"],
                            "icon": window["icon"],
                            "id": window["id"],
                            "address": window["address"],
                        }
                    )

    return dock_apps


def get_active_client():
    active_window = run_command(["hyprctl", "activewindow", "-j"])
    app_class = None
    app_icon = None
    
    if active_window:
        app_class = fix_name(active_window["class"])
        for app in apps:
            if app_class.lower() in app["name"].lower():
                app_class = app["name"]
                app_icon = app["icon"]
                break

    active_workspace = run_command(["hyprctl", "activeworkspace", "-j"])["id"]
    
    return {
        "id": active_workspace, 
        "class": app_class, 
        "icon": app_icon
    }


def update_dock():
    update_eww("dock", get_dock_apps(get_workspaces()))


def monitor_socat():
    socat = ["socat", "-U", "-", f"UNIX-CONNECT:/tmp/hypr/{SIGNATURE}/.socket2.sock"]
    with subprocess.Popen(socat, stdout=subprocess.PIPE, text=True) as process:
       for line in process.stdout:
            workspaces = get_workspaces()

            if line.startswith(("activewindow>>","closewindow>>")):
                update_eww("dock", get_dock_apps(workspaces))
                update_eww("active", get_active_client())
                generate(workspaces)
            elif line.startswith("movewindow>>"):
                generate(workspaces)


if __name__ == "__main__":
    try:
        workspaces = get_workspaces()
        generate(workspaces)
        update_eww("dock", get_dock_apps(workspaces))
        update_eww("active", get_active_client())
        monitor_socat()
    except KeyboardInterrupt:
        pass