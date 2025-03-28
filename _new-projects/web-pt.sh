#!/bin/sh
# script to quickly make folders and subfolder for a new web pt activity

# Check if the number of arguments is not exactly 2
if [ $# -ne 2 ]; then
  echo "Usage: <project path> <project name>"
  exit 1
fi

# Assign the arguments to variables
project_path=$1
project_name=$2


cd $project_path
mkdir $project_name
cd $project_name

echo "ewoJImZvbGRlcnMiOiBbCgkJewoJCQkicGF0aCI6ICIuIgoJCX0KCV0sCgkic2V0dGluZ3MiOiB7fQp9" | base64 -d > $project_name.code-workspace

# make needed folders
mkdir "feroxbuster-scans"
mkdir "notes"
touch "notes/notes.txt"
mkdir "burp"
mkdir "creds"
touch "creds/users.txt"
touch "creds/passwords.txt"
mkdir "code-review"
mkdir headers
mkdir "dumps"
mkdir "sslscan"
mkdir "sqlmap"
mkdir "httpx"
mkdir "file-upload-samples"