import pyautogui
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import pyperclip

np.debugPrint("Loading target list ...")
targets = fm.fileToSimpleList(str(sys.argv[1]))

PROGRESS_COUNT = 0
TOTAL_COUNT = len(targets)

def queryTarget(target: str):
    
    pyautogui.moveTo(x=coordinates.x,y=coordinates.y)
    pyautogui.click()
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')

    pyautogui.write(target)

    pyautogui.press('enter')

# ==============================================================================

np.infoPrint("Phase 1 - Determining coordinates. Focus this terminal, then move the mouse over the BugMeNot page, then press enter.")
input()

coordinates = pyautogui.position()
print(coordinates,"\n\n")

np.infoPrint("Phase 2 - Querying the targets. Press enter when you're ready.")


for t in targets:

    PROGRESS_COUNT += 1
    progressPercenteage = int((PROGRESS_COUNT / TOTAL_COUNT) * 100)

    np.infoPrint("Progress: {}% \r\t\t\t {}/{}".format(progressPercenteage,PROGRESS_COUNT,TOTAL_COUNT))
    print("Target:",t)
    queryTarget(t)    
    input("Press enter to continue.\n")

    

