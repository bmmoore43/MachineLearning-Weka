print'''
Inputs:
	1 - directory with directories that contain file with AUC-ROC values
'''
import os,sys



start_dir = sys.argv[1]

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

for dir in os.listdir(start_dir):
    if dir.startswith("results"):
        file_dir = str(start_dir) + str(dir) + '/'
        print file_dir
        for file in os.listdir(file_dir):
	   
	   if file.startswith("metabolite-aucroc"):
                print file
                path = file_dir + file
                inp = open(path)
                dict = {}
                populate_dict(inp,dict)
                print dict

                out = open(path+".top",'w')
                get_top_performing(dict,out)
                inp.close()
                out.close()
