#-----------------------------------------------------------------
# Vitis v2024.1 (64-bit)
# Start of session at: Fri Apr 18 09:47:04 2025
# Current directory: C:\Users\aj582\projects\image_comp_ps
# Command line: vitis -i
# Journal file: vitis_journal.py
# Batch mode: $XILINX_VITIS/bin/vitis -new -s C:\Users\aj582\projects\image_comp_ps\vitis_journal.py
#-----------------------------------------------------------------

#!/usr/bin/env python3
import vitis
from xsdb import *
import time
s = start_debug_session()
s.connect(url="TCP:DESKTOP-L2M9C3R:3121")
#[Out]# 'tcfchan#0'
session.targets()
targets()
ta
s.ta()
s.ta(2)
#[Out]# <xsdb.target.Target at 0x14fa5580d90>
s.ta()
s.rst()
s.ta()
s.ta(3)
#[Out]# <xsdb.target.Target at 0x14fa575d430>
s.ta()
s.fpga(file="./lwip_echo_server/_ide/bitstream/image_comp_ps.bit")
import os
os.getcwd()
#[Out]# 'C:\\Users\\aj582\\projects\\image_comp_ps'
s.fpga(file="./build/ps/lwip_echo_server/_ide/bitstream/image_comp_ps.bit")
s.dow('./build/ps/lwip_echo_server/build/lwip_echo_server.elf')
s.ta(2)
#[Out]# <xsdb.target.Target at 0x14fa58c3c10>
s.ta
#[Out]# <function xsdb.session.Session.__getattr__.<locals>.unknown(*args, **kwargs)>
s.ta()
s.dow('./build/ps/lwip_echo_server/build/lwip_echo_server.elf')
s.dow("./build/ps/z7_echo_server_pform/zynq_fsbl/build/fsbl.elf")
s.con
#[Out]# <bound method Target.con of <xsdb.session.Session object at 0x0000014FA458C400>>
s.con()
s.stop()
s.dow('./build/ps/lwip_echo_server/build/lwip_echo_server.elf')
s.con()
s.stop()
s.rst()
exit()
vitis.dispose()
