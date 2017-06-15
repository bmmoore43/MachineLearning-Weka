# MachineLearning-Weka
machine learning and grid search programs

1. The first thing is to make a classes file. gene, yes (to designated feature) and then gene, no.
Before starting machine learning, you may want to get random subsets of genes (if your negative gene set is way larger than your positive or vice versa)

	get_random_genes2.py
	
for multiple class files with random neg sets use: 

	command_files_getrandom.py
	
to get your command_files_random-neg-gene.sh file:

    	python command_files1.py <classes file> <type (ie. SMvsPM)> 
	Designate the number of random draws that you want in the command file.
	
submit the shell script or use qsub: 

	$sh command_files_random-neg-gene.sh
    	python qsub_hpc.py -f submit -u john3784 -c command_files_random-neg-gene.sh -w 60 -m 9 -n 230

if pos set is bigger than neg set use:
	
	get_random_genes2-rev.py

2. Next get features for each gene. Divide into numeric or binary or categorical and make a matrix for each.

3. Now get arff files using your classes file and features file

		python ~lloydjo1/scripts/2_Machine_Learning/1_ARFF/2_ARFF_from_matrix.py SMvsPMvsOther-	glucosinolate_genes.ML_classes_file.txt metabolite SMvsPM_nogluc binary_matrix_2.0.mod.txt,binary continuous_matrix_2.0.txt,numeric categor_cluster_matrix.txt,categorical 

4. You may need to remove some unwanted charcters in order for your arff file to run:

    	grep '"' -v  metabolites-2ndmetabolites-binary_numeric.arff > metabolites-2ndmetabolites-binary_numeric-mod.arff #removes lines with character
    
    or find and replace:
    
    	sed -e 's/"//g' binary_matrix_2.0.txt > binary_matrix_2.0.mod.txt
    	sed -e 's/NA/?/g' SMvsOther_feat_select-metabolite-binary.arff > SMvsOther_feat_select-metabolite-binary.mod.arff
    
    for special charcters:
    
    	sed -i -e 's/\[//g;s/\]//g' file -> removes [ and ] (edits file in place)

5. Make command file for use in all arff files with this format:
    
    	desc#classifier1_name 1 2 3 4 5 6 command#weka %s command %s line for classifier 1 desc#classifier2_name 1 2 3 command#weka %s command line for classifier 2

    i. example of johnny's command file:

        desc#nb_tree
        0.25 0.5 1 2 3 4
        command#java weka.classifiers.meta.FilteredClassifier -t ARFF -c last -p 0 -distribution -F "weka.filters.supervised.instance.SpreadSubsample -M %s" -W weka.classifiers.trees.NBTree
    
        desc#smo
        0.25 0.5 1 2 3 4
        0.01 0.1 0.5 1 1.5 2.0
        command#java weka.classifiers.meta.FilteredClassifier -t ARFF -c last -p 0 -distribution -F "weka.filters.supervised.instance.SpreadSubsample -M %s" -W weka.classifiers.functions.SMO -- -C %s -M -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0"
    
        desc#j48
        0.25 0.5 1 2 3 4
        0.05 0.15 0.25 0.35 0.45
        command#java weka.classifiers.meta.FilteredClassifier -t ARFF -c last -p 0 -distribution -F "weka.filters.supervised.instance.SpreadSubsample -M %s" -W weka.classifiers.trees.J48 -- -C %s -M 2
    
        desc#logistic
        0.25 0.5 1 2 3 4
        9 5 1 1E-04 1E-08 1E-10
        command#java weka.classifiers.meta.FilteredClassifier -t ARFF -c last -p 0 -distribution -F "weka.filters.supervised.instance.SpreadSubsample -M %s" -W weka.classifiers.functions.Logistic -- -R %s -M -1
    
        desc#naive_bayes
        0.25 0.5 1 2 3 4
        command#java weka.classifiers.meta.FilteredClassifier -t ARFF -c last -p 0 -distribution -F "weka.filters.supervised.instance.SpreadSubsample -M %s" -W weka.classifiers.bayes.NaiveBayes
    
        desc#ran_for
        0.25 0.5 1 2 3 4
        1 2 3 4 5 7 9
        command#java weka.classifiers.meta.FilteredClassifier -t ARFF -c last -p 0 -distribution -F "weka.filters.supervised.instance.SpreadSubsample -M %s" -W weka.classifiers.trees.RandomForest -- -I 100 -K %s -S 1

    ii. OR use simplified example: metabolite.command:
        
        desc#smo
        0.01 0.1 0.5 1 1.5 2.0
        command#java weka.classifiers.functions.SMO -t ARFF -c last -p 0 -distribution -C %s -M -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0"
    
        desc#ran_for
        1 2 3 4 5 7 9
        command#java weka.classifiers.trees.RandomForest -t ARFF -c last -p 0 -distribution -I 100 -K %s -S 1
    
    iii. if many arff files, can run a couple using all parameters, choose the best parameters for these, then run all just on the best parameters

