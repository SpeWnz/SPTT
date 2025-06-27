import _common
import ZHOR_Modules.nicePrints as np
import os


np.infoPrint("Starting netcat listener on {}".format(_common.CONFIG['netcat-listen-port']))
com = "nc -lvvp {}".format(_common.CONFIG['netcat-listen-port'])
os.system(com)