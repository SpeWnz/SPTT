import os
import sys
import glob
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np

if __name__ == '__main__':
    

    if len(sys.argv) < 3:
        np.infoPrint("Usage: python3 {} <commands output folder> <report name>".format(str(sys.argv[0])))
        exit()

    folderPath = str(sys.argv[1])
    reportPath = str(sys.argv[2])

    if not os.path.isdir(folderPath):
        np.errorPrint("Path is not a folder")
        exit()
    

    maxLength = 0
    files = glob.glob(folderPath + "/*.txt")

    for f in files:
        lines = fm.fileToSimpleList(f)

        for l in lines:
            if len(l) > maxLength:
                maxLength = len(l)


    print(maxLength)



    for f in files:
        
        title = " OUTPUT OF " + f + " "
        separator = ""
        if (maxLength - len(title)) > 0:
            separator = title + ("~" * (maxLength - len(title)))
        else:
            separator = title


        os.system("echo \"{}\" >> __temp.txt".format(separator))
        os.system("cat \"{}\" >> __temp.txt".format(f))
        os.system("echo \"\" >> __temp.txt")

    os.system("cat __temp.txt | aha --black > {}".format(reportPath))
    os.system("rm __temp.txt")


