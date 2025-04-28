# set PROJ_NAME [lindex $argv 0]
# set BOARD_PART [lindex $argv 1]
set HDL_PATH [lindex $argv 2]
set PL_OUTPUT_PATH [lindex $argv 3]
set PY_PATH [lindex $argv 4]


proc get_hdl_config_param {field_name} {
    # get variables outside this proc scope
    upvar PY_PATH PY_PATH
    upvar HDL_PATH HDL_PATH
    # use the python json parser
    return [exec $PY_PATH -c "import json; f=open('$HDL_PATH/config.json'); print(json.load(f)\['$field_name'\]); f.close()"]
}

proc jsonlist_2_list {json_list} {
    # remove [] characters to avoid treating items as TCL commmands
    set j_list_format [string trim $json_list "\[\]"]
    # convert string to list
    set j_list_split [split $j_list_format ","]
    # remove other characters left over: space and '
    foreach item $j_list_split { lappend result [string trim $item { '}]}
    return $result
}

set PROJ_NAME [get_hdl_config_param "project_name"]
set BOARD_PART [get_hdl_config_param "board_part"]
set HDL_LIST [jsonlist_2_list [get_hdl_config_param "hdl_src"]]

# create_project -force $PROJ_NAME $PL_OUTPUT_PATH
# set_property board_part $BOARD_PART [current_project]

# foreach tcl_file [glob -directory $HDL_PATH *.tcl] {
#     source $tcl_file
# }

# foreach hdl_file [glob -directory $HDL_PATH *.v *.sv *.vhd] {
#     add_files $hdl_file
# }

# update_compile_order -fileset sources_1

# launch_runs impl_1 -to_step write_bitstream -jobs 2
# wait_on_run impl_1
# write_hw_platform -fixed -include_bit -force $PL_OUTPUT_PATH/$PROJ_NAME.xsa


