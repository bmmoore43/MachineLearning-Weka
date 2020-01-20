def print_help():
	print'''
inp1 = top file
inp2 = runcc file
'''

import os,sys

try:
	top_file = sys.argv[1]
	runcc_file = sys.argv[2]
except:
	print_help()
	sys.exit()

def pull_smo_file_nm(top_fl):
	inp = open(top_fl)
	for line in inp:
		if "--smo_oup" in line:
			lineLst = line.split("\t")
			scv = lineLst[0]
			prd = scv.replace(".sorted_cv","")
	inp.close()
	return prd
	
smo_pred_fl = pull_smo_file_nm(top_file)
print "Running:\npython /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/get_full_output.py %s %s"%(runcc_file,smo_pred_fl)
os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/get_full_output.py %s %s"%(runcc_file,smo_pred_fl))
