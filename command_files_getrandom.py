#takes class file and gets draws from negative genes as subsets. input number of draws and class file
import sys, os

oup=open("command_files_random-neg-gene.sh" ,"w" )

# n =number of draws from neg set + 1
n= 101

#fill in class file
inp= sys.argv[1]
type= sys.argv[2]

for i in range(1, n):        
    oup.write(" python /mnt/home/john3784/machine_learning/get_random_genes2-rev.py /mnt/home/john3784/2-specialized_metab_project/pos-neg_genesets/%s /mnt/home/john3784/machine_learning/random_subsets/random-metab-subset_%s_%s\n" %(inp, type, i))
