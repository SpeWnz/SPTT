import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.osUtils as osu

import argparse
import sys
import os
import itertools

parser = argparse.ArgumentParser(description="Hashcat wordlist generator")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-r',metavar='"RULES"',type=str,required=True,help='Rules file')
REQUIRED_ARGUMENTS.add_argument('-w',metavar='"WORDLIST"',type=str,required=True,help='Keywords file')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FILE"',type=str,required=True,help='Output file')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('-stf',type=str,required=True,help="Sort Temp Folder (temporary folder used by the sort utility. By default is in /tmp. For very large wordlists it is recommended to select another path)")
OPTIONAL_ARGUMENTS.add_argument('-P2',action="store_true",help="Add 2-Permutation words to pre-elaborated wordlist")
OPTIONAL_ARGUMENTS.add_argument('-P3',action="store_true",help="Add 3-Permutation words to pre-elaborated wordlist")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==================================================================================================================================

TEMP_LIST_NAME = "__temp"
TEMP_SORT_FOLDER = "/tmp"

def generatePermutations(input_list, n, allow_repeats=True):
    if allow_repeats:
        # Generate permutations with repetition allowed
        return [''.join(p) for p in itertools.product(input_list, repeat=n)]
    else:
        # Generate permutations without repetition
        return [''.join(p) for p in itertools.permutations(input_list, n)]

# generates the pre-elaborated wordlist to feed into hashcat
def generateInputList(inputListPath: str):
    words = fm.fileToSimpleList(inputListPath)
    outputList = []

    outputList += lu.toLowerAll(words)  # add all lower
    outputList += lu.toUpperAll(words)  # add all upper

    outputList = lu.removeDuplicates(outputList)

    # at this point the list contains all words plus all "2-permutations" and "3-permutations"
    
    if '-P2' in sys.argv:
        outputList += generatePermutations(outputList,2,False)
    
    if '-P3' in sys.argv:
        outputList += generatePermutations(outputList,3,False)

    fm.listToFile(outputList,TEMP_LIST_NAME) 
    

# idea from: https://infinitelogins.com/2020/11/16/using-hashcat-rules-to-create-custom-wordlists/
# hashcat --force <wordlist> -r append_exclamation.rule -r /usr/share/hashcat/rules/best64.rule --stdout | sort -u > hashcat_words.txt
if __name__ == '__main__':

    res, _ = osu.commandResult("which hashcat")

    if res == '':
        np.errorPrint("Hashcat was not found.")
        exit()

    if '-stf' in sys.argv:
        TEMP_SORT_FOLDER = args.stf

    np.infoPrint("Genrating pre-elaborated wordlist to feed into hashcat...")
    generateInputList(args.w)
    #input("asd")
    
    com = 'hashcat --force "{}" -r "{}" --stdout | sort -u -T "{}" > "{}"'.format(
        TEMP_LIST_NAME,
        args.r,
        TEMP_SORT_FOLDER,
        args.o
    )
    np.debugPrint(com)
    
    np.infoPrint("Generating wordlist ...")
    os.system(com)
    np.infoPrint("Done")

    os.remove(TEMP_LIST_NAME)