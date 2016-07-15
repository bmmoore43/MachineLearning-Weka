import sys, os

start_dir = "/mnt/home/john3784/machine_learning/random_subsets/"

oup=open("command_files_randomsubsets_4ARFF.sh" ,"w" )

for file in os.listdir(start_dir):
    if file.startswith( "random-metab-subset"):
        file_name = file.strip().split("_")
        name = file_name[1]+"."+file_name[2]
        print (name)
        path = start_dir
        file1 = start_dir+file
        
        oup.write("python ~lloydjo1/scripts/2_Machine_Learning/1_ARFF/2_ARFF_from_matrix.py %s %s metabolites-%s /mnt/home/john3784/2-specialized_metab_project/machine-learn_matrices/binary_matrix-domain_matrix.txt,binary /mnt/home/john3784/2-specialized_metab_project/machine-learn_matrices/continuous_matrix_added-features.txt,numeric\n" %(file1, name, name))
