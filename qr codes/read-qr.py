from PIL import Image
from pyzbar.pyzbar import decode
import argparse
import sys

import ZHOR_Modules.nicePrints as np

parser = argparse.ArgumentParser(description="Read QR Code")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input text file')


# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

if __name__ == '__main__':        
    data = decode(Image.open(args.i))
    print(str(data[0].data.decode('utf-8')))