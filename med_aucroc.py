import os, sys

start_dir= sys.argv[1]
dict = {}
def populate_dict(inp, dict):
    first_line = inp.readline()
    print first_line
    if first_line == "":
        pass
    else:
        L = first_line.strip().split("\t")
        name = L[0]
        aucroc = L[1]
        #stddev = L[2]
        print aucroc
        #if name.endswith("ran_for_oup"):
        #    print name
        dict[name]=aucroc

        

for dir in os.listdir(start_dir):
    if dir.startswith("results"):
        file_dir = str(start_dir) + str(dir) + '/'
        print file_dir
        for file in os.listdir(file_dir):
	   
	   if file.startswith("metabolite-aucroc.top"):
                print file
                path = file_dir + file
                inp = open(path)
                populate_dict(inp,dict)
                print dict
                inp.close()

aucroc_list = []

def parse_dict(dict, out):
    for name in dict:
        aucroc = dict[name]
        aucroc_list.append(aucroc)
        out.write("%s\t%s\n" % (name, aucroc))
    

    #med = statistics.median(aucroc_list)
    #stddev = statistics.stdev(aucroc_list)
    #aucroc_str = "\t".join(aucroc_list)
    #    
    #out.write("top_auc-rocs" + "\t" + "%s" + "\n" + "median" + "\t" + "%s" + "\n" + "std_dev" + "\t" + "%s" + "\n" % (aucroc_str, med, stddev))

out = open(str(start_dir)+"randomforest-topaucroc_sum",'w')
parse_dict(dict,out)
                
out.close()