import sys
import os
import vitis # AMD Vitis CLI package

# sert path and name vars from command-line input
sw_path = sys.argv[1]
sys.path.append(sw_path) # config.py is in the sw_path
import config

def get_platform_file(vitis_client, platform_dir):
    platform_xpfm=vitis_client.find_platform_in_repos(platform_dir)
    return platform_xpfm

def get_component(vitis_client, comp_name):
    try: comp = vitis_client.get_component(comp_name)
    except: return None
    else : return comp

client = vitis.create_client()
client.set_workspace(path="./")

platform = get_component(client, config.platform_name)
if not platform:
    raise Exception("Please create platform first")

# Second step is to create the application that will run on the platform
# If a app template is provided in config.py, check that it's valid
if config.template_name != None:
    if not config.template_name in client.get_templates('EMBD_APP'):
        raise Exception("Invalid template name provided")
    
# need to retrieve the platofrm xpfm file for app creation reference
platform_xpfm = get_platform_file(client, config.platform_name)

comp = get_component(client, config.app_name)
if not comp:
    print("App " + config.app_name + " does not exist")
    print("Creating the app")
    comp = client.create_app_component(name=config.app_name,
                                       platform =platform_xpfm,
                                       domain = config.os_name + "_"+ config.cpu_name,
                                       template = config.template_name)

# before building, add any user source files to the app project
sw_src_path = str(sw_path) + "/src"
if os.path.exists(sw_src_path): 
    comp.import_files(from_loc = sw_src_path, files=None, dest_dir_in_cmp="src")
comp.build()

# Finish
vitis.dispose()
