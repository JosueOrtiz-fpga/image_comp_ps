# tool macros
# VIV_BIN := /tools/Xilinx/Vivado/2024.1/bin
VIV_BIN := /c/AMD/Vivado/2024.1/bin
# VITIS_BIN := /tools/Xilinx/Vitis/2024.1/bin
VITIS_BIN := /c/AMD/Vitis/2024.1/bin

VIVADO := $(VIV_BIN)/vivado
VITIS := $(VITIS_BIN)/vitis
HW_SERVER := $(VIV_BIN)/hw_server

# path macros
HDL_PATH := hdl
SW_SRC_PATH := sw
SCRIPTS_PATH := scripts

PL_OUTPUT_PATH := build/pl/
PS_OUTPUT_PATH := build/ps/

# Project data
PROJECT_NAME := image_comp_ps
BOARD_PART := $(shell python -c "print("Hello")")

# default rule
default: build

# phony rules
.PHONY: makedir
makedir:
	@mkdir -p $(PL_OUTPUT_PATH)
	@mkdir -p $(PS_OUTPUT_PATH)

.PHONY: vivado
vivado:
	@echo $(BOARD_PART)
	$(VIVADO) -mode batch -source $(SCRIPTS_PATH)/viv_build.tcl -tclargs $(PROJECT_NAME) $(HDL_PATH) $(PL_OUTPUT_PATH)
	mv ./$(PL_OUTPUT_PATH)/$(PROJECT_NAME).runs/impl_1/*.bit ./$(PL_OUTPUT_PATH)
	mv *.jou *.log $(PL_OUTPUT_PATH)
.PHONY: vitis
vitis:
	$(VITIS) -s $(SCRIPTS_PATH)/vitis_build.py $(PS_OUTPUT_PATH) $(SW_SRC_PATH) $(PL_OUTPUT_PATH)

.PHONY: build
build: clean makedir vivado vitis

.PHONY: vitis_xsdb
vitis_xsdb:
	$(eval SW_SRC_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SW_SRC_PATH)))
	$(eval SCRIPTS_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(SCRIPTS_PATH)))
	$(eval PL_OUTPUT_PATH_REL:=$(shell realpath --relative-to $(PS_OUTPUT_PATH) $(PL_OUTPUT_PATH)))
	cd $(PS_OUTPUT_PATH); $(VITIS) -s $(SCRIPTS_PATH_REL)/vitis_xsdb.py  $(PROJECT_NAME) $(SW_SRC_PATH_REL) $(PL_OUTPUT_PATH_REL) $(HW_SERVER)													 
	# killall hw_server
	 taskkill /IM hw_server.exe /F

.PHONY: vitis_clean
vitis_clean:
	@rm -rf $(PS_OUTPUT_PATH) $(SW_SRC_PATH)/__pycache__/

.PHONY: clean
clean:
	@rm -rf $(PL_OUTPUT_PATH) $(PS_OUTPUT_PATH)
