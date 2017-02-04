print'''
Load SciPy module

Inputs:
	1 - Directory with files for testing
		Script assumes they are '.grouped' files
	2 - Group name 1
	3 - Group name 2
	4 - Outfile name
	5 - Column with identifiers (index 0)
	6 - Index to start values lists on (index 0)
'''

import os,sys,scipy
from fisher import pvalue

dir = os.path.abspath(sys.argv[1])
name1 = sys.argv[2]
name2 = sys.argv[3]
out_name = sys.argv[4]
id_ind = int(sys.argv[5])
val_ind = int(sys.argv[6])

def fisher(file,id_ind,val_ind,nm1,nm2,outfile):
	inp = open(file)

	id_list = []
	all_list = []
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			id = lineLst[id_ind]
			id_list.append(id)
			values = lineLst[val_ind:]
			all_list.append(values)
	
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

	def get_counts(list,nm1,nm2):
		cnt1 = 0
		cnt0 = 0
		for item in list:
			if item == nm1:
				cnt1 += 1
			elif item == nm2:
				cnt0 += 1
		p = round((float(cnt1)/(float(cnt1)+float(cnt0)))*100,1)
		return cnt1,cnt0,p

	
	for combo in combo_list:
		ind1 = combo[0]-1
		ind2 = combo[1]-1
		l1 = all_list[ind1]
		l2 = all_list[ind2]
		cnt11,cnt10,per1 = get_counts(l1,nm1,nm2)
		cnt01,cnt00,per0 = get_counts(l2,nm1,nm2)
		# odds_ratio,p_val = stats.fisher_exact([[cnt11,cnt10],[cnt01,cnt00]])
		print file
		print cnt11,cnt10,per1
		print cnt01,cnt00,per0
		p_val = pvalue(cnt11,cnt10,cnt01,cnt00)
		# out.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (id_list[ind1],id_list[ind2],p_val,odds_ratio,freq1,freq0))
		outfile.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (file.split("/")[-1],id_list[ind1],id_list[ind2],p_val.two_tail,per1,per0))

	inp.close()

def get_files_list(d):
	l = []
	for f in os.listdir(d):
		if f.endswith(".grouped"):
			l.append(d+"/"+f)
	return l

files_list = get_files_list(dir)
if out_name.endswith("fisher_test"):
	out = open(out_name,"w")
else:
	out = open(out_name + ".fisher_test","w")
out.write("#file\tcomp1\tcomp2\tp-val\tper1\tper2\n")
for file in files_list:
	fisher(file,id_ind,val_ind,name1,name2,out)
