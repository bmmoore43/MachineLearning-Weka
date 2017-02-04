# IMPOT
import sys

# MAIN
# Reads a *.cc all_cv commmand file [1] and a list of finished *.pred files [2]
# (i.e completed_files.txt) and filters the commands for the ones you need to rerun

command_lines = open(sys.argv[1],"r").readlines()
#print command_lines[0:9]

finished_files = [l.strip() for l in open(sys.argv[2],"r").readlines()]
#print finished_files[0:9]

keep_commands = [c for c in command_lines if not c.strip().split("> ")[1] in finished_files]

output = open(sys.argv[1] + ".rerun","w")
output.write("".join(keep_commands))
output.close()
