import _common
import ZHOR_Modules.nicePrints as np
import os


np.infoPrint("Starting netcat listener on {}:{}".format(_common.CONFIG['our-ip'],_common.CONFIG['our-port']))
com = "nc -lvvp {}".format(_common.CONFIG['our-port'])
os.system(com)