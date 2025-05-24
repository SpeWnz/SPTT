import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm

import paramiko
from datetime import timedelta
import argparse
import sys
import time
import os




parser = argparse.ArgumentParser(description="SCP Dumper - download multiple remote files with SCP")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET"',type=str,required=True,help='Target IP or fqdn')
REQUIRED_ARGUMENTS.add_argument('-f',metavar='"FILES"',type=str,required=True,help='List of remote files to download')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USER"',type=str,required=True,help='User')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Path of output folder to dump files into')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('-p',metavar='"PASSWORD"',type=str,help='Passwords')
OPTIONAL_ARGUMENTS.add_argument('-k',metavar='"KEY"',type=str,help='Private key file')
OPTIONAL_ARGUMENTS.add_argument('-P',metavar='"PASSPHRASE"',type=str,help='Private key passphrase (default: None)')
OPTIONAL_ARGUMENTS.add_argument('--port',type=str,help='Port (Default: 22)')

OPTIONAL_ARGUMENTS.add_argument('-s',metavar='"SLEEP"',type=int,help='Sleep time between each request (in milliseconds)')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ===============================================================================================================================================

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

privateKey              = None
privateKey_passphrase   = None
privateKeyObject        = None
password                = None
localDownloadPathRoot   = args.o
port                    = 22

# ===============================================================================================================================================


if __name__ == '__main__':

    # set password if present
    if (args.p) != None:
        password = args.p

    # set passphrase if present
    if (args.P) != None:
        privateKey_passphrase = args.P

    # set different port if specified
    if (args.port) != None:
        port = args.port
    

    # load pk in memory
    if (args.k != None):
        privateKey = args.k
        # If your key is not RSA (e.g., ed25519), you can use paramiko.Ed25519Key similarly
        privateKeyObject = paramiko.RSAKey.from_private_key_file(privateKey, password=privateKey_passphrase)

    # Connect to the server using private key authentication
    ssh.connect(args.t, port=port, username=args.u,password=password, pkey=privateKeyObject)

    # Open SFTP session
    sftp = ssh.open_sftp()

    # Download the file
    files = fm.fileToSimpleList(args.f)

    for file in files:

        localPath = f"{localDownloadPathRoot}/{args.t}/{file}"
        os.makedirs(os.path.dirname(localPath), exist_ok=True)

        sftp.get(file, localPath)
        print(f"Downloaded {file} to {localPath}")


    # Close the SFTP session and SSH connection
    sftp.close()
    ssh.close()