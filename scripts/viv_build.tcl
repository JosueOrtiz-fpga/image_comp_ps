set PROJ_NAME [lindex $argv 0]
set HDL_PATH [lindex $argv 1]
set PL_OUTPUT_PATH [lindex $argv 2]

create_project -force $PROJ_NAME $PL_OUTPUT_PATH
set_property board_part digilentinc.com:cora-z7-07s:part0:1.1 [current_project]

foreach tcl_file [glob -directory $HDL_PATH *.tcl] {
    source $tcl_file
}

foreach hdl_file [glob -directory $HDL_PATH *.v *.sv *.vhd] {
    add_files $hdl_file
}

update_compile_order -fileset sources_1

launch_runs impl_1 -to_step write_bitstream -jobs 2
wait_on_run impl_1
write_hw_platform -fixed -include_bit -force $PL_OUTPUT_PATH/$PROJ_NAME.xsa


