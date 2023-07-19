import pyautogui
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import argparse
import pyperclip

# script che scrive da solo nella barra di ricerca
# utile per siti con api a pagamento
# es: dehashed, ripe, bugmenot, hipb, ecc...

__VERSION = "v190723"

parser = argparse.ArgumentParser(description="Insert Target Autogui " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input target list')



# Argomenti opzionali
REQUIRED_ARGUMENTS.add_argument('--start-index',metavar='"PREFIX STRING"',type=int,help='Index to start (by default, start at the beginning of the list')
REQUIRED_ARGUMENTS.add_argument('--prefix',metavar='"PREFIX STRING"',type=str,help='String to place before target item')
REQUIRED_ARGUMENTS.add_argument('--suffix',metavar='"SUFFIX STRING"',type=str,help='String to place after target item')
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




    

PROGRESS_COUNT = 0
TOTAL_COUNT = len(targets)

def queryTarget(target: str):
    
    pyautogui.moveTo(x=coordinates.x,y=coordinates.y)
    pyautogui.click()
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')

    if PREFIX is not None:
        pyperclip.copy(PREFIX)
        pyautogui.hotkey('ctrl', 'v')

    pyperclip.copy(target)
    pyautogui.hotkey('ctrl', 'v')


    if SUFFIX is not None:
        pyperclip.copy(SUFFIX)
        pyautogui.hotkey('ctrl', 'v')


    pyautogui.press('enter')

# ==============================================================================

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

    

