#! /usr/bin/env bash
#
echo [$(pacmd list-sinks | grep -A 15 '* index' | awk '/volume: front/ {print $5}')]
