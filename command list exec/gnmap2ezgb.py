import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import _common

# what should the script look for
_common.nmapFilters = ["http","https"]

# edit these
ezgb_executable_path = "INSERT HERE"
ezgb_template_path = "INSERT HERE"
ezgb_output_folder_path = "INSERT HERE"

if __name__ == '__main__':    

    if len(sys.argv) != 3:
        msg = "Usage: python3 {} <gnmap file> <output json file name>".format(sys.argv[0])
        np.infoPrint(msg)
        exit()

    out = []
    targets = _common.getTargets_http(str(sys.argv[1]))
    for item in targets:

        # BUILD COMMAND HERE

        # python3 -u for unbuffered stdout
        target = '"{}:{}"'.format(item['ip'],item['port'])
        com = 'python3 -u "{}" -T "{}" -t "{}" -o "{}"'.format(
            ezgb_executable_path,
            target,
            ezgb_template_path,
            ezgb_output_folder_path
            )
        if (item['ssl']):
            com += ' --https'

        
        out.append(com)
    

    _common.makeJsonDictionary(out,str(sys.argv[2]))

    
