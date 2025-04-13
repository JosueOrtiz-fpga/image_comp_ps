# tool macros
VIVADO := /tools/Xilinx/Vivado/2024.1/bin/vivado
VITIS := /tools/Xilinx/Vitis/2024.1/bin/vitis

project_name := image_comp_ps

# path macros
HDL_SRC_PATH := ../../hdl
SW_SRC_PATH := ../../../sw
XSA_FILE := "../"$(project_name)".xsa"



# # compile macros
# TARGET_NAME := main
# ifeq ($(OS),Windows_NT)
# 	TARGET_NAME := $(addsuffix .exe,$(TARGET_NAME))
# endif
# TARGET := $(BIN_PATH)/$(TARGET_NAME)
# TARGET_DEBUG := $(DBG_PATH)/$(TARGET_NAME)

# # src files & obj files
# SRC := $(foreach x, $(SRC_PATH), $(wildcard $(addprefix $(x)/*,.c*)))
# OBJ := $(addprefix $(OBJ_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))
# OBJ_DEBUG := $(addprefix $(DBG_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))

# # clean files list
# DISTCLEAN_LIST := $(OBJ) \
#                   $(OBJ_DEBUG)
# CLEAN_LIST := $(TARGET) \
# 			  $(TARGET_DEBUG) \
# 			  $(DISTCLEAN_LIST)

# default rule
default: clean makedir vivado vitis

# builder-build :
# 	docker build -f builder.Dockerfile -t $(project_name)-builder:latest .

# builder-run :
# 	docker run \
# 		--rm \
# 		-it \
# 		--platform linux/amd64 \
# 		--workdir /builder/mnt \
# 		-v ${PWD}:/builder/mnt \
# 		$(project_name)-builder:latest \
# 		/bin/bash


# # non-phony targets
# $(TARGET): $(OBJ)
# 	$(CXX) $(CXXFLAGS) -o $@ $(OBJ)

# $(OBJ_PATH)/%.o: $(SRC_PATH)/%.c*
# 	$(CXX) $(CCOBJFLAGS) -o $@ $<

# $(DBG_PATH)/%.o: $(SRC_PATH)/%.c*
# 	$(CXX) $(CCOBJFLAGS) $(DBGFLAGS) -o $@ $<

# $(TARGET_DEBUG): $(OBJ_DEBUG)
# 	$(CXX) $(CXXFLAGS) $(DBGFLAGS) $(OBJ_DEBUG) -o $@

# phony rules
.PHONY: makedir
makedir:
	@mkdir -p $(project_name)
	@mkdir -p $(project_name)/$(project_name)".sw"

.PHONY: vivado
vivado:
	cd $(project_name); $(VIVADO) -mode batch -source ../viv_build.tcl -tclargs $(HDL_SRC_PATH)

.PHONY: vitis
vitis:
	cd $(project_name)/$(project_name)".sw"; $(VITIS) -s ../../vitis_build.py $(SW_SRC_PATH) $(XSA_FILE)

# .PHONY: debug
# debug: $(TARGET_DEBUG)

.PHONY: clean
clean:
	@rm -rf $(project_name) $(project_name)/$(project_name)".sw"

.PHONY: vitis_clean
vitis_clean:
	@rm -rf $(project_name)/$(project_name)".sw"
	@mkdir $(project_name)/$(project_name)".sw"
	@cd $(project_name)/$(project_name)".sw"; rm -rf $(SW_SRC_PATH)/__pycache__/

# .PHONY: distclean
# distclean:
# 	@echo CLEAN $(CLEAN_LIST)
# 	@rm -f $(DISTCLEAN_LIST)
