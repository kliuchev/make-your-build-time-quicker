#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <slot-number> <existing-branch>" >&2
    exit 2
fi
case "$1" in
    *[!0-9]*|'') echo "Slot must be a positive number" >&2; exit 2 ;;
esac
if [ "$1" -lt 1 ]; then
    echo "Slot must be a positive number" >&2
    exit 2
fi

root=$(git rev-parse --show-toplevel)
branch=$2
if ! git -C "$root" show-ref --verify --quiet "refs/heads/$branch"; then
    echo "Branch does not exist locally: $branch" >&2
    exit 2
fi
slots="$(dirname "$root")/$(basename "$root")-worktrees"
slot="$slots/slot-$1"
mkdir -p "$slots"
if [ -d "$slot" ]; then
    git -C "$slot" switch "$branch"
else
    git -C "$root" worktree add "$slot" "$branch"
fi
echo "$slot"
