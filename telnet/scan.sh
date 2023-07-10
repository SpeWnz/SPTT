#!/bin/sh


TARGET=$1
PORT=$2

module="auxiliary/scanner/telnet/telnet_version"
printf "MSF Module: $module\n"
msfconsole -q -x "use $module; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"

module="auxiliary/scanner/telnet/brocade_enable_login"
printf "MSF Module: $module\n"
msfconsole -q -x "use $module; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"

module="auxiliary/scanner/telnet/telnet_encrypt_overflow"
printf "MSF Module: $module\n"
msfconsole -q -x "use $module; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"

module="auxiliary/scanner/telnet/telnet_ruggedcom"
printf "MSF Module: $module\n"
msfconsole -q -x "use $module; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"
