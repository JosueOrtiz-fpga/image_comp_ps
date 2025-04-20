import sys
import os
import json
import vitis # AMD Vitis CLI package

# sert path and name vars from command-line input
proj_name = sys.argv[1]
sw_path = sys.argv[2]
pl_output_path = sys.argv[3]

xsa_file = pl_output_path + "/" + proj_name + ".xsa"
sys.path.append(sw_path) # config.py is in the sw_path

import config

def get_platform_file(vitis_client, platform_dir):
    platform_xpfm=vitis_client.find_platform_in_repos(platform_dir)
    return platform_xpfm

def get_component(vitis_client, comp_name):
    try: comp = vitis_client.get_component(comp_name)
    except: return None
    else : return comp

def get_domain(platform, dom_name):
    try: dom = platform.get_domain(dom_name)
    except: return None
    else : return dom

def lib_in_bsp(domain, lib_name):
    dom_libs = domain.get_libs()
    lib_names = []
    for dicts in dom_libs:
        lib_names.append(dicts["name"])
    return (lib_name in lib_names)

client = vitis.create_client()
client.set_workspace(path="./")

# the platform is the first component that needs to be created
platform = get_component(client, config.platform_name)
if not platform:
    print("Platform " + config.platform_name + " does not exist")
    print("Creating the platform")
    # first step is to create the platform with details
    # from the config.py file
    platform = client.create_platform_component(name = config.platform_name,
                                                hw_design = xsa_file,
                                                os = config.os_name,
                                                cpu = config.cpu_name, 
                                                no_boot_bsp = False)

# ensure the domain exists
domain_name = config.os_name + "_"+ config.cpu_name
domain = get_domain(platform, domain_name)
if not domain:
    print("Domain " + domain_name + " does not exist")
    print("Creating the domain")
    domain = platform.add_domain(name = domain_name, 
                                 cpu = config.cpu_name, 
                                 os = config.os)
    
# ensure the bsp libraries have been added
if config.bsp_libs != None:
    print("User bsp_entries not empty")
    print("Checking if bsp_libs are already added")
    for lib_name in config.bsp_libs:
        if not lib_in_bsp(domain, lib_name):
            print("Adding " + lib_name +" lib")
            domain.set_lib(lib_name=lib_name)
platform.build()

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
