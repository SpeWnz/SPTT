import time
import pyautogui
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.osUtils as osu
import sys
import argparse
import pyperclip

# script che scrive da solo le credenziali sui form di login
# utile laddove il'intruder non è utilizzabile per via di meccanismi complessi di login

__VERSION = "v300125"

parser = argparse.ArgumentParser(description="Intruder Autogui " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"INPUT"',type=str,required=True,help='Input users list')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"INPUT"',type=str,required=True,help='Input passw list')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--start-index',metavar='"PREFIX STRING"',type=int,help='Index to start (by default, start at the beginning of the list')
OPTIONAL_ARGUMENTS.add_argument('--alt-tab',action="store_true",help="Also automatically alt+tab")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# ============================================================================================================================================================

np.debugPrint("Loading lists ...")
USERS = fm.fileToSimpleList(args.u)
PASSW = fm.fileToSimpleList(args.p)


STARTING_INDEX = 0

if ('--start-index' in sys.argv):
    STARTING_INDEX = args.start_index

ALT_TAB = False
if ('--alt-tab' in sys.argv):
    ALT_TAB = True

PROGRESS_COUNT = 0
TOTAL_COUNT = len(USERS)


USER_POS = None
PASS_POS = None
SUBM_POS = None


def queryTarget(user: str, passw: str):
    global USER_POS
    global PASS_POS
    global SUBM_POS
    
    # user 
    pyautogui.click(x=USER_POS.x,y=USER_POS.y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')
    pyperclip.copy(user)
    pyautogui.hotkey('ctrl','v')
    time.sleep(0.5)
    
    # pass
    pyautogui.click(x=PASS_POS.x,y=PASS_POS.y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')
    pyperclip.copy(passw)
    pyautogui.hotkey('ctrl','v')
    time.sleep(0.5)

    # submit 
    pyautogui.click(x=SUBM_POS.x,y=SUBM_POS.y)
    time.sleep(0.5)

    if ALT_TAB:
        pyautogui.hotkey('alt','tab')


# ==============================================================================

if __name__ == '__main__':


    np.infoPrint("Determining user coordinates. Focus this terminal, then hover the mouse on the user textbox, then press enter.")
    input()
    USER_POS = pyautogui.position()
    np.debugPrint(f"{USER_POS}")

    np.infoPrint("Determining password coordinates. Focus this terminal, then hover the mouse on the password textbox, then press enter.")
    input()
    PASS_POS = pyautogui.position()
    np.debugPrint(f"{PASS_POS}")

    np.infoPrint("Determining submit button coordinates. Focus this terminal, then hover the mouse on the submit button, then press enter.")
    input()
    SUBM_POS = pyautogui.position()
    np.debugPrint(f"{SUBM_POS}")

    np.infoPrint("Done. Press enter when you're ready.")
    osu.pressEnterToContinue()

    PROGRESS_COUNT = STARTING_INDEX

    for i in range(STARTING_INDEX,len(USERS)):
        
        PROGRESS_COUNT += 1
        progressPercenteage = int((PROGRESS_COUNT / TOTAL_COUNT) * 100)

        np.infoPrint("Progress: {}% \r\t\t\t {}/{}".format(progressPercenteage,PROGRESS_COUNT,TOTAL_COUNT))
        print("Trying:",USERS[i],PASSW[i])
        queryTarget(USERS[i],PASSW[i])    
        input("Press enter to continue.\n")

        

