
#import modules
import sys
import os

def print_help():
	print'''
arguments:
inp1 = directory with model_applied.arff prediction files
inp2 = file with instance IDs from the unlabeled ARFF file

This script will associate yes probability scores with gene IDs for each
balanced model. It will also combine all scores across files for each ML
classifer into one output file.

  output score files: input_dir/model--[classifier]--[parameters].scores
'''

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		dir = sys.argv[1]
		instance_ids = os.path.abspath(sys.argv[2])
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	os.chdir(dir)
	print "\nAssociating IDs with scores\n"
	os.system("for i in *model_applied.arff; do python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/prediction_score_to_identifiers.py $i %s; done"%(instance_ids))
	print "\nCombining scores from all balanced runs"
	os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/prediction_score_to_identifiers-combine_batch_scores-unlabeled.py .")
	# os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/4_Predictions/manual_cv-pred_score2id-combine_batch_scores.py %s %s"%(dir,all_instance_ids))

if __name__ == "__main__":
	main()
