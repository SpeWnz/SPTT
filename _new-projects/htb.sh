#!/bin/sh
# script to quickly make folders and subfolder for a new htb machine

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
echo "IyBSRUNBUCBNQUNDSElORQoKIyMgTk9NSSBNQUNDSElORSBFIEZMQUcKCnwgbm9tZSAgICAgIHwgdWx0aW1vIG90dC4gICB8IHByb29mIGZsYWcgICB8IGxvY2FsIGZsYWd8CnwgLS0tLS0tLS0gIHwgLS0tLS0tLSAgICAgICB8LS0tLS0tLS0gICAgICB8IC0tLS0tLS0tICB8CnwgREMwMSAgICAgIHwgLjE0MCAgICAgICAgICB8ICAgICAgICAgICAgICB8ICAgICAgICAgICB8CnwgTVMwMSAgICAgIHwgLjE0MSAgICAgICAgICB8ICAgICAgICAgICAgICB8ICAgICAgICAgICB8CnwgTVMwMiAgICAgIHwgLjE0MiAgICAgICAgICB8ICAgICAgICAgICAgICB8ICAgICAgICAgICB8CnwgVk0xICAgICAgIHwgLjE0MyAgICAgICAgICB8ICAgICAgICAgICAgICB8ICAgICAgICAgICB8CnwgVk0yICAgICAgIHwgLjE0NCAgICAgICAgICB8ICAgICAgICAgICAgICB8ICAgICAgICAgICB8CnwgVk0zICAgICAgIHwgLjE0NSAgICAgICAgICB8ICAgICAgICAgICAgICB8ICAgICAgICAgICB8CgojIyBNYWNjaGluZSBlIGNyZWRzCkRDMDEgMTAuMTAuMTAyLjE0MAoKTVMwMSAxOTIuMTY4LjE0Mi4xNDEgICAgICAgIAoKTVMwMiAxMC4xMC4xMDIuMTQyCgpWTTEgMTkyLjE2OC4xNDIuMTQzIAoKVk0yIDE5Mi4xNjguMTQyLjE0NAoKVk0zIDE5Mi4xNjguMTQyLjE0NQoKCiMgU1ZPTEdJTUVOVE8gVk0gSU5ESUUKCiMjIFZNMQoKYXNkYXNkYXNkCgoKIyMgVk0yCgphc2Rhc2Rhc2QKCiMjIFZNMwoKYXNkYXNkYXNkCgojIFNWT0xHSU1FTlRPIEFEIFNFVAoKIyMgTVMwMQoKYXNkYXNkCgojIyBNUzAyCgphc2Rhc2QKCiMjIERDMDEKCmFzZGFzZA==" | base64 -d > notes.md

mkdir "nmap-scans"
mkdir "nmap-sqlite"
mkdir "targets"

mkdir "creds"
touch "creds/users.txt"
touch "creds/passwords.txt"
touch "creds/hashes.txt"
mkdir "dumps"
mkdir "file-upload-samples"
mkdir "sqlmap"
mkdir "mimikatz"
mkdir "ferox-buster-scans"
mkdir "winpeas"
mkdir "linpeas"
