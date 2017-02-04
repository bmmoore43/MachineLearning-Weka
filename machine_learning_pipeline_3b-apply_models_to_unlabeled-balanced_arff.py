
#import modules
import sys
import os

def print_help():
	print'''
inp1 = directory with arff_grid_search subdirectories (-main_dir in previous steps)
inp2 = unlabelled ARFF file
inp3 = output directory

This will generate a runcc file with command to apply the best models to an
unlabelled ARFF file and to instances that were not selected during the
balancing steps (not selected files are expected to be within the directory
provided in inp1 and should be there if you have been following this pipeline)

output runcc file:
  inp1_dir/apply_models-unlabeled.runcc
'''

def pull_models(head_dr):
	l = []
	fp_head_dr = os.path.abspath(head_dr)
	for dr in os.listdir(fp_head_dr):
		if dr.endswith("arff_grid_search"):
			for fl in os.listdir(fp_head_dr+"/"+dr):
				if fl.endswith(".model"):
					fp_mod = "%s/%s/%s"%(fp_head_dr,dr,fl)
					# print fp_mod
					l.append(fp_mod)
	return l

def pull_not_selected(head_dr):
	d = {}
	fp_head_dr = os.path.abspath(head_dr)
	for fl in os.listdir(fp_head_dr):
		if "not_selected" in fl:
			if fl.endswith(".arff"):
				# ex: feats_500bp2_phenVinter-functional-numeric.not_selected91.arff
				fp_fl = fp_head_dr+"/"+fl
				bal_num = fl.split("not_selected")[-1].replace(".arff","")
				d[bal_num] = [fl,fp_fl]
	return d

def write_prediction_cmds(dr,mdl_l,unlb_arff,out_dir,not_sel_d):
	fp_dr = os.path.abspath(dr)
	out = open("%s/apply_models-unlabeled.runcc"%fp_dr,"w")
	command = "module load Weka; java weka.filters.supervised.attribute.AddClassification -serialized %s -i %s -o %s -c last -distribution"
	for model in mdl_l:
		model_no_path = model.split("/")[-1]
		arff_no_path = unlb_arff.split("/")[-1]
		# out_nm = out_dir+"/"+arff_no_path+"---"+model_no_path+"---model_applied.arff"
		out_nm = "%s/%s---%s---model_applied.arff"%(out_dir,arff_no_path,model_no_path)
		pred_cmd = command%(model,unlb_arff,out_nm)
		out.write(pred_cmd+"\n")
		#ex: feats_500bp2_phenVinter-functional-numeric.balanced6.arff--smo--par2.0.model
		bal_num = model_no_path.split("balanced")[-1].split(".")[0]
		not_sel_fl,not_sel_fl_fp = not_sel_d[bal_num]
		not_sel_out_nm = "%s/%s---%s---model_applied.arff"%(fp_dr,not_sel_fl,model_no_path)
		print dr
		print fp_dr
		print not_sel_out_nm
		not_sel_cmd = command%(model,not_sel_fl_fp,not_sel_out_nm)
		print not_sel_cmd
		print
		out.write(not_sel_cmd+"\n")
	out.close()

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		dir = sys.argv[1]
		unlabeled_arff = os.path.abspath(sys.argv[2])
		output_dir = os.path.abspath(sys.argv[3])
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	models_list = pull_models(dir)
	not_selected_dict = pull_not_selected(dir)
	# test_files_dict,model_files_dict = find_files(dir)
	write_prediction_cmds(dir,models_list,unlabeled_arff,output_dir,not_selected_dict)
	

if __name__ == "__main__":
	main()
