#!/usr/bin/env zsh
set -euo pipefail

ROOT="${0:A:h:h}"
OUTPUT="$(TERM=dumb "$ROOT/scripts/profile-terminal-card.sh")"

[[ "$OUTPUT" == *"juliosuas@fsociety operator % whoami"* ]]
[[ "$OUTPUT" == *$'juliosuas\n'* ]]
[[ "$OUTPUT" == *"cat terminal/05_stack.txt"* ]]
