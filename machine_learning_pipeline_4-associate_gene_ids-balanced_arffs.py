
#import modules
import sys
import os

def print_help():
	print'''
arguments:
inp1 = directory with [arff]_grid_search subdirectories
inp2 = file with instance IDs from the original, unbalanced ARFF file

Module requirement: scikit (module load scikit)

This script will associate yes probability scores with gene IDs for each
balanced, manually CV split file. It will also combine all scores across
files for each ML classifer into one output file.

  output score files: input_dir/model--[classifier]--[parameters].scores
'''

def associate_not_selected_scores(dr):
	# fp_dr = os.path.abspath(dr)
	for fl in os.listdir(dr):
		# print fl
		if "not_selected" in fl:
			if fl.endswith("---model_applied.arff"):
				print fl
				fp_app_fl = dr+"/"+fl
				
				fl_nm_l = fl.split("---")
				orig_arff = fl_nm_l[0]
				instance_ids = orig_arff+".instanceIDs"
				fp_ins_fl = dr+"/"+instance_ids
				
				os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/prediction_score_to_identifiers.py %s %s"%(fp_app_fl,fp_ins_fl))
	

def collect_sorted_cv_for_curves(dr):
	out = open(dr+"/manualcv_files_for_curves","w")
	for fl in os.listdir(dr):
		if fl.startswith("model--"):
			if fl.endswith(".sorted_cv"):
				out.write(dr+"/"+fl+"\n")
	out.close()

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		main_dir_raw = sys.argv[1]
		all_instance_ids_raw = sys.argv[2]
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	main_dir = os.path.abspath(main_dir_raw)
	all_instance_ids = os.path.abspath(all_instance_ids_raw)
	os.chdir(main_dir)
	print "\nAssociating IDs with scores - CV files\n"
	os.system("for i in *cv_split; do echo $i; python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/prediction_score_to_identifiers-batch_wrapper.py $i; done")
	print "\nAssociating IDs with scores - not selected files\n"
	associate_not_selected_scores(main_dir)
	print "\nCombining score from across balanced runs (both selected and not selected instances)\n"
	os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/manual_cv-pred_score2id-combine_batch_scores.py %s %s"%(main_dir,all_instance_ids))
	os.system("for i in model--*scores; do echo $i; python /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/convert_columns_to_sorted_cv.py -i $i; done")
	os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/curves_file-manual_cv.py . manual_cv.curves_data")
	os.system("R --vanilla --slave --args manual_cv.curves_data n < /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/4_aucroc_and_pr_curves-full_path.R")
	collect_sorted_cv_for_curves(main_dir)
	# os.system("ls $PWD/model--*.sorted_cv > manual_cv_files_for_curves")

if __name__ == "__main__":
	main()
