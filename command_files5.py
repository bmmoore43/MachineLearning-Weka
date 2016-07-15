import sys, os

start_dir = "/mnt/home/john3784/Documents/machine_learning/"

oup=open("command_files_fmeasure.sh" ,"w" )

for dir in os.listdir(start_dir):
    if dir.startswith("results"):
        print dir
        path = str(start_dir) + str(dir) +"/" 
        for file in os.listdir(path):
            if file.endswith("pred"):
                file_path = path + str(file)      
                oup.write("python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/performance_at_thresholds-pred.py %s yes no \n" %(file_path))
