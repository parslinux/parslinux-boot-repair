#!/usr/bin/env bash
# ==============================================================================
# Pars Linux Boot Repair — Stop Script
# ==============================================================================
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Stopping Pars Linux Boot Repair processes..."

PIDS=$(pgrep -f "parslinux-boot-repair|pardus-boot-repair|Main.py" || true)

if [ -n "$PIDS" ]; then
    echo -e "${RED}Killing processes: $PIDS${NC}"
    kill -TERM $PIDS 2>/dev/null || true
    sleep 1
    # Force kill if still lingering
    kill -KILL $PIDS 2>/dev/null || true
    echo -e "${GREEN}All instances terminated.${NC}"
else
    echo "No running instances found."
fi
