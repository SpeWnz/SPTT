import pyautogui
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import pyperclip

np.debugPrint("Loading target list ...")
targets = fm.fileToSimpleList(str(sys.argv[1]))

PROGRESS_COUNT = 0
TOTAL_COUNT = len(targets)

def queryMail(mail: str):

    # split mail --> pyautogui cant write @
    values = mail.split('@')

    
    pyautogui.moveTo(x=coordinates.x,y=coordinates.y)
    pyautogui.click()
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')

    pyautogui.write(values[0])
    pyperclip.copy('@')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.write(values[1])

    pyautogui.press('enter')

# ==============================================================================

np.infoPrint("Phase 1 - Determining coordinates. Focus this terminal, then move the mouse over the HaveIBeenPwned page, then press enter.")
input()

coordinates = pyautogui.position()
print(coordinates,"\n\n")

np.infoPrint("Phase 2 - Querying the mails. Press enter when you're ready.")


for mail in targets:

    progressPercenteage = int((PROGRESS_COUNT / TOTAL_COUNT) * 100)

    np.infoPrint("Progress: {}% \r\t\t\t {}/{}".format(progressPercenteage,PROGRESS_COUNT,TOTAL_COUNT))
    print("Target:",mail)
    queryMail(mail)    
    input("Press enter to continue.\n")

    PROGRESS_COUNT += 1
    

