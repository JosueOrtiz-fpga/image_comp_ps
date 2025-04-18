import sys
import subprocess
import re
import json
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

    return properties_dict["TransportName"] + ":" + hostname + ":" + properties_dict["Port"]

session = start_debug_session()
session.connect(url=start_hw_server(sys.argv[1]))
print(session.targets())

# print(start_hw_server(sys.argv[1]))
