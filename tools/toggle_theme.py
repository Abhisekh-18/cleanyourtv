#!/usr/bin/env python3
"""Interactive and CLI theme switcher for CleanYourTV on Hisense SmartTV 4K FFM.
Supports: glass, aurora, nature-calm, scenes, sweden, default.
Preserves user's 5-slot dock layout and captures a verification screenshot.
"""

import json
import os
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.join(REPO_ROOT, "work")
STATE_FILE = os.path.join(WORK_DIR, "current_theme.txt")
STAGED_THEME_DIR = os.path.join(WORK_DIR, "theme-staged")

THEMES = [
    {
        "id": "glass",
        "name": "Glass",
        "desc": "Cinematic shelf, frosted glass dock, soft teal/violet light & horizon glow"
    },
    {
        "id": "aurora",
        "name": "Aurora",
        "desc": "Dark teal & violet aurora wallpaper with navy backdrop"
    },
    {
        "id": "nature-calm",
        "name": "Nature Calm",
        "desc": "12 calming Wikimedia nature scenes rotating every 5 minutes"
    },
    {
        "id": "scenes",
        "name": "Scenes",
        "desc": "14 dark illustrated landscape wallpapers rotating every hour"
    },
    {
        "id": "sweden",
        "name": "Sweden",
        "desc": "3 Swedish landscapes (Abisko aurora, Vasabron, Skeppsbron) rotating hourly"
    },
    {
        "id": "default",
        "name": "Default (Apple TV)",
        "desc": "Pitch black backdrop, Apple TV 4K dock band, and clean minimalist layout"
    }
]

CUSTOM_DOCK_APPS = [
    "com.google.android.youtube.tv",
    "in.startv.hotstar",
    "com.netflix.ninja",
    "com.apple.atve.androidtv.appletv",
    "org.videolan.vlc",
]
CUSTOM_COLUMNS = 5
CUSTOM_GREETING_NAME = "Abhisekh"


