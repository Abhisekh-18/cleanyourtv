#!/usr/bin/env bash
# Restore script for Hisense SmartTV 4K FFM
set -euo pipefail
cd "$(dirname "$0")"
TV_HOST="${TV_HOST:-192.168.1.10}"
echo "Restoring TV at $TV_HOST..."

# Re-enable all packages disabled during debloat
export TV_HOST
tools/restore.sh work/debloat.txt com.google.android.apps.tv.launcherx

# Revert Private DNS if modified
tools/venv/bin/python tools/tv.py "settings put global private_dns_mode opportunistic"

echo "TV restored successfully."
