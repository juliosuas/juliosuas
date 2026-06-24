#!/usr/bin/env zsh
set -euo pipefail

ROOT="${0:A:h:h}"
GREEN=$'\033[0;32m'
RESET=$'\033[0m'

clear
printf '%s' "$GREEN"

printf 'Last login: Sat Jun  6 03:29:18 on ttys007\n'
printf 'juliosuas@fsociety ~ %% cd ~/operator\n'
printf 'juliosuas@fsociety operator %% cat terminal/00_boot.txt\n'
cat "$ROOT/terminal/00_boot.txt"
printf '\n\n'

printf 'juliosuas@fsociety operator %% cat terminal/01_white-rabbit.txt\n'
cat "$ROOT/terminal/01_white-rabbit.txt"
printf '\n\n'

printf 'juliosuas@fsociety operator %% whoami\n'
printf 'juliosuas\n\n'

printf 'juliosuas@fsociety operator %% cat terminal/02_identity.txt\n'
cat "$ROOT/terminal/02_identity.txt"
printf '\n\n'

printf 'juliosuas@fsociety operator %% cat terminal/03_receipts.txt\n'
cat "$ROOT/terminal/03_receipts.txt"
printf '\n\n'

printf 'juliosuas@fsociety operator %% ls ~/src\n'
cat "$ROOT/terminal/04_projects.txt"
printf '\n\n'

printf 'juliosuas@fsociety operator %% cat terminal/05_stack.txt\n'
cat "$ROOT/terminal/05_stack.txt"
printf '\n\n'

printf 'juliosuas@fsociety operator %% '
printf '%s' "$RESET"
