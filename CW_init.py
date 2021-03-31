import time
import globals
import chipwhisperer as cw
import subprocess
import sys

#   _____  ______ ______   
#  |  __ \|  ____|  ____|  
#  | |  | | |__  | |__ ___ 
#  | |  | |  __| |  __/ __|
#  | |__| | |____| |  \__ \
#  |_____/|______|_|  |___/
#                          
#                          

def cw_init() -> tuple:
    """
    Initialize the CW scope, the target and the programmer for future use
    """
    # scope = None
    # target = None
    # prog = None

    try:
        if not scope.connectStatus:
            scope.con()
    except NameError:
        scope = cw.scope()
    
    try:
        target = cw.target(scope)
    except IOError:
        print("INFO: Caught exception on reconnecting to target - attempting to reconnect to scope first.")
        print("INFO: This is a work-around when USB has died without Python knowing. Ignore errors above this line.")
        scope = cw.scope()
        target = cw.target(scope)

    print("INFO: Found ChipWhisperer😍")

    if "STM" in globals.cw_platform or globals.cw_platform == "CWLITEARM" or globals.cw_platform == "CWNANO":
        prog = cw.programmers.STM32FProgrammer
    elif globals.cw_platform == "CW303" or globals.cw_platform == "CWLITEXMEGA":
        prog = cw.programmers.XMEGAProgrammer
    else:
        prog = None

    time.sleep(0.05)
    scope.default_setup()
    scope.adc.samples = globals.cw_scope_adc_samples

    return (scope, target, prog)


def reset_target(scope) -> None:
    """
    Reset the CW target
    """
    if globals.cw_platform == "CW303" or globals.cw_platform == "CWLITEXMEGA":
        scope.io.pdic = 'low'
        time.sleep(0.1)
        scope.io.pdic = 'high_z' #XMEGA doesn't like pdic driven high
        time.sleep(0.1) #xmega needs more startup time
    else:  
        scope.io.nrst = 'low'
        time.sleep(0.05)
        scope.io.nrst = 'high_z'
        time.sleep(0.05)

def compile_target() -> None:
    """Program the CW target code"""

    try:
        res = subprocess.call("make PLATFORM=" + str(globals.cw_platform) + " CRYPTO_TARGET=" + str(globals.cw_cryptotarget) + " -C \""+str(globals.cw_target_fw_absolute_path)+"\"", shell=True)
        print(res)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        sys.exit("🔴 CW Compiler: Error when trying to launch compilation! 🔴\n")

    # %%bash -s "$PLATFORM" "$CRYPTO_TARGET"
    # cd ../../../hardware/victims/firmware/simpleserial-aes
    # make PLATFORM=$1 CRYPTO_TARGET=$2


def program_target(scope, prog) -> None:
    """Program the CW target"""
    cw.program_target(scope, prog, globals.cw_target_fw_absolute_path + globals.cw_target_fw_hex)


def disconnect(scope, target) -> None:
    target.dis()
    scope.dis()


