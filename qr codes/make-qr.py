import segno
import argparse
import sys

import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.timestampsUtils as tsu

parser = argparse.ArgumentParser(description="Make QR Code")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input text file')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

if __name__ == '__main__':        

    textContent = open(args.i,'r').read()
    outputFile = tsu.getTimeStamp_iso8601() + ".png"

    qrcode = segno.make_qr(textContent)
    qrcode.save(outputFile,scale=10)