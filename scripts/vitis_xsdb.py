import sys
import subprocess
import re
import json
import time
import vitis
from xsdb import *

proj_name = sys.argv[1]
sw_path = sys.argv[2]
sys.path.append(sw_path) # config.py is in the sw_path
import config

def start_hw_server(hw_server_path):
    cmd = hw_server_path + " -d -S"
    result = subprocess.run(cmd, 
                            shell=True, 
                            capture_output=True, 
                            text=True)
    # properties JSON string are lead by a logger time stamp
    properties_json = re.findall(r"{.*}", result.stdout)[0]
    properties_dict = json.loads(properties_json)

    # hostname is returned with a trailing new line
    result = subprocess.run(["hostname"], capture_output=True, text=True)
    hostname = result.stdout.rstrip()
    
    url = properties_dict["TransportName"] + ":" + hostname + ":" + properties_dict["Port"]
    print(url)
    return url

session = start_debug_session()
session.connect(url=start_hw_server(sys.argv[3]))

print("Session Started\n")
print("Printing Targets\n")
session.targets()

session.targets(3)
session.fpga(file=f"./{config.app_name}/_ide/bitstream/{proj_name}.bit")

session.targets(2)
session.dow(f"./{config.platform_name}/zynq_fsbl/build/fsbl.elf")
session.con()
time.sleep(5)
session.stop()

session.dow(f"./{config.app_name}/build/{config.app_name}.elf")
session.con()
time.sleep(15)
session.stop()
vitis.dispose()

