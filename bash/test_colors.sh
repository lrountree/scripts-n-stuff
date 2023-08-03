#! /bin/bash

# Color reference
clear
# Using echo to set and unset the color
echo -ne "\e[4;38;5;93m"
echo "Bash Color Code Cheat Sheet! 38;5;93"
echo -ne "\e[24m"
echo -ne "\e[38;5;129m"
echo "Remember, \e[#m and you can clear with \e[0m foreground is 38;5 background is 48;5; and underline is 4;"
echo -ne "\e[0m"

# Echo command
echo -e "\e[34mBlue 34			     \e[1;34mBold\e[0m"
echo -e "\e[94mLight Blue  94		     \e[1;94mBold\e[0m"
echo -e "\e[38;5;21mElectric Blue  38;5;21       \e[1;38;5;21mBold\e[0m"
echo -e "\e[36mCyan  36		     \e[1;36mBold\e[0m"
echo -e "\e[96mLight Cyan  96	 	     \e[1;96mBold\e[0m"
echo -e "\e[91mLight Red  91		     \e[1;91mBold\e[0m"
echo -e "\e[31mRed  31			     \e[1;31mBold\e[0m"
echo -e "\e[33mYellow  33	 	     \e[1;33mBold\e[0m"
echo -e "\e[93mLight Yellow  93	     \e[1;93mBold\e[0m"
echo -e "\e[35mMagenta  35		     \e[1;35mBold\e[0m"
echo -e "\e[95mLight Magenta  95	     \e[1;95mBold\e[0m"
echo -e "\e[38;5;57mElectric Purple  38;5;57     \e[1;38;5;57mBold\e[0m"
echo -e "\e[92mLight Green  92		     \e[1;92mBold\e[0m"
echo -e "\e[38;5;46mBright Green  38	     \e[1;38;5;46mBold\e[0m"
echo -e "\e[37mLIght Grey  37		     \e[1;37mBold\e[0m"
echo -e "\e[90mDark Grey  90		     \e[1;90mBold\e[0m"
echo -e "\e[97mWhite  97		     \e[1;97mBold\e[0m"
echo -e $"\e[38;5;220mTest Here  38;5;220          \e[1;38;5;226mBold\e[0m"
echo ""

# Blinking
echo -e "\e[5;32mGreen, Blinking.\e[25;0m"
echo ""

# Hightlight
echo -e "\e[41mRed Hightlight\e[0m"
echo -e "\e[41;30mRed Highlight, Black Text\e[0m"
echo -e "\e[103mLight Yellow Highlight\e[0m"
echo -e "\e[42mGreen Highlight\e[0m"
echo -e "\e[105mLight Magenta Highlight\e[0m"
echo -e "\e[48;5;46;30mBrighter Green Highlight, Black Text\e[0m"
echo -e "\e[106;33mLight Cyan Highlight, Yellow Text\e[0m"
echo -e "\e[40;97mBlack Highlight, White Text\e[0m"
echo -e "\e[30;31mBlacker Highlight, Red Text\e[0m"
echo -e "\e[48;5;46;97mBright Green Highlight, White text\e[0m"
echo -e "\e[107;30mWhite Highlight, Black Text\e[0m"
echo -e "\e[42;30mGreen Highlight, Black Text\e[0m"
echo ""

# Read command, using 256 color grid
read -p $'\e[38;5;226mPrompt user for information:\e[0m ' Stack_Name

# Full 256 color grid
VAR1=`for i in {16..21} {21..16} ; do echo -en "\e[48;5;16;38;5;${i}m#\e[0m" ; done ; echo`
VAR2=`for i in {16..21} {21..16} ; do echo -en "\e[48;5;${i}m \e[0m" ; done ; echo`
VAR3=`for i in {256..232} {232..256} ; do echo -en "\e[48;5;${i}m \e[0m" ; done ; echo`
printf "${VAR1}${VAR2}${VAR3}\n"
for i in {0..256} ; do echo -en "\e[48;5;${i}m$i\e[0m" ; done ; echo
for i in {0..256} ; do echo -en "\e[38;5;${i}m$i\e[0m" ; done ; echo