4. Balance ARFF files and generate parameter grid search commands: will create 100 random subsets of neg files, then create a all_bal_grid_searches.runcc to submit to the queue
        
	python /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_1-grid_search_runcc-balanced_arffs.py

        python /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_1-grid_search_runcc-balanced_arffs.py -arff /mnt/home/john3784/2-specialized_metab_project/machine-learn_files/metabolite-SMvsPM_nogluc-binary_numeric_categorical-mod.arff -main_dir /mnt/home/john3784/2-specialized_metab_project/machine-learn_files/arff_files2.0/ -cmd /mnt/home/john3784/2-specialized_metab_project/machine-learn_files/metabolite.command 
	
To loop through multiple arff files run:
	
	python ~john3784/Github/MachineLearning-Weka/command_files_multiarff_gridsearch.py <dir with arff files, including separate output directories labeled as name_results>

submit runcc files

    python ~shius/codes/qsub_hpc.py -f submit -c <runcc file> -w <walltime in min> -m <memory in gigs> -J <job name>
    
    python /mnt/home/john3784/2-specialized_metab_project/qsub_hpc.py  -f submit -u john3784 -c all_bal_grid_searches.runcc -w 239 -m 12 -n 230
	
submit via Johnny's qsub for grouped submissions (typically 20-50 at a time)

	 python /mnt/home/lloydjo1/scripts/qsub_hpc-JL.py -f submit -c metabolite_all.runcc -u john3784 -n 230 -w 239 -m 12 -nc 20

if not all jobs finished, run grid search again, then concatenate the bal_grid_search.failed.runcc files to resubmit as one file. Run with a longer walltime

        cat *arff_grid_search/bal_grid_search.failed.runcc > all_bal_grid_searches.failed.runcc
        
        python /mnt/home/john3784/2-specialized_metab_project/qsub_hpc.py  -f submit -u john3784 -c all_bal_grid_searches.failed.runcc -w 600 -m 12 -n 230

7. Assess grid search performances:

    When the grid search through parameters from step 1 has completed, use this script to calculate the performances (aucroc) of each classifier/parameter set combination
    
        /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_2-performance-balanced_arffs.py
        
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

	flag: -manual_cv

This optional flag will manually cross-validate the balanced ARFF files output a runcc file to generate models from training sets. This is useful to get a score that is associated with each instance in your dataset. Follow steps 3 and 4 below to continue this leg of the pipeline.
This option will output a runcc file containing commands to generate models for the training ARFF files sets that were also created in this step. This file is called all_cv.runcc and will be located in the directory provided by -main_dir.

	flag: -models

This optional flag will output a runcc file to generate the models for the best-performing parameter set for each classifier. This is useful if you wish to apply the learning to a group of unknown instances. Follow steps 3b and 4b below to continue this leg of the pipeline.
This option will output a runcc file containing commands to generate models from teh best-performing parameter sets. This file is called best_models.runcc and will be located in the directory provided by -main_dir.

