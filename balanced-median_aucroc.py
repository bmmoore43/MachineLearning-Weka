
#import modules
import os
import sys
import random

def print_help():
	print'''
inp1 = all aucroc file
'''

def find_main_dir(f):
	fp = os.path.abspath(f)
	fp_dr_l = fp.split("/")[0:-1]
	dr = "/".join(fp_dr_l)
	return dr

def populate_dict(d,lvl1_key,lvl2_key,add_item):
	if lvl1_key not in d:
		d[lvl1_key] = {}
		d[lvl1_key][lvl2_key] = [add_item]
	else:
		if lvl2_key not in d[lvl1_key]:
			d[lvl1_key][lvl2_key] = [add_item]
		else:
			d[lvl1_key][lvl2_key].append(add_item)

def parse_aucroc(fl):
	main_dir = find_main_dir(fl)
	d_auc = {}
	d_bal = {}
	inp = open(fl)
	for line in inp:
		lineLst = line.strip().split("\t")
		
		aucroc = lineLst[1]
		fl_nm_l = lineLst[0].split("--")
		fl_nm = fl_nm_l[0]
		desc = fl_nm_l[1]
		pars = fl_nm_l[2].replace(".pred.sorted_cv","")
		populate_dict(d_auc,desc,pars,float(aucroc))
		
		fl_nm_split = fl_nm.split(".")
		for item in fl_nm_split:
			if item.startswith("balanced"):
				full_path_file = "%s/%s_grid_search/%s"%(main_dir,fl_nm,lineLst[0])
				populate_dict(d_bal,desc,pars,[float(aucroc),lineLst[2],full_path_file])
				break
	
	# print d_bal
	inp.close()
	return d_auc,d_bal
	# return d_auc

def median(l):
	l.sort()
	if len(l) % 2 == 1:
		med_index = int(len(l)/2.0-0.5)
		return l[med_index]
	else:
		i1 = len(l)/2
		i2 = len(l)/2-1
		return (l[i1]+l[i2])/2.0

def median_wVal(l):
	l.sort()
	if len(l) % 2 == 1:
		med_index = int(len(l)/2.0-0.5)
		return l[med_index],[l[med_index]]
	else:
		i1 = len(l)/2
		i2 = len(l)/2-1
		return (l[i1]+l[i2])/2.0,[l[i1],l[i2]]

def calc_median(fl_nm,dct,dct2):
	out_all = open("%s.all_med"%fl_nm,"w")
	top_d = {}
	for desc in dct:
		top_d[desc] = ["NA",0]
		pars_dct = dct[desc]
		for pars in pars_dct:
			aucroc_l = pars_dct[pars]
			med_aucroc = median(aucroc_l)
			out_all.write("%s\t%s\t%s\n"%(desc,pars,med_aucroc))
			if med_aucroc > top_d[desc][1]:
				top_d[desc] = [pars,med_aucroc]
				
	out_all.close()
	
	out_top = open("%s.top_med"%fl_nm,"w")
	out_median_top = open("%s.top_med.single_files"%fl_nm,"w")
	for desc in top_d:
		pars,med_aucroc = top_d[desc]
		out_top.write("%s\t%s\t%s\n"%(desc,pars,med_aucroc))
		
		auc_stdErr_flNm_lists = dct2[desc][pars]
		auc_l = []
		for auc_stdErr_flNm_list in auc_stdErr_flNm_lists:
			auc,stdErr,flNm = auc_stdErr_flNm_list
			auc_l.append(auc)
		
		med_single_auc,raw_median_vals = median_wVal(auc_l)
		# print desc,pars
		# print raw_median_vals
		median_fl = [[0,"",""]]
		
		median_lists = []
		for auc_stdErr_flNm_list in auc_stdErr_flNm_lists:
			auc,stdErr,flNm = auc_stdErr_flNm_list
			if auc in raw_median_vals:
				median_lists.append(auc_stdErr_flNm_list)
				# out_median_top.write("%s\t%s\t%s\n"%(flNm,auc,stdErr))
		ran_chc = random.choice(median_lists)
		out_median_top.write("%s\t%s\t%s\n"%(ran_chc[2],ran_chc[0],ran_chc[1]))
	out_median_top.close()		
	out_top.close()

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		aucrocs = sys.argv[1]
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	aucroc_dict,balance_dict = parse_aucroc(aucrocs)
	calc_median(aucrocs,aucroc_dict,balance_dict)

if __name__ == "__main__":
	main()
