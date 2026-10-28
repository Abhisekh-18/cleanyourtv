# Theme Switching & TV Reconnection Guide

This guide explains how to run the theme switcher locally on your Mac, switch or preview themes on your **Hisense SmartTV 4K FFM**, and reconnect to the TV whenever it is turned off or has debugging disabled.

---

## 1. How to Run Locally on Your Mac

### Step 1: Open Terminal
Press <kbd>Cmd</kbd> + <kbd>Space</kbd>, type **Terminal**, and press <kbd>Enter</kbd>.

### Step 2: Navigate to the Project Directory
Run:
```zsh
cd /Users/abhisekhsahoo/Downloads/DIC/openforge/cleanyourtv
```

### Step 3: Launch the Theme Switcher

#### Option A: Interactive Menu (Recommended)
```zsh
./toggle-theme.sh
```
This opens the interactive menu:
```text
============================================================
   CleanYourTV - Theme Switcher for Hisense SmartTV 4K FFM
   Connected TV Host: 192.168.1.10 | Current Theme: [glass]
============================================================
  [1] Glass                * - Frosted glass dock, soft lighting & horizon glow
  [2] Aurora                 - Dark teal & violet aurora wallpaper with navy backdrop
  [3] Nature Calm            - 12 calming Wikimedia nature scenes rotating every 5 min
  [4] Scenes                 - 14 dark illustrated landscape wallpapers rotating hourly
  [5] Sweden                 - 3 Swedish landscapes (Abisko aurora, etc.) rotating hourly
  [6] Default (Apple TV)     - Pitch black backdrop, Apple TV 4K dock band
  [7] Toggle to Next Theme
  [0] Exit
------------------------------------------------------------
Select an option (0-7): 
```
Type the number (e.g. `2` for Aurora) and press <kbd>Enter</kbd>. The theme will apply immediately and display a confirmation.

#### Option B: Direct Theme Switching
Pass the theme name directly as an argument:
```zsh
./toggle-theme.sh aurora
./toggle-theme.sh glass
./toggle-theme.sh scenes
./toggle-theme.sh nature-calm
./toggle-theme.sh sweden
./toggle-theme.sh default
```

#### Option C: Quick Cycle / Toggle
Cycle sequentially to the next theme in the rotation:
```zsh
./toggle-theme.sh toggle
```

---

## 2. Available Themes

| Theme ID | Name | Description |
|---|---|---|
| `glass` | **Glass** | Frosted glass dock shelf, soft horizon glow matching focused app, translucent pill buttons. |
| `aurora` | **Aurora** | Dark navy backdrop with deep teal and violet polar aurora ribbon. |
| `nature-calm` | **Nature Calm** | 12 high-resolution calming nature landscapes rotating every 5 minutes. |
| `scenes` | **Scenes** | 14 dark illustrated minimal landscape wallpapers rotating every hour. |
| `sweden` | **Sweden** | 3 Nordic landscapes (Abisko aurora borealis, Vasabron, Skeppsbron) rotating hourly. |
| `default` | **Apple TV Default** | Pure pitch black OLED background, Apple TV 4K dock band, and minimal UI. |

*Note: All themes preserve your custom 5-app dock layout (Apple TV, Netflix, YouTube, Prime Video, Disney+ Hotstar) and 5-column grid.*

---

## 3. How to Reconnect After Turning Off the TV

### Scenario A: The TV was in standby or turned off & on
As long as **USB Debugging** is still toggled **ON** in Developer options, ADB will start automatically when the TV boots.

1. **Check the TV's IP address**:
   * On your TV remote, go to: **Settings → Network & Internet → [Your Connected Network]**.
   * Note the **IP address**.
2. **If the IP is unchanged (`192.168.1.10`)**:
   ```zsh
   ./toggle-theme.sh
   ```
3. **If your router assigned a new IP** (e.g. `192.168.1.45`):
   ```zsh
   TV_HOST=192.168.1.45 ./toggle-theme.sh
   ```

> [!TIP]
> **Static IP Reservation:** In your home Wi-Fi/Ethernet router admin panel, assign a fixed DHCP reservation to your Hisense TV so its IP address never changes.

---

### Scenario B: Debugging was turned OFF for security
If you turned off debugging to lock down port 5555:

1. **Turn on USB Debugging on the TV**:
   * On your TV remote, open **Settings → Device Preferences (or System) → Developer options**.
   * *(If Developer Options is hidden: Go to **Settings → About**, scroll down to **Android TV OS build**, and press the OK button on your remote **7 times** until it announces developer mode).*
   * Turn **USB debugging** to **ON**.
2. **Accept the Computer Prompt**:
   * Run your theme command on your Mac.
   * Look at your TV screen. If a prompt appears asking *"Allow USB debugging?"*, check the box for *"Always allow from this computer"* and choose **Allow / OK**.
3. **Switch your theme**:
   ```zsh
   ./toggle-theme.sh
   ```
4. **Lock it back down (Recommended)**:
   * When you are done customizing, toggle **USB debugging** back to **OFF** in Developer Options.
   * Your chosen theme, custom dock, and debloated setup will stay active even with debugging turned off.

---

## 4. Useful Helper Commands

You can run these directly from Terminal in `/Users/abhisekhsahoo/Downloads/DIC/openforge/cleanyourtv`:

* **Pull a live screenshot from the TV to your Mac**:
  ```zsh
  TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py --screenshot shots/current.png
  open shots/current.png
  ```

* **Simulate pressing the remote Home button**:
  ```zsh
  TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py input keyevent 3
  ```

* **Check if ADB port 5555 is closed**:
  ```zsh
  tools/venv/bin/python tools/adb-closed.py 192.168.1.10
  ```

* **Full Factory Restore**:
  ```zsh
  ./restore-this-tv.sh
  ```
