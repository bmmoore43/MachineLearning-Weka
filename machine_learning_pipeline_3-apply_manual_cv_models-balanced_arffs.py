
#import modules
import sys
import os

def print_help():
	print'''
arguments:
inp1 = directory with [arff]_grid_search subdirectories

This script will generate a runcc file for applying the manual models of the best parameter
sets for each classifier.
  output runcc file: main_dir/all_apply_models.runcc
'''

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		main_dir = sys.argv[1]
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	os.chdir(main_dir)
	print "\nWriting runcc file for each balanced set"
	os.system("for i in *arff_cv_split; do python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/manual_cv-apply_models.py $i; done")
	os.system("cat *arff_cv_split/apply_models.runcc > all_apply_models.runcc")

if __name__ == "__main__":
	main()
