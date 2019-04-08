#!/bin/bash
set -o errexit -o pipefail -o noclobber -o nounset

! getopt --test >/dev/null
if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
    echo "getopt failed."
    exit 1
fi

OPTIONS=j:
LONGOPTIONS=jobs:

! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    exit 2
fi

eval set -- "$PARSED"

JOBS=1

while true; do
    case "$1" in
    -j | --jobs)
        JOBS="$2"
        shift 2

        if [[ ! $JOBS =~ ^-?[0-9]+$ ]]; then
            echo "--jobs must be an integer."
            exit 3
        fi
        ;;
    --)
        shift
        break
        ;;
    *)
        echo "Unknown argument: $1"
        exit 4
        ;;
    esac
done

CONFIG_FILE=/dev/null

if [[ $# -ne 1 ]]; then
    echo "$0: A single configuration file is required."
    exit 5
else
    CONFIG_FILE="$1"
    echo "Using config file ${CONFIG_FILE} with ${JOBS} jobs..."
fi

# Make the fractal Python library visible to Blender.
PYTHONPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
echo "Setting PYTHONPATH=${PYTHONPATH}..."
export PYTHONPATH

blender --background --python generate.py -- "${CONFIG_FILE}"

for ((job = 0; job < JOBS; job++)); do
    echo "Starting job $job..."
    # TODO: Capture output?
    blender --background --python render.py -- "${CONFIG_FILE/.json/-cylinders.json}" --job "$job" --jobs "$JOBS" "${CONFIG_FILE/.json/-job-$job.blend}" &
done

# TODO: Find a way to wait until the above generation is done.
# CHUNKED_FILES=("${CONFIG_FILE/.json/-job-}"*".blend")
# echo "Joining" "${CHUNKED_FILES[@]}" "..."

# blender --background --python join.py -- "${CHUNKED_FILES[@]}"
