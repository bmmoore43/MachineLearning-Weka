print'''
Inputs:
	1 - File with AUC-ROC values
'''
import os,sys

file = sys.argv[1]

def populate_dict(inp,dict):
	for line in inp:
		run_type = line.split("_ou")[0]
		if run_type not in dict:
			dict[run_type] = []
		lineLst = line.strip().split("\t")
		filename,aucroc,var = lineLst
		dict[run_type].append([filename,float(aucroc),var])

def make_string_list(list):
	str_list = []
	for item in list:
		str_list.append(str(item))
	return(str_list)

def get_top_performing(dict,out):
	best_runs = []
	for run_type in dict:
		type_list = dict[run_type]
		type_list.sort(key=lambda k: (k[1]), reverse=True)
		best_runs.append(type_list[0])
	best_runs.sort(key=lambda k: (k[1]), reverse=True)
	for best_run in best_runs:
		out_str = "\t".join(make_string_list(best_run))
		out.write(out_str + "\n")

inp = open(file)
dict = {}
populate_dict(inp,dict)
inp.close()

out = open(file+".top",'w')
get_top_performing(dict,out)
out.close()