def get_current_theme():
    if os.path.isfile(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return f.read().strip()
        except OSError:
            pass
    return "glass"


def set_current_theme(name):
    os.makedirs(WORK_DIR, exist_ok=True)
    try:
        with open(STATE_FILE, "w") as f:
            f.write(name + "\n")
    except OSError:
        pass


def apply_theme(theme_id, tv_host="192.168.1.10"):
    print(f"\nApplying theme: '{theme_id}' to TV at {tv_host}...")
    theme_script = os.path.join(REPO_ROOT, "tools", "theme.sh")
    env = os.environ.copy()
    env["TV_HOST"] = tv_host

    if theme_id in ("reset", "--reset"):
        # Reset to built-in config.xml
        res = subprocess.run([theme_script, "--reset"], cwd=REPO_ROOT, env=env)
        if res.returncode != 0:
            print(f"Error resetting theme (exit code {res.returncode})", file=sys.stderr)
            return False
        set_current_theme("default")
        theme_id = "default"
    else:
        # Clean and prepare staged directory
        if os.path.exists(STAGED_THEME_DIR):
            shutil.rmtree(STAGED_THEME_DIR)
        os.makedirs(STAGED_THEME_DIR, exist_ok=True)

        if theme_id == "default":
            # Apple TV Minimalist Default with custom dock apps and greeting name
            cfg = {
                "dock_apps": CUSTOM_DOCK_APPS,
                "columns": CUSTOM_COLUMNS,
                "fill_dock": True,
                "greeting_name": CUSTOM_GREETING_NAME,
                "wallpaper": False,
                "dock_glass": False,
                "ambient_glow": True,
                "app_glow": False,
                "background_color": "#000000"
            }
        else:
            src_theme_dir = os.path.join(REPO_ROOT, "themes", theme_id)
            if not os.path.isdir(src_theme_dir):
                print(f"Error: Theme '{theme_id}' not found in {src_theme_dir}", file=sys.stderr)
                return False

            # Read config.json
            cfg_path = os.path.join(src_theme_dir, "config.json")
            cfg = {}
            if os.path.isfile(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)

            # Overlay user's custom 5-slot dock apps, columns, and personalized greeting name
            cfg["dock_apps"] = CUSTOM_DOCK_APPS
            cfg["columns"] = CUSTOM_COLUMNS
            cfg["fill_dock"] = True
            cfg["greeting_name"] = CUSTOM_GREETING_NAME

            # Copy single wallpaper if present
            wp = os.path.join(src_theme_dir, "wallpaper.jpg")
            if os.path.isfile(wp):
                shutil.copy2(wp, os.path.join(STAGED_THEME_DIR, "wallpaper.jpg"))

            # Copy wallpapers folder if present
            wp_dir = os.path.join(src_theme_dir, "wallpapers")
            if os.path.isdir(wp_dir):
                shutil.copytree(wp_dir, os.path.join(STAGED_THEME_DIR, "wallpapers"))

        with open(os.path.join(STAGED_THEME_DIR, "config.json"), "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

        # Run theme.sh with staged directory
        res = subprocess.run([theme_script, STAGED_THEME_DIR], cwd=REPO_ROOT, env=env)
        if res.returncode != 0:
            print(f"Error pushing theme (exit code {res.returncode})", file=sys.stderr)
            return False
        set_current_theme(theme_id)

    # Capture a verification screenshot
    import time
    time.sleep(1.5)
    shot_path = os.path.join(REPO_ROOT, "shots", f"theme-{theme_id}.png")
    tv_script = os.path.join(REPO_ROOT, "tools", "tv.py")
    py = os.path.join(REPO_ROOT, "tools", "venv", "bin", "python")
    if not os.path.isfile(py):
        py = sys.executable

    print("Capturing verification screenshot...")
    subprocess.run([py, tv_script, "--screenshot", shot_path], cwd=REPO_ROOT, env=env)
    print(f"Theme '{theme_id}' successfully applied!")
    print(f"Screenshot saved to: {shot_path}")
    return True


def toggle_next(tv_host="192.168.1.10"):
    current = get_current_theme()
    order = ["default", "glass", "aurora", "nature-calm", "scenes", "sweden"]
    try:
        idx = order.index(current)
        next_idx = (idx + 1) % len(order)
    except ValueError:
        next_idx = 0
    next_theme = order[next_idx]
    print(f"Toggling from '{current}' -> '{next_theme}'")
    return apply_theme(next_theme, tv_host)


def interactive_menu(tv_host="192.168.1.10"):
    current = get_current_theme()
    print("=" * 60)
    print("   CleanYourTV - Theme Switcher for Hisense SmartTV 4K FFM")
    print(f"   Connected TV Host: {tv_host} | Current Theme: [{current}]")
    print("=" * 60)
    for i, t in enumerate(THEMES, 1):
        mark = "*" if t["id"] == current else " "
        print(f"  [{i}] {t['name']:<20} {mark} - {t['desc']}")
    print("  [7] Toggle to Next Theme")
    print("  [0] Exit")
    print("-" * 60)

    try:
        choice = input("Select an option (0-7): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return

    if choice == "0" or not choice:
        print("Done.")
        return
    elif choice == "7":
        toggle_next(tv_host)
    else:
        try:
            num = int(choice)
            if 1 <= num <= len(THEMES):
                apply_theme(THEMES[num - 1]["id"], tv_host)
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid input.")


def main():
    tv_host = os.environ.get("TV_HOST", "192.168.1.10")
    if len(sys.argv) == 1:
        interactive_menu(tv_host)
    else:
        arg = sys.argv[1].lower().strip()
        if arg in ("toggle", "next", "--toggle", "--next"):
            toggle_next(tv_host)
        elif arg in ("list", "--list"):
            for t in THEMES:
                print(f"{t['id']:<15} {t['desc']}")
        else:
            match = next((t["id"] for t in THEMES if t["id"] == arg), None)
            if match or arg in ("reset", "default"):
                apply_theme(match or "default", tv_host)
            else:
                print(f"Unknown theme '{arg}'. Available: " + ", ".join(t["id"] for t in THEMES))
                sys.exit(1)


if __name__ == "__main__":
    main()
