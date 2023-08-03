#! /bin/bash
# Lucas Rountree, 2017
# Y/N block for copy/paste into scripts

read -p "Yes or No? Y/N [n]: " YORN2
if [ "${YORN2}" = "" ]; then
  YORN="n"
elif [ "${YORN2}" = "Y" -o "${YORN2}" = "y" -o "${YORN2}" = "n" -o "${YORN2}" = "N" ]; then
  YORN="${YORN2}"
else
  echo "Please choose y or n. Quitting."
fi
if [ "${YORN}" = "Y" -o "${YORN}" = "y" ]; then
  echo "Yes"
elif [ "${YORN}" = "N" -o "${YORN}" = "n" ]; then
  echo "No"
fi
