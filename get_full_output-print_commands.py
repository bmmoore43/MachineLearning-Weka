
import os,sys

try:
	runcc_file = sys.argv[1]
	target_file_name = sys.argv[2]
except:
	print'''
Load Weka module

Inputs:
	1 - .runcc file
	2 - Full output file
'''
	sys.exit()

inp = open(runcc_file)
for line in inp:
	if target_file_name in line:
		command_line = line.strip().replace("-p 0 -distribution","-i -k")
		# command_line = command_line.replace(target_file_name,target_file_name.replace(".pred",".full_output"))
		command_line = command_line.replace(".pred",".full_output")
		# replace("module load Weka;","").strip()
		# print "Running command line:\n",command_line
		print command_line
		# os.system(command_line)
		# print "\nDone!" 
inp.close()
