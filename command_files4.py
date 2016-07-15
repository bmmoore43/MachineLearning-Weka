import sys, os

start_dir = "/mnt/home/john3784/machine_learning/arff_files/"

oup=open("command_files_qsub_auc-roc.sh" ,"w" )

for dir in os.listdir(start_dir):
    if dir.startswith("results"):
        print dir
        path = str(start_dir) + str(dir) +"/" 
        output = path + 'metabolite-aucroc'      
        oup.write("R --vanilla --slave --args %s %s < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/2_aucroc_calc-batch.R \n" %(path, output))
