print'''
Inputs:
	1 - directory with directories that contain files with f-measure values
'''
import os,sys, operator, numpy



start_dir = sys.argv[1]

def populate_dict(inp,dict,name):
	for line in inp:
	    if line.startswith("threshold"):
	        pass
	    else:
		run_type = name
		
		lineLst = line.strip().split("\t")
		#threshold,kappa,fm = lineLst[0:3]
		fm = lineLst[2]
		
		if run_type not in dict:
		    dict[run_type] = [float(fm)]
		else:
		    dict[run_type].append(float(fm))

def make_string_list(list):
	str_list = []
	for item in list:
		str_list.append(str(item))
	return(str_list)

def get_top_performing(dict,out):
	best_runs = {}
	for run_type in dict:
	       #print (run_type)
	       type_list = dict[run_type]
	       type_list.sort(reverse=True)
	       best_runs[run_type] = type_list[0]
	       #best_runs.append((run_type, type_list[0]))
	#print (best_runs)
	sorted_bestruns = sorted(best_runs.items(), key=operator.itemgetter(1), reverse=True)
	#best_runs.sort(key=lambda k: (k[1]), reverse=True)
	for best_run in sorted_bestruns:
		out_str = "\t".join(make_string_list(best_run))
		out.write(out_str + "\n")

for dir in os.listdir(start_dir):
    if dir.endswith(".arff_grid_search"):
        file_dir = str(start_dir) + str(dir) + '/'
        #print file_dir
        dict = {}
        for file in os.listdir(file_dir):
	   #print (file)
	   if file.endswith(".thresh_perf"):
                #print (file)
                path = file_dir + file
                inp = open(path)
                #dict = {}
                name = str(file)
                populate_dict(inp,dict,name)
                
                inp.close()

        out = open(file_dir+"Fmeasure.top",'w')
        #print (dict)
        get_top_performing(dict,out)
        out.close()

def get_fmeasure(inp,D):
    for line in inp:
        L= line.strip().split('.arff')
        L2= L[1].split('\t')
        ml_type= L2[0]
        FM= float(L2[1])
        if ml_type not in D:
            D[ml_type]=[FM]
        else:
            D[ml_type].append(FM)

f_dict={}
    
for dir in os.listdir(start_dir):
    #print (dir)
    if dir.endswith(".arff_grid_search"):
        file_dir = str(start_dir) + str(dir) + '/'
        print (file_dir)
        for file in os.listdir(file_dir):
            if file == "Fmeasure.top":
                print (file)
                path = file_dir + file
                print (path)
                inp = open(path, 'r')
                get_fmeasure(inp,f_dict)
                inp.close()

print (f_dict)
file_dir2 = str(start_dir) + "Fmeasure.top_all"
out2= open(file_dir2, 'w')
out2.write('machine-learn_run\tmedian_FM\tmean_FM\tmax_FM\n')
for run in f_dict:
    f_list = f_dict[run]
    f_med = numpy.median(f_list)
    f_mean = numpy.mean(f_list) 
    f_max = max(f_list)  
    out2.write('%s\t%s\t%s\t%s\n' % (run, f_med, f_mean, f_max))
out2.close()         