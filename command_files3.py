import sys, os

start_dir = "/mnt/home/john3784/machine_learning/arff_files/"

oup=open("command_files_gridsearch_ARFF.sh" ,"w" )

count = 1
for file in os.listdir(start_dir):
    if file.endswith( "_numeric.arff.mod.arff"):
        file_name = file.strip().split("-")
        name = str(file_name[0]+file_name[2]+"-"+file_name[3])
        print name
        path = str(start_dir) + "results" + str(count) + "/"
        os.mkdir(path) 
        file1 = start_dir+file
        oup.write("python ~lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc3.py /mnt/home/john3784/machine_learning/metabolite.command %s %s %s\n" %(file1, name, path))
        count = count + 1