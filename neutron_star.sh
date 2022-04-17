#!/bin/bash


action="${1}"

function check_args() {
    echo "${action}" | grep -E 'run' > /dev/null
    if (($? != 0)); then
        echo "Args must be [ run ]"
        exit 1
    fi
}


function run() {
    uvicorn --host 0.0.0.0 --port 12599 neutron_star.app.app:app --reload
}

function main() {
    check_args
    if [[ "${action}" == "run" ]]; then
        run
    fi
}

main
exit 0