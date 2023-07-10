import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.userInputUtils as uiu
import base64

__VERSION = "v1 (170223)"
print("jwt-decoder",__VERSION,"\n\n")

np.infoPrint("Insert JWT Token")
token = str(input("> "))
print("\n\n\n\n")

values = token.split('.')
decodedValues = []

for v in values:
    v +=  "=" * ((4 - len(v) % 4) % 4)
    decodedValues.append(str(base64.b64decode(v))[2:-1])


for d in decodedValues:
    try:
        print("Decoded value:\n",d,"\n\n")
    except:
        np.errorPrint("Couldn't decode value")

