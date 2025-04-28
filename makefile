# tool macros
# VIV_BIN := /tools/Xilinx/Vivado/2024.1/bin
VIV_BIN := /c/AMD/Vivado/2024.1/bin
# VITIS_BIN := /tools/Xilinx/Vitis/2024.1/bin
VITIS_BIN := /c/AMD/Vitis/2024.1/bin

PYTHON :=/c/AMD/Vivado/2024.1/tps/win64/python-3.8.3/python

VIVADO := $(VIV_BIN)/vivado
VITIS := $(VITIS_BIN)/vitis
HW_SERVER := $(VIV_BIN)/hw_server

# path macros
HDL_PATH := hdl
SW_SRC_PATH := sw
SCRIPTS_PATH := scripts

PL_OUTPUT_PATH := build/pl
PS_OUTPUT_PATH := build/ps

# Project data
define get_pl_config
    $(shell python -c "import json;\
                       a='$(HDL_PATH)/config.json';\
					   f=open(a);\
					   print(json.load(f)['$(1)'])")
endef
# the return from python includes leading whitespace
PROJECT_NAME := $(strip $(call get_pl_config,project_name))
BOARD_PART := $(strip $(call get_pl_config,board_part))

# default rule
default: build

# phony rules
.PHONY: makedir
makedir:
	@mkdir -p $(PL_OUTPUT_PATH)
	@mkdir -p $(PS_OUTPUT_PATH)

.PHONY: vivado
vivado:
	$(VIVADO) -mode batch -source $(SCRIPTS_PATH)/viv_build.tcl -tclargs $(PROJECT_NAME) $(BOARD_PART) $(HDL_PATH) $(PL_OUTPUT_PATH) $(PYTHON)
	mv *.jou *.log $(PL_OUTPUT_PATH)
	mv ./$(PL_OUTPUT_PATH)/$(PROJECT_NAME).runs/impl_1/*.bit ./$(PL_OUTPUT_PATH)

.PHONY: vitis
vitis:
	$(VITIS) -s $(SCRIPTS_PATH)/vitis_build.py $(PS_OUTPUT_PATH) $(SW_SRC_PATH) $(PL_OUTPUT_PATH)

.PHONY: build
build: clean makedir vivado vitis

.PHONY: vitis_xsdb
vitis_xsdb:
	$(VITIS) -s $(SCRIPTS_PATH_REL)/vitis_xsdb.py  $(PS_OUTPUT_PATH) $(SW_SRC_PATH) $(PL_OUTPUT_PATH) $(HW_SERVER)
	# killall hw_server
	 taskkill /IM hw_server.exe /F

.PHONY: vitis_clean
vitis_clean:
	@rm -rf $(PS_OUTPUT_PATH) $(SW_SRC_PATH)/__pycache__/

.PHONY: clean
clean:
	@rm -rf $(PL_OUTPUT_PATH) $(PS_OUTPUT_PATH)
