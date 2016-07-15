'''Flexible script for creating grid search command lines.

grid_search_cc.py [Parameter and commandline file] [ARFF file] [] [path to output directory]

The command line file will be of the following format:
	
	desc#[Classifier/run description]
	x1 x2 x3 ... xn
	y1 y2 ... ym
	 :  :  :   :
	k1 k2 ... kp
	command#[Command line with %s in each location that needs a parameter]
	
...and can optionally stack multiple classifier/run types one after the other, e.g.:
	
	desc#[...]
	[Space-delimited parameter lines]
	command#[...]
	desc#[...]
	[Space-delimited parameter lines]
	command#[...]

The #desc line will provide a base character string for output files. Each row 
should is a space delimited list of all values you want for one parameter. You 
can have an arbitray number of possible values, and an arbitrary number of 
parameters. The rows should be in the order that they will be plugged into the 
command line.

The command line row should always start with "command#"
'''

import sys
import os
import itertools

print'''
Inputs:
	1 - Command file
	2 - ARFF file
	3 - .runcc name stump
	4 - Output directory
'''

def row2list(row):
	'''Converts space-delimited lines to lists.
	
	Used to pull out parameters that you are grid searching.
	'''
	l = []
	for i in row.strip().split(' '):
		l.append(i)
	return l

def create_cost_matricies(low, high, by, name):
	'''Creates 2x2 cost matricies through combinations from low to high.
	
	Only changes weights in top-right and bottom-left. Also includes 1, 1.
	'''
	weight_values = range(int(low), int(high)+1, int(by))
	weight_perm = list(itertools.permutations(weight_values, 2))
	weight_perm.append((1, 1))
	n = 0
	cost_mat_list = []
	for comb in weight_perm:
		n += 1
		out_name = name + "%sTO%s.cost" % comb
		if not os.path.isfile(out_name):
			output = open(out_name, 'w')
			output.write('% Rows\tColumns\n2\t2\n% Matrix elements\n')
			output.write('0.0\t%s\n%s\t0.0' % comb)
			output.close()
		cost_mat_list.append(out_name)
	return cost_mat_list

def parse_commands(par):
	'''Parses the command file that you import
	
	Returns the command line to be used, and the list of tuples of all 
	possible parameter combinations.
	'''	
	row_list = []
	command = None
	description = None
	for row in par:
		if row.startswith("desc#"):
			description = row.strip().split('#')[1]
		elif row.startswith("command"):
			command = row.strip().split('#')[1].replace("ARFF",os.path.abspath(sys.argv[2]))
		elif row.startswith("cost"):
			low, high, by, name = row.strip().split('#')[1].split(',')
			row_list.append(create_cost_matricies(low, high, by, name))
		else:
			row_list.append(row2list(row))
	par_list = list(itertools.product(*row_list))
	if command == None:
		raise NameError("Make sure that you parameter file has a proper \
command line. (Should look like command#java weka. ...)")
	if description == None:
		raise NameError("Make sure that you parameter file has a proper \
description. (Should look like desc#smo)")
	return description, command, par_list

def removeSpacesReturnLst(line):
	line = line.strip()
	while "  " in line:
		line = line.replace("  "," ")
	lineLst = line.split(" ")
	return lineLst

def main():
	
	par = sys.argv[1]
	runcc_stump = sys.argv[3]
	try:
		out_dir = os.path.abspath(sys.argv[4])
	except IndexError:
		out_dir = os.path.abspath(os.curdir)
	par_file = open(par)
	
	commandDict = {}
	for line in par_file:
		if line.startswith("desc#"):
			desc = line.strip().split("#")[1]
			commandDict[desc] = []
		commandDict[desc].append(line)
	
	out_files_name_dict = {}
	output = open('%s/%s.runcc' % (out_dir,runcc_stump), 'w')
	print '%s/%s.runcc' % (out_dir,runcc_stump)
	for desc in commandDict:
		print desc
		description, command, par_list = parse_commands(commandDict[desc])
		n = 0
		for par_tuple in par_list:
			n += 1	
			out_file_name = '%s--%s_oup%s.pred' % (sys.argv[2].split("/")[-1], description, str(n))
			command_line = "module load Weka; " + command % par_tuple + ' > %s/%s\n' % (out_dir, out_file_name)
			out_files_name_dict[out_file_name] = command_line
			output.write(command_line)
	
	failed_output = open('%s/%s.failed.runcc' % (out_dir,runcc_stump), 'w')
	for out_file_name in out_files_name_dict:
		abs_path = out_dir + "/" + out_file_name
		file_present = os.path.isfile(abs_path)
		file_size = None
		if file_present == True:
			file_size = os.path.getsize(abs_path)
		if file_present == False or file_size == 0:
			failed_output.write(out_files_name_dict[out_file_name])
	
	output.close()
	failed_output.close()

if __name__ == "__main__":
	main()

print "Done!"
sys.exit()