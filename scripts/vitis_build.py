import sys
import os
import vitis # AMD Vitis CLI package

# sert path and name vars from command-line input
proj_name = sys.argv[1]
sw_path = sys.argv[2]
pl_output_path = sys.argv[3]

xsa_file = pl_output_path + "/" + proj_name + ".xsa"
sys.path.append(sw_path) # config.py is in the sw_path

import config


client = vitis.create_client()
client.set_workspace(path="./")

# first step is to create the platform with details
# from the config.py file
platform = client.create_platform_component(name = config.platform_name,
                                            hw_design = xsa_file,
                                            os = config.os_name,
                                            cpu = config.cpu_name, 
                                            no_boot_bsp = False)

# default domain created is name by concatenating os_name and _cpu_name
domain_name = config.os_name + "_"+ config.cpu_name
# before building, add any libraries caleld out in config.py
if config.bsp_libs != None:
    platform = client.get_component(config.platform_name)
    domain = platform.get_domain(domain_name)
    for lib_name in config.bsp_libs:
        status = domain.set_lib(lib_name=lib_name)
status = platform.build()

# Second step is to create the application that will run on the platform
# If a app template is provided in config.py, check that it's valid
if config.template_name != None:
    template_list = client.get_templates('EMBD_APP')
    check = config.template_name in template_list
    if check == False:
        raise Exception("Invalid template name provided")
    
# need to retrieve the platofrm xpfm file for app creation reference
platform_xpfm=client.find_platform_in_repos(config.platform_name)
comp = client.create_app_component(name=config.app_name,
                                   platform =platform_xpfm,
                                   domain = domain_name,
                                   template = config.template_name)

# before building, add any user source files to the app project
sw_src_path = str(sw_path) + "/src"
if os.path.exists(sw_src_path): 
    comp.import_files(from_loc = sw_src_path, files=None, dest_dir_in_cmp="src")
comp.build()

# Finish
vitis.dispose()
