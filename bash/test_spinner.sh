#! /bin/bash

# Set Variables/Arrays
#SPIN_ARR=(◐ ◓ ◑ ◒)
#SPIN_ARR=(◴ ◷ ◶ ◵)
SPIN_ARR=(○ ◎ ◉ ● ◉ ◎)
SPIN_CYCLE="0"

# Run something to test against
test_process() {
sleep 10
}

# Basic spinner test
test_spinner() {
while [ "${SPIN_CYCLE}" -le "3" ]
do
  for ELEMENT in "${SPIN_ARR[@]}"
  do
    if [ "${ELEMENT}" == "${SPIN_ARR[0]}" ]; then
      SPIN_CYCLE="$((${SPIN_CYCLE} + 1))"
    fi
    echo -ne "\rRunning: ${ELEMENT} "
    sleep .5
  done
done
}

# Test spinner against function
test_spinner_function() {
FUNCTION_PID="$!"
while [ "$(ps -A | grep "${FUNCTION_PID}")" ]
do
  for ELEMENT in "${SPIN_ARR[@]}"
  do
    echo -ne "\rRunning: ${ELEMENT} "
    sleep .5
  done
done
}

test_process & test_spinner_function
