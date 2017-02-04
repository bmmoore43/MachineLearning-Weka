
#import modules
import sys
import os

def print_help():
	print'''
required args:
  -main_dir = directory with [arff]_grid_search subdirectories
  -cmd = machine learning command file used in previous step

default args:
  -cv = No. of CV folds, default = 10
  -pos = Name of positive class, default = yes
  -neg = Name of positive class, default = no

optional args:
  -manual_cv
  -models

This script will calculate the median AUC-ROC across the 100 (default) balanced
Weka runs for each parameter set.
  outputs:
  main_dir/all_aucroc - aucroc values for all classifier/parameter sets for 
			each balanced run
  main_dir/all_aucroc.all_med - median aucroc for each classifier/parameter set
  main_dir/all_aucroc.top_med - median aucroc of best parameter set for each 
				classifier

Optional arguments:
  -manual_cv  Manually cross-validation split the balanced ARFF files and
	      generate a runcc file for making models of the training data
	      using the best parameter sets for each classifer.
	manual cv runcc file output: main_dir/all_cv.runcc

  -models  Output a runcc command file to generate model for each balanced
	   dataset using the best-performing parameter set for each classifier.
	models runcc file output: main_dir/best_models.runcc
'''

def parse_args(argv_l):
	#set defaults
	cv = 10
	ps = "yes"
	ng = "no"
	mn_cv = False
	mdl = False
	for i in range(0,len(argv_l)):
		if argv_l[i] == "-main_dir":
			dr = argv_l[i+1]
		elif argv_l[i] == "-cmd":
			cmd = os.path.abspath(argv_l[i+1])
		elif argv_l[i] == "-cv":
			cv = argv_l[i+1]
		elif argv_l[i] == "-pos":
			ps = argv_l[i+1]
		elif argv_l[i] == "-neg":
			ng = argv_l[i+1]
		elif argv_l[i] == "-manual_cv":
			mn_cv = True
		elif argv_l[i] == "-models":
			mdl = True
		elif argv_l[i].startswith("-"):
			print "Flag not recognized:",argv_l[i]
			print "Quitting"
			sys.exit()
	return dr,cmd,cv,ps,ng,mn_cv,mdl

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		main_dir_raw,cmd_file,cv_folds,pos_nm,neg_nm,manual_cv,models = parse_args(sys.argv)
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	main_dir = os.path.abspath(main_dir_raw)
	os.chdir(main_dir)
	print "\nCV sorting pred files"
	os.system("for i in *arff_grid_search; do python /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/1_cv_sort-batch.py $i %s %s %s; done"%(pos_nm,neg_nm,cv_folds))
	print "\nCalculating AUC-ROC"
	os.system("R --vanilla --slave --args . all_aucroc < /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/2_aucroc_calc-batch-balanced.R")
	os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/balanced-median_aucroc.py all_aucroc")
	os.system("R --vanilla --slave --args all_aucroc.top_med.single_files n < /mnt/home/lloydjo1/scripts/2_Machine_Learning/3_Performance/4_aucroc_and_pr_curves-full_path.R")
	if manual_cv == True or models == True:
		"\nConverting command file to generate models from best parameter sets"
		os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/convert_command_file-add_model.py %s all_aucroc.top_med ."%(cmd_file))
		cmd_file_nm = cmd_file.split("/")[-1]
	if manual_cv == True:
		print "\nGenerating cross-validation ARFF files and dirs"
		os.system("for i in *balanced*arff; do mkdir $i\_cv_split; python /mnt/home/lloydjo1/scripts/2_Machine_Learning/1_ARFF/arff_cv_split.py $i $i.instanceIDs %s; mv *test.arff* $i\_cv_split; mv *train.arff* $i\_cv_split; done"%(cv_folds))
		print "\nWriting manual CV search commands"
		os.system("for i in *arff_cv_split; do python /mnt/home/lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc-manual_cv.py %s/%s.create_model $i; done"%(main_dir,cmd_file_nm))
		os.system("cat *arff_cv_split/cv_grid_search.runcc > all_cv.runcc")
	if models == True:
		print "\nWriting best-model generation commands"
		os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc-balanced_models.py %s/%s.create_model ."%(main_dir,cmd_file_nm))

if __name__ == "__main__":
	main()
