#!/bin/bash
set -o pipefail -o noclobber -o nounset

! getopt --test >/dev/null
if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
    echo "getopt failed."
    exit 1
fi

OPTIONS=a
LONGOPTIONS=all

! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    exit 2
fi

eval set -- "$PARSED"

ALL=n

while true; do
    case "$1" in
    -a | --all)
        ALL=y
        shift
        ;;
    --)
        shift
        break
        ;;
    *)
        echo "Unknown argument: $1"
        exit 3
        ;;
    esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# rm -v "$REPO_ROOT/data/"*"-job-"*".blend" "$REPO_ROOT/data/"*"-cylinders.json" "$REPO_ROOT/data/"*".blend1"
find "$REPO_ROOT/data" \( -name '*-job-*.blend' -or -name '*-cylinders.json' -or -name '*.blend1' \) -delete

if [[ $ALL == y ]]; then
    # rm -v "$REPO_ROOT/data/"*".blend"
    find "$REPO_ROOT/data" -name '*.blend' -delete
fi
