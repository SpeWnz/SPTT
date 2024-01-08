import pyautogui
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.argparseUtils as apu
import sys
import argparse
import pyperclip

# script che scrive da solo nella barra di ricerca
# utile per siti con api a pagamento
# es: dehashed, ripe, bugmenot, hipb, ecc...

__VERSION = "v122023"

parser = argparse.ArgumentParser(description="Insert Target Autogui " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input target list')



# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--start-index',metavar='"PREFIX STRING"',type=int,help='Index to start (by default, start at the beginning of the list')
OPTIONAL_ARGUMENTS.add_argument('--prefix',metavar='"PREFIX STRING"',type=str,help='String to place before target item')
OPTIONAL_ARGUMENTS.add_argument('--suffix',metavar='"SUFFIX STRING"',type=str,help='String to place after target item')
OPTIONAL_ARGUMENTS.add_argument('--alt-tab',action="store_true",help="Also automatically alt+tab")
OPTIONAL_ARGUMENTS.add_argument('-rs',metavar='"REPLACE STRING"',type=str,help='String to replace (for example §§§) (MUTINC with -rw)')
OPTIONAL_ARGUMENTS.add_argument('-rw',metavar='"REPLACE WITH"',type=str,help='Replace the -rs argument with some string (MUTINC with -rs)')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# ============================================================================================================================================================

np.debugPrint("Loading target list ...")
targets = fm.fileToSimpleList(args.i)


STARTING_INDEX = 0

if ('--start-index' in sys.argv):
    STARTING_INDEX = args.start_index

PREFIX = args.prefix
SUFFIX = args.suffix

ALT_TAB = False
if ('--alt-tab' in sys.argv):
    ALT_TAB = True



    

PROGRESS_COUNT = 0
TOTAL_COUNT = len(targets)


def composeString(target: str):
    toPaste = ""
    
    if PREFIX is not None:
        toPaste += PREFIX

    toPaste += target    

    if SUFFIX is not None:
        toPaste += SUFFIX


    # do we have to replace something?
    if '-rs' in sys.argv:
        toReplace = args.rs
        replaceWith = args.rw

        toPaste = toPaste.replace(toReplace,replaceWith)

    return toPaste


def queryTarget(target: str):
    
    pyautogui.moveTo(x=coordinates.x,y=coordinates.y)
    pyautogui.click()
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')

    toPaste = composeString(target)

    pyperclip.copy(toPaste)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')

    if ALT_TAB:
        pyautogui.hotkey('alt','tab')



# ==============================================================================

if __name__ == '__main__':

    if apu.checkMutIncArgs(sys.argv,['-rs','-rw']):
        pass
    else:
        exit()


    np.infoPrint("Phase 1 - Determining coordinates. Focus this terminal, then move the mouse over the page's search bar, then press enter.")
    input()

    coordinates = pyautogui.position()
    print(coordinates,"\n\n")

    np.infoPrint("Phase 2 - Querying the targets. Press enter when you're ready.")

    PROGRESS_COUNT = STARTING_INDEX

    for i in range(STARTING_INDEX,len(targets)):
        target = targets[i]

        PROGRESS_COUNT += 1
        progressPercenteage = int((PROGRESS_COUNT / TOTAL_COUNT) * 100)

        np.infoPrint("Progress: {}% \r\t\t\t {}/{}".format(progressPercenteage,PROGRESS_COUNT,TOTAL_COUNT))
        print("Target:",target)
        queryTarget(target)    
        input("Press enter to continue.\n")

        

