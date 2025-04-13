set PROJ_NAME [lindex $argv 0]
set HDL_PATH [lindex $argv 1]

create_project -part xc7z007sclg400-1 -force $PROJ_NAME
set_property board_part digilentinc.com:cora-z7-07s:part0:1.1 [current_project]

puts "tcl_files: [glob -directory $HDL_PATH *.tcl]"
foreach tcl_file [glob -directory $HDL_PATH *.tcl] {
    source $tcl_file
}

puts "v_files: [glob -directory $HDL_PATH *.v]"
foreach v_file [glob -directory $HDL_PATH *.v] {
    add_files $v_file
}

update_compile_order -fileset sources_1

launch_runs impl_1 -to_step write_bitstream -jobs 2
wait_on_run impl_1
set xsa_file [append "" $PROJ_NAME .xsa]
write_hw_platform -fixed -include_bit -force -file $xsa_file


