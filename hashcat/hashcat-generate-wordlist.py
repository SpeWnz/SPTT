import ZHOR_Modules.nicePrints as np
import argparse
import sys
import os
import ZHOR_Modules.osUtils as osu

parser = argparse.ArgumentParser(description="Hashcat wordlist generator")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-r',metavar='"RULES"',type=str,required=True,help='Rules file')
REQUIRED_ARGUMENTS.add_argument('-w',metavar='"WORDLIST"',type=str,required=True,help='Password wordlist file')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FILE"',type=str,required=True,help='Output file')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==================================================================================================================================

# idea from: https://infinitelogins.com/2020/11/16/using-hashcat-rules-to-create-custom-wordlists/
# hashcat --force <wordlist> -r append_exclamation.rule -r /usr/share/hashcat/rules/best64.rule --stdout | sort -u > hashcat_words.txt
if __name__ == '__main__':
    res, _ = osu.commandResult("which hashcat")

    if res == '':
        np.errorPrint("Hashcat was not found.")
        exit()

    com = 'hashcat --force "{}" -r "{}" --stdout | sort -u > "{}"'.format(
        args.w,
        args.r,
        args.o
    )
    np.debugPrint(com)
    
    np.infoPrint("Generating wordlist ...")
    os.system(com)
    np.infoPrint("Done")
