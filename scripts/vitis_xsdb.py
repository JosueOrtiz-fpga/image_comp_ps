import sys
import os
import subprocess
import re
import json
import time
from pathlib import Path
from xsdb import *

ps_output_path = sys.argv[1]
sw_path = sys.argv[2]
pl_output_path = sys.argv[3]
hw_server_path = sys.argv[4]

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
session.connect(url=start_hw_server(hw_server_path))

print("Session Started\n")
print("Printing Targets\n")
session.targets()

bit_file_path = Path(pl_output_path).glob("*.bit") # returns a generator object
bit_file = str(list(bit_file_path)[0]) #list converts generator to list of PosixPath entries)
if os.path.exists(bit_file):
    session.targets(3)
    print("Programming the FPGA with " + bit_file + "\n")
    session.fpga(file=f"{bit_file}")

fsbl_elf = f"./{config.platform_name}/zynq_fsbl/build/fsbl.elf"
if os.path.exists(fsbl_elf):
    session.targets(2)
    print("Programming the FSBL " + fsbl_elf + "\n")
    session.dow(fsbl_elf)
    print("Running the FSBL " + fsbl_elf + "\n")
    session.con()
    time.sleep(5)
    session.stop()

app_elf = f"./{config.app_name}/build/{config.app_name}.elf"
if os.path.exists(app_elf):
    session.targets(2)
    print("Programming the APP " + app_elf + "\n")
    session.dow(app_elf)
    print("Running the APP " + app_elf + "\n")
    session.con()
    time.sleep(15)
    session.stop()

