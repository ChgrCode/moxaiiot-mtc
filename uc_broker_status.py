#!/usr/bin/env python3
'''
UC-8200 MQTT Broker LED status indicator.

This script turns on the user LED if MQTT broker is running and 
and toggles the LED if the subscribed toppic has some data.

Examples:
 
uc_broker_status.py -t "#"  monitors all topics
uc_broker_status.py -t "/MTC/#" monitors topics below /MTC

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

import paho.mqtt.client as mqtt

from uc_user_led import toggle_led_state, set_led_state

MQTT_TOPIC = "$SYS/#"
VERBOSE = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    set_led_state(1)
    print("Subscribe to topic: %s"% MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC)
    
# The callback for when the client disconnects from the server.
def on_disconnect(client, userdata, rc):
    print("Disonnected with result code "+str(rc))
    set_led_state(0)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if VERBOSE:
        print(msg.topic+" "+str(msg.payload))
    toggle_led_state(0.05)


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
    parser.add_argument("-t", "--topic", dest="topic", metavar="Topic", type=str, action="store", default='#', help="Topic to monitor")
    parser.add_argument("-v", "--verbose", dest="verbose_level", action="count", default=None, help="Turn on console DEBUG mode. Max = -vvv")
    parser.add_argument("-V", "--version", action="version", version=__version__) 

    return parser.parse_args(assigned_args)

'''
'''
def main(assigned_args = None):  
    # type: (List)    
    global MQTT_TOPIC, VERBOSE   
    
    cargs = main_argparse(assigned_args)   
    MQTT_TOPIC = cargs.topic
    VERBOSE = cargs.verbose_level
    
    set_led_state(0)
    toggle_led_state(1)
   
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    connect_success = False
    while not connect_success:
        try:
            print("Connect to localhost")
            client.connect("localhost", 1883, 60)
            connect_success = True
        except Exception as e:
            print(e)
            #traceback.print_exc(file=sys.stdout)           
        time.sleep(1)        
    
    try:    
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()
    except KeyboardInterrupt as e: 
        print("User disconnect")  
        client.disconnect()   
    except Exception as e:
        print(e)
        client.disconnect()
                         
    return 0
    
if __name__ == "__main__":     
    sys.exit(main())
