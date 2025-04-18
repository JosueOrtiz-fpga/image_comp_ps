import sys
import subprocess
import re
import json
import time
import vitis
from xsdb import *

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
session.connect(url=start_hw_server(sys.argv[1]))

print("Session Started\n")
print("Printing Targets\n")
session.targets()

session.targets(3)
session.fpga(file="./lwip_echo_server/_ide/bitstream/image_comp_ps.bit")

session.targets(2)
session.dow("./z7_echo_server_pform/zynq_fsbl/build/fsbl.elf")
session.con()
time.sleep(5)
session.stop()

session.dow('./lwip_echo_server/build/lwip_echo_server.elf')
session.con()
time.sleep(5)
session.stop()

exit()
vitis.dispose()
