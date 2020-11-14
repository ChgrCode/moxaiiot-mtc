#! /usr/bin/python3
'''
UC-8200 User LED utillity.

This script turns on or off the User LED on the UC-82xx.

Examples: 
uc-led.py -v --on # turning on the LED with debug output
uc-led.py --off # turning off the LED without debug output
uc-led.py --toggle 1000 # toogle the user LED from off to on for 1000 micro seconds.

'''

'''
Change log    
1.0.0 - 2020-11-01 - cg
    Initial version
'''

__author__ = "chgrCode"
__license__ = "MIT"
__version__ = '1.0.0'
__maintainer__ = "chgrCode"
__credits__ = ["..."]
__status__ = "beta"

import os 
import sys
import traceback
import signal
import platform
import datetime
import time
import argparse
import subprocess


USER_OUTPUT="USER LED IS NOW "
LED_STATE=-1

'''
'''
def toggle_led_state(duration):
    state = -1
    
    state = LED_STATE
    
    if not (state == 0) and not (state == 1):
        print("ERROR(toggle_led_state): Wrong LED state %s\n", state)
        return False   
        
    if state == 1:
        ret = set_led_state(0)
        if not ret: return ret
        time.sleep(duration)
        ret = set_led_state(1)
        if not ret: return ret
    else:
        ret = set_led_state(1)
        if not ret: return ret
        time.sleep(duration)
        ret = set_led_state(0)
        if not ret: return ret       
    
    return True

'''
'''
def set_led_state(state):
    global LED_STATE
    LED_CND="/sbin/mx-led-ctl"
    mxledcmd = subprocess.run([LED_CND, "-p", "1", "-i", "1", led_state_txt(state)])
    if mxledcmd.returncode:
        print("ERROR(set_led_state): The exit code was: %d" % mxledcmd.returncode)
        print(mxledcmd.stdout)
        print(mxledcmd.stderr)
        return False
    LED_STATE=state
    return True


'''
'''
def led_state_txt(state):
    if state == 1:
        return "on"
    elif state == 0:
        return "off"
    else:
        return "Unknown"

'''
'''
def main_argparse(assigned_args = None):  
    # type: (List)  
    """
    Parse and execute the call from command-line.
    Args:
        assigned_args: List of strings to parse. The default is taken from sys.argv.
    Returns: 
        Namespace list of args
    """
    import argparse, logging
    parser = argparse.ArgumentParser(prog="uc-led-app", description=globals()['__doc__'], epilog="!!Note: .....")
    parser.add_argument("-0", "--off", dest="led_state", action="store_const",  const=0, default=-1, help="Turn off LED")
    parser.add_argument("-1", "--on", dest="led_state", action="store_const",  const=1, default=-1, help="Turn on LED")
    parser.add_argument("-t", "--toggle", dest="led_toggle", metavar="Toggle", type=int, action="store", default=-1, help="Toggle user LED for ms.")
    parser.add_argument("-v", "--verbose", dest="verbose_level", action="count", default=None, help="Turn on console DEBUG mode. Max = -vvv")
    parser.add_argument("-V", "--version", action="version", version=__version__) 

    return parser.parse_args(assigned_args)

'''
'''
def main(assigned_args = None):  
    # type: (List)    
    
    cargs = main_argparse(assigned_args)
    
    if cargs.verbose_level:
        print(cargs)
    
    if cargs.led_toggle == -1:
        if cargs.verbose_level:            
            print("Switch User LED to %s"% led_state_txt(cargs.led_state))
        if not set_led_state(cargs.led_state):
            return 1
    else:
        if cargs.verbose_level:
            print("Toggle User LED")
        if not set_led_state(0):
            return 1
        if not toggle_led_state(cargs.led_toggle/1000):
            return 1
    
    print("%s  %s\n"% (USER_OUTPUT, led_state_txt(LED_STATE)))    
                 
    return 0
    
if __name__ == "__main__":     
    sys.exit(main())