8. get F measure

  		python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/performance_at_thresholds-pred.py <pred file> <pos class name> <neg class name>
  
       		python /mnt/home/john3784/Github/MachineLearning-Weka/performance_at_thresholds-pred2.py SMvsOther-metabolite-binary_numeric_categorical.mod.balanced49.arff_grid_search/SMvsOther-metabolite-binary_numeric_categorical.mod.balanced49.arff--ran_for--par1.pred  yes no

  for multiple files use: 
  
  	python command_files5.py
  	qsub command_files_fmeasure.sh

  OR use a unix loop: 
  
        for i in *arff_grid_search/*.pred; do echo $i; python /mnt/home/john3784/Github/MachineLearning-Weka/performance_at_thresholds-pred2.py $i yes no; done

9. top performing f measure

  		3-get_top_performing_FM_final.py <dir with results folders with .thresh_perf files>
  	
		python ~john3784/Github/MachineLearning-Weka/3_get_top_performing_FM_final.py /mnt/home/john3784/2-specialized_metab_project/machine-learn_files/arff_files2.0/SMvsOther_arff_files/

10. Get SVM weights for each feature

  		python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/get_full_output-top_file.py <.top file> <.runcc file>
  		python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/get_full_output-top_file.py metabolite-aucroc2.top metabolite_all4.runcc
		
  output: 
  
  		metabolites-2ndmetabolites-binary_numeric-mod2.arff--smo_oup6.full_output

  parse .fulloutput file to get weights:
  
  	python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/weights_from_SMO.py <.full_output SMO file>
 	 python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/weights_from_SMO.py metabolites-2ndmetabolites-binary_numeric-mod2.arff--smo_oup6.full_output
	 
  output:
  
  	metabolites-2ndmetabolites-binary_numeric-mod2.arff--smo_oup6.full_output.weights

11.Look at feature importance to see under or over representation, and if you should flip the signs on weights
  
  Turn the matrix into separate files for each column with this script:
  
  	python ~lloydjo1/Projects/0_side_projects/1_metabolism_gene_predictions/_scripts/matrix2mld.py <matrix file>
  	
Using the script below, create a file for each feature with three rows: row 1 includes the values for a feature for secondary metabolite genes, row 2 has the values for primary metabolite genes, and row 3 has the values for all other genes
  
  	python ~lloydjo1/scripts/pull_out_data_on_files.py <feature file> <output name> y <1-column file with secondary metabolite gene IDs> <1-column file with primary metabolite gene IDs>

This step can be run with a unix loop: 

	for i in *[suffix]; do echo $i; python ~lloydjo1/scripts/pull_out_data_on_files.py $i $i.grouped y <1-column file with secondary metabolity gene IDs> <1-column file with primary metabolite gene IDs>; done

Move the resulting binary and numeric value files (these will be suffixed ".grouped") into separate binary and numeric directories
Load the SciPy module before doing the enrichment testing below

  In the numeric directory, run one of these scripts to either K-S or MWU test each of the grouped files:

  	python ~lloydjo1/scripts/_Batch/mwu_test-batch.py <numeric directory> <output file name> 0 1

-or-

  	python ~lloydjo1/scripts/_Batch/ks_test-batch.py <numeric directory> <output file name> 0 1
  	grep "Rest" -v numeric_feature_importance.ks_test

  In the binary directory, run this script to Fisher's Exact Test each of the grouped files:

  	python ~lloydjo1/scripts/_Batch/fisher_exact-batch.py <binary directory> 0 1 <output name> 0 1
  	grep "Rest" -v binary_features_importance.fisher_test

12. Visualize features via Barplot:
  
  		barplot_features.R with an input of a list of features and their weights (pos or neg)

#applying models to known cv data and get scores:

1. first get run the manually cross validated files (all_cv.runcc) to get scores for your training set:

		python /mnt/home/lloydjo1/scripts/qsub_hpc-JL.py -f submit -c all_cv.runcc -u john3784 -n 230 -w 239 -m 12 -nc 20

	Calculate the fmeasure for each run, and find the highest fmeasure.
	Use the score associated with this f-measure as your cutoff for classifying

2. apply models to cross validated samples 

		python /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_3-apply_manual_cv_models-balanced_arffs.py
		
arguments:

	inp1 = directory with [arff]_grid_search subdirectories

This script will generate a runcc file for applying the manual models of the best parameter
sets for each classifier: output runcc file: main_dir/all_apply_models.runcc

3. associate scores with cross-validated samples #this step requires scikit

		python /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_4-associate_gene_ids-balanced_arffs.py
	
arguments:

	inp1 = directory with [arff]_grid_search subdirectories
	inp2 = file with instance IDs from the original, unbalanced ARFF file

This script will associate yes probability scores with gene IDs for each
balanced, manually CV split file. It will also combine all scores across
files for each ML classifer into one output file.

  output score files: input_dir/model--[classifier]--[parameters].scores
  
4. get F-measure cut off to call threshold on score file -this script does not do balanced data to calc fmeasure

		python ~john3784/Github/MachineLearning-Weka/get_threshold_cutoff.py model--smo--par0.1.all_scores

5. get F-measure for balanced data to call threshold

	first get random pulls from your negative dataset (will output 100 random files for each model)
	
		python get_random_genes_scorefile.py <model .score file>
		
	output:
	
		scores.random_out.1..100 files
		
	now get threshold from random sampling of data:
	
		python performance_at_thresholds-pred2_randomfiles.py <start_dir with random files> <pos class name> <neg class name>

	output:
	
		model_random_thresh_perf.txt
		
	use this file to draw threshold

#use best model to apply to unknown data

1. First you need the best_models.runcc file generated in step 7 (assessing grid search performance)
	
	qsub this file:
	
		python /mnt/home/john3784/2-specialized_metab_project/qsub_hpc.py  -f submit -u john3784 -c best_models.runcc -w 239 -m 12 -n 230
2. use the following script to generate another runcc file to apply best-performing models to an unlabled ARFF file:
	
		/mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_3b-apply_models_to_unlabeled-balanced_arff.py
	
		arguments:
	
		inp1 = directory with arff_grid_search subdirectories (-main_dir in previous steps)
		inp2 = unlabelled ARFF file
		inp3 = output directory

This script will output a runcc files containing commands to apply best-performing models to an ARFF file with unlabeled instances. This file will be called apply_models-unlabeled.runcc and will be located in the directory provided in the first input argument.

		python /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_3b-apply_models_to_unlabeled-balanced_arff.py /mnt/home/john3784/2-specialized_metab_project/machine-learn_files/arff_files2.0/SMvsPM_nogluc_arff_files/ SMvsPM_nogluc-metabolite-binary_numeric_categorical.mod.unlabeled.arff /mnt/home/john3784/2-specialized_metab_project/machine-learn_files/arff_files2.0/SMvsPM_nogluc_arff_files/results/

3. qsub the apply_models-unlabeled.runcc

		python /mnt/home/john3784/2-specialized_metab_project/qsub_hpc.py  -f submit -u john3784 -c apply_models-unlabeled.runcc -w 239 -m 12 -n 230

4. Associate scores with instance identifiers - unlabeled instances

	Once models have completed being applied to test sets, this script will assocaited teh machine learning scores with instance identifiers:
	
		python /mnt/home/lloydjo1/scripts/2_Machine_Learning/machine_learning_pipeline_4b-associate_gene_ids-unlabeled-balanced_arffs.py  
	
	arguments:
	
		inp1 = directory with model_applied.arff prediction files
		inp2 = file with instance IDs from the unlabeled ARFF file

	This script will associate yes probability scores with gene IDs for each
	balanced model. It will also combine all scores across files for each ML classifer into one output file.

  	output score files: input_dir/model--[classifier]--[parameters].scores

5. get F-measure cut off to call threshold on score file

		python ~john3784/Github/MachineLearning-Weka/get_threshold_cutoff.py model--smo--par0.1.all_scores


#A note on Support Vector Machines and feature selection:

  For a general kernel it is difficult to interpret the SVM weights, however for the linear SVM there actually is a useful interpretation:
  1) Recall that in linear SVM, the result is a hyperplane that separates the classes as best as possible. The weights represent this hyperplane, by giving you the coordinates of a vector which is orthogonal to the hyperplane - these are the coefficients given by svm.coef_. Let's call this vector w.
  2) What can we do with this vector? It's direction gives us the predicted class, so if you take the dot product of any point with the vector, you can tell on which side it is: if the dot product is positive, it belongs to the positive class, if it is negative it belongs to the negative class.
  3) Finally, you can even learn something about the importance of each feature. This is my own interpretation so convince yourself first. Let's say the svm would find only one feature useful for separating the data, then the hyperplane would be orthogonal (at a right angle, perpendicular to the point of intersection) to that axis. So, you could say that the absolute size of the coefficient relative to the other ones gives an indication of how important the feature was for the separation. For example if only the first coordinate is used for separation, w will be of the form (x,0) where x is some non zero number and then |x|>0.

#Archived instructions:

1. Make multiple ARFF files with random subsets of negative genes:
    use class files to get multiple ARFF files
    python command_files2.py
    python qsub_hpc.py -f queue -u john3784 -c command_files_randomsubsets_4ARFF.sh -w 120 -m 9 -n 230

2. You may need to get rid of ? in Arff file:
    grep '?,?,?,?,?,?,?,?,?' -v  metabolites-2ndmetabolites-binary_numeric.arff > metabolites-2ndmetabolites-binary_numeric-mod.arff
    use a for loop for multiple arff files:
    for i in *-binary_numeric.arff; do echo $i; grep "?,?,?,?,?,?,?,?,?" -v $i > $i.mod; done
    sometimes you may need to find/replace and you can use unix for this:
    sed s/'{no,yes}'/'{yes,no}'/g metabolites-2ndmetabolites-binary_numeric-mod.arff > test_file_nm

3. make command file

4. use command file to do a gridsearch with arff file
  python ~lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc3.py <command file> <ARFF file> <output name prefix> <output dir for machine learning results>
  python ~lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc3.py metabolite.command2 metabolites-2ndmetabolites-binary_numeric-mod.arff metabolite_all /mnt/home/john3784/Documents/machine_learning/

5. for multiple arff files:
  python command_files3.py
  python qsub_hpc.py -f submit -u john3784 -c command_files_gridsearch_ARFF.sh -w 120 -m 9 -n 230

6. parse prediction files - Use pred files to get cross-validation file
  each column represents a pair: actual class, predicted class for the test data set (how well does your model work on test data?)
    
    python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/1_cv_sort-batch.py <dir with .pred files> <pos class name> <neg class name> <cross-validation folds in run>
  
    python 1_cv_sort-batch.py /mnt/home/john3784/Documents/machine_learning/ yes no 10

  For multiple files within multiple folders labeled 'results':
  python 1_cv_sort-batch2.py /mnt/home/john3784/Documents/machine_learning yes no 10
  
7. get AUC-ROC from sorted-cv files
  R --vanilla --slave --args <dir with .sorted_cv files> <output name> < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/2_aucroc_calc-batch.R
  R --vanilla --slave --args /mnt/home/john3784/Documents/machine_learning/ metabolite-aucroc < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/2_aucroc_calc-batch.R

  for multiple directories use a command file:
  python command_files4.py
  python qsub_hpc.py -f submit -u john3784 -c command_files_qsub_auc-roc.sh -w 40 -m 4 -n 230

8. get the best performing run for each classifier
  python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/3_get_top_performing.py <auc-roc file>
  python 3_get_top_performing.py metabolite-aucroc
  for multiple directories that have auc-roc files:
  python 3_get_top_performing2.py /mnt/home/john3784/Documents/machine_learning/

9. visualize auc-roc
  R --vanilla --slave --args <top aucroc file> <dir with .sorted_cv files> <classifier labels> <SE in legend? y/n> <space around chart? y/n> < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/4_aucroc_and_pr_curves.R
  R --vanilla --slave --args metabolite-aucroc2.top ~john3784/Documents/machine_learning/ RF,SVM,log,NBtree,NB,J48 y y < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/4_aucroc_and_pr_curves.R
