print'''
Load SciPy and NumPy modules

Inputs:
	1 - Directory with data files, data should be in rows
		Script assumes you want to perform K-S testing
		only on files ending in '.grouped'
	2 - Outfile name
	3 - Column with identifiers (index 0)
	4 - Index to start values lists on (index 0)
'''

import os,sys,scipy,numpy
from scipy import stats

dir = os.path.abspath(sys.argv[1])
outfile_name = sys.argv[2]
id_ind = int(sys.argv[3])
val_ind = int(sys.argv[4])


def pairwise_kstest(file,id_ind,val_ind,outfile):
	
	inp = open(file)
	id_list = []
	all_list = []
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			id = lineLst[id_ind]
			id_list.append(id)
			values = lineLst[val_ind:]
			float_list = []
			for value in values:
				try:
					float_list.append(float(value))
				except:
					print value,"unfloatable"
			all_list.append(float_list)
	inp.close()
	
	num_of_sets = len(all_list)
	rnge = range(1,num_of_sets+1)
	combo_list = []
	for i in rnge:
		for j in rnge:
			if i != j:
				current = [i,j]
				reverse = [j,i]
				if current not in combo_list and reverse not in combo_list:
					combo_list.append(current)
	
	for combo in combo_list:
		ind1 = combo[0]-1
		ind2 = combo[1]-1
		m1 = numpy.median(all_list[ind1])
		m2 = numpy.median(all_list[ind2])
		n1 = len(all_list[ind1])
		n2 = len(all_list[ind2])
		pVal = stats.ks_2samp(all_list[ind1],all_list[ind2])
		outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (file.split("/")[-1],id_list[ind1],id_list[ind2],pVal[1],m1,m2,n1,n2))

def get_files_list(directory):
	list = []
	for file in os.listdir(directory):
		if file.endswith(".grouped"):
			list.append(directory+"/"+file)
	return list

if outfile_name.endswith("ks_test"):
	out = open(outfile_name,"w")
else:
	out = open(outfile_name + ".ks_test","w")
out.write("#file\tcat1\tcat2\tp_val\tmed1\tmed2\tn1\tn2\n")
files_list = get_files_list(dir)
for file in files_list:
	print "Working on file:",file
	pairwise_kstest(file,id_ind,val_ind,out)
out.close()
