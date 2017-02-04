
#import modules
import sys
import os

def print_help():
	print'''
required arguments:
 -arff = ARFF file
 -main_dir = primary working directory*
 -cmd = WEKA machine learning command file

default arguments:
 -bal = # of balanced ARFF files to generate, default = 100

* Tell the pipeline where to generate 100 (default) balanced ARFF files and 100 corresponding directories

Pipeline will output a runcc file in the main directory called all_bal_grid_searches.runcc in the main directory.
This can be submitted to the MSU HPCC queue using Shinhan's qsub_hpc.py script.
'''

def parse_args(argv_l):
	bal = 100
	for i in range(0,len(argv_l)):
		if argv_l[i] == "-arff":
			arf = os.path.abspath(argv_l[i+1])
		elif argv_l[i] == "-main_dir":
			mn_dr = os.path.abspath(argv_l[i+1])
		elif argv_l[i] == "-cmd":
			cmd = os.path.abspath(argv_l[i+1])
		elif argv_l[i] == "-bal":
			bal = argv_l[i+1]
		elif argv_l[i].startswith("-"):
			print "Flag not recognized:",argv_l[i]
			print "Quitting"
			sys.exit()
	return arf,mn_dr,cmd,bal

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		arff_inp,main_dir,cmd_fl,balance_cnt = parse_args(sys.argv)
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	# CREATE BALANCED ARFF FILES
	print "Creating balanced ARFF files"
	os.system("python /mnt/home/lloydjo1/scripts/2_Machine_Learning/1_ARFF/balance_arff.py %s %s.instanceIDs %s"%(arff_inp,arff_inp,balance_cnt))
	os.system("mv %s.balanced*.arff* %s"%(arff_inp.replace(".arff",""),main_dir))
	os.system("mv %s.not_selected*.arff* %s"%(arff_inp.replace(".arff",""),main_dir))
	
	# PREPARE GRID SEARCH COMMAND FILES
	print "Preparing grid search command files"
	os.chdir(main_dir)
	os.system("for i in *balanced*arff; do echo $i; python /mnt/home/lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_runcc.py %s $i; done"%cmd_fl)
	os.system("cat *grid_search/bal_grid_search.runcc > all_bal_grid_searches.runcc")
	

if __name__ == "__main__":
	main()
