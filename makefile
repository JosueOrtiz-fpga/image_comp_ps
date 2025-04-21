# tool macros
# VIV_BIN := /tools/Xilinx/Vivado/2024.1/bin
VIV_BIN := /c/AMD/Vivado/2024.1/bin
# VITIS_BIN := /tools/Xilinx/Vitis/2024.1/bin
VITIS_BIN := /c/AMD/Vitis/2024.1/bin

VIVADO := $(VIV_BIN)/vivado
VITIS := $(VITIS_BIN)/vitis
HW_SERVER := $(VIV_BIN)/hw_server

project_name := image_comp_ps

# path macros
HDL_SRC_PATH := hdl
SW_SRC_PATH := sw
SCRIPTS_PATH := scripts

PL_OUTPUT_PATH := build/pl/
PS_OUTPUT_PATH := build/ps/

# default rule
default: clean makedir vivado vitis

# phony rules
.PHONY: makedir
makedir:
	@mkdir -p $(PL_OUTPUT_PATH)
	@mkdir -p $(PS_OUTPUT_PATH)

.PHONY: vivado
vivado:
	$(eval HDL_SRC_PATH_REL:=$(shell realpath --relative-to $(PL_OUTPUT_PATH) $(HDL_SRC_PATH)))
	$(eval SCRIPTS_PATH_REL:=$(shell realpath --relative-to $(PL_OUTPUT_PATH) $(SCRIPTS_PATH)))
	cd $(PL_OUTPUT_PATH); $(VIVADO) -mode batch -source $(SCRIPTS_PATH_REL)/viv_build.tcl -tclargs $(project_name) $(HDL_SRC_PATH_REL)

.PHONY: platform
platform:
	$(eval SW_SRC_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SW_SRC_PATH)))
	$(eval SCRIPTS_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SCRIPTS_PATH)))
	$(eval PL_OUTPUT_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(PL_OUTPUT_PATH)))
	cd $(PS_OUTPUT_PATH); $(VITIS) -s $(SCRIPTS_PATH_REL)/vitis_pform.py $(project_name) $(SW_SRC_PATH_REL) $(PL_OUTPUT_PATH_REL)

.PHONY: app
app:
	$(eval SW_SRC_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SW_SRC_PATH)))
	$(eval SCRIPTS_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SCRIPTS_PATH)))
	$(eval PL_OUTPUT_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(PL_OUTPUT_PATH)))
	cd $(PS_OUTPUT_PATH); $(VITIS) -s $(SCRIPTS_PATH_REL)/vitis_app.py $(SW_SRC_PATH_REL)

.PHONY: build
build: clean makedir vivado platform app

.PHONY: clean
clean:
	@rm -rf $(PL_OUTPUT_PATH) $(PS_OUTPUT_PATH) $(SW_SRC_PATH)/__pycache__/


.PHONY: vitis_clean
vitis_clean:
	@rm -rf $(PS_OUTPUT_PATH) $(SW_SRC_PATH)/__pycache__/

.PHONY: vitis_xsdb
vitis_xsdb:
	$(eval SCRIPTS_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SCRIPTS_PATH)))
	cd $(PS_OUTPUT_PATH); $(VITIS) -s $(SCRIPTS_PATH_REL)/vitis_xsdb.py $(HW_SERVER)
	# killall hw_server
	 taskkill /IM hw_server.exe /F
