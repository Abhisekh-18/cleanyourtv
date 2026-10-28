# Clean Your TV - Hisense SmartTV 4K FFM (songshan)

Setup guide, maintenance instructions, and restoration steps for your debloated Hisense SmartTV 4K FFM running Android 11 (SDK 30).

---

## What Was Done

1. **Full Backups**:
   - Stored in `backup/`: complete package list (`packages.txt`), disabled packages (`disabled.txt`), system properties (`getprop.txt`), and Android settings (`settings-global.txt`, `settings-secure.txt`, `settings-system.txt`).
2. **Debloat Applied**:
   - Disabled store demos (`com.hisense.storemode`, `fusion.android.tv.demo`).
   - Disabled first-time setup stubs & tracking (`com.hisense.fte`, `android.autoinstalls.config.google.gtvpai`, `com.google.android.partnersetup`, `com.google.android.feedback`).
   - Disabled manufacturer stubs & unused tools (`com.mstar.android.tv.disclaimercustomization`, `com.hisense.hibrowser`, `com.vt.eula`, `com.iqqijni.tv1.keyboard`, `com.google.android.play.games`, `com.android.dreams.basic`, `com.google.android.youtube.tvmusic`, `com.google.android.videos`, `com.hisense.udpserver`, `com.vt.tv.mediacenter`).
   - Disabled OTA & remote update daemons (`com.hisense.tv.ota`, `com.hisense.remoteupgrade`, `com.vt.tv.usbota`, `com.vt.audio_update_service`).
   - Disabled Google TV setup wizard (`com.google.android.tungsten.setupwraith`) and stock launcher (`com.google.android.apps.tv.launcherx`).
   - Preserved all user-selected apps: Netflix, Prime Video, Disney+ Hotstar, Apple TV, YouTube, SonyLIV, JioCinema, Airtel Xstream, Zee5, VLC, Kodi, MX Player, FX, Chromecast, Miracast, AirPlay, and Voice Assistants.
   - Preserved all core Android packages, hardware TV input middleware, and MediaTek tuner services.
3. **Ad-blocking Private DNS**:
   - Configured `dns.adguard-dns.com` via Android Private DNS for system-wide ad/tracker blocking.
   - Note: Private DNS does not block YouTube video ads (which are served from the same domain as video streams).
   - Undo: `TV_HOST=192.168.1.10 tools/tv.py "settings put global private_dns_mode opportunistic"`
4. **Apple TV Style Leanback Launcher**:
   - Clean, lightweight native Android TV launcher (`minSdk` 26, zero network permissions, <550 KB APK).
   - Pitch black background with ambient glow matching the focused app.
   - 5-slot bottom dock: **Apple TV**, **Netflix**, **YouTube**, **Prime Video**, and **Disney+ Hotstar**.
   - Responsive frosted pill buttons top-right for Inputs, Wi-Fi, and Settings.
   - Clean thin clock and date top-left.

---

## Quick Reference Scripts

- **Restore everything to factory state**:
  ```bash
  ./restore-this-tv.sh
  ```
- **Rebuild and reinstall the launcher**:
  ```bash
  ./build-and-install-my-tv.sh
  ```
- **Switch or toggle between themes**:
  ```bash
  # Interactive theme menu:
  ./toggle-theme.sh

  # Or switch directly by name:
  ./toggle-theme.sh glass
  ./toggle-theme.sh aurora
  ./toggle-theme.sh nature-calm
  ./toggle-theme.sh scenes
  ./toggle-theme.sh sweden
  ./toggle-theme.sh default

  # Cycle/toggle to the next theme in sequence:
  ./toggle-theme.sh toggle
  ```
  *(See [THEME-GUIDE.md](THEME-GUIDE.md) for full details on switching themes, reconnecting, and running locally).*

---

## How to Re-enable Any App or Service

To re-enable any disabled package individually, run:
```bash
TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py "pm enable --user 0 <package_name>"
```

### Common examples:
- **System OTA Updates**:
  ```bash
  TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py "pm enable --user 0 com.hisense.tv.ota"
  TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py "pm enable --user 0 com.hisense.remoteupgrade"
  ```
- **Google Play Games**:
  ```bash
  TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py "pm enable --user 0 com.google.android.play.games"
  ```
- **Google TV Movies**:
  ```bash
  TV_HOST=192.168.1.10 tools/venv/bin/python tools/tv.py "pm enable --user 0 com.google.android.videos"
  ```

---

## Customizing the Launcher

### Changing Dock Apps or Column Count
1. Open `launcher/app/src/main/res/values/config.xml`.
2. To change the dock apps or their order, edit `<string-array name="dock_apps">`:
   ```xml
   <string-array name="dock_apps">
       <item>com.apple.atve.androidtv.appletv</item>
       <item>com.netflix.ninja</item>
       <item>com.google.android.youtube.tv</item>
       <item>com.amazon.amazonvideo.livingroom</item>
       <item>in.startv.hotstar</item>
   </string-array>
   ```
3. To change the number of columns / dock slots (4, 5, 6, 7):
   ```xml
   <integer name="columns">5</integer>
   ```
4. Rebuild and reinstall:
   ```bash
   ./build-and-install-my-tv.sh
   ```

### Applying Themes & Changing Wallpapers
You can push themes without rebuilding the APK:
```bash
# Push glass theme (frosted glass dock and ambient lighting):
TV_HOST=192.168.1.10 tools/theme.sh themes/glass

# Push aurora theme:
TV_HOST=192.168.1.10 tools/theme.sh themes/aurora

# Push scenes theme:
TV_HOST=192.168.1.10 tools/theme.sh themes/scenes

# Reset to built-in config.xml:
TV_HOST=192.168.1.10 tools/theme.sh --reset
```

---

## Closing ADB (Important Security Step)

Port 5555 is unencrypted plaintext. Leaving network debugging enabled allows any device on your local network to access a shell.

To lock down your TV:
1. On your TV, navigate to **Settings** → **Device Preferences** (or **System**) → **Developer options**.
2. Turn **OFF** **Network debugging** / **Wireless debugging**.
3. Turn **OFF** **USB debugging** (unless you specifically need wired debugging kept on).
4. Select **Revoke USB debugging authorizations** and confirm.
5. Reboot the TV.
6. Verify port 5555 is closed from your computer:
   ```bash
   tools/venv/bin/python tools/adb-closed.py 192.168.1.10
   ```
   The tool should report that port 5555 is closed.
