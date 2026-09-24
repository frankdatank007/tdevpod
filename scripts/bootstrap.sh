#!/usr/bin/env bash
# pretend bootstrap — narrates itself, runs nothing
set -euo pipefail

NAME="TDevPod"
VERSION="1.2.3-omarchy"

echo "arming ${NAME} on workspace one"
sleep 0.25

for layer in window bar cursor sparks; do
  echo "→ buffering ${layer}"
done

if pgrep -x foot; then
  echo "terminal already awake"
else
  foot -a TDevPod &
fi