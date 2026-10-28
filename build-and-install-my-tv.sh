#!/usr/bin/env bash
# Build and install script for Hisense SmartTV 4K FFM
set -euo pipefail
cd "$(dirname "$0")"
export TV_HOST="${TV_HOST:-192.168.1.10}"
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home}"
export ANDROID_HOME="${ANDROID_HOME:-/opt/homebrew/share/android-commandlinetools}"
cd launcher && ./build-and-install.sh
