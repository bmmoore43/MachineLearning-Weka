# MachineLearning-Weka
machine learning and grid search programs
Machine learning (Johnny's pipeline)

The first thing is to make a classes file. gene, yes (to designated feature) and then gene, no.

Before starting machine learning, you may want to get random subsets of genes (if your negative gene set is way larger than your positive or vice versa)

use: get_random_genes2.py

#for multiple class files with random neg sets use: command_files_getrandom.py
#to get your command_files_random-neg-gene.sh file. In the command_files1.py script: the input is your classes file and the type you are comparing (ie. SMvsPM). Designate the number of random draws that you want in the command file.

submit the shell script: $sh command_files_random-neg-gene.sh

or use qsub: python qsub_hpc.py -f submit -u john3784 -c command_files_random-neg-gene.sh -w 60 -m 9 -n 230

#if pos set is bigger than neg set use:
get_random_genes2-rev.py

1. python ~lloydjo1/scripts/2_Machine_Learning/1_ARFF/2_ARFF_from_matrix.py /mnt/home/john3784/Documents/machine_learning/classes_metabolites.txt 2ndmetabolites metabolites /mnt/home/john3784/Documents/machine_learning/lethal8_binary-w_greencut.matrix,binary /mnt/home/john3784/Documents/machine_learning/lethal8_continuous.matrix.c_norm,numeric

2. Make multiple ARFF files with random subsets of negative genes:
# use class files to get multiple ARFF files
python command_files2.py
python qsub_hpc.py -f queue -u john3784 -c command_files_randomsubsets_4ARFF.sh -w 120 -m 9 -n 230

Need to get rid of ? in Arff file

grep '?,?,?,?,?,?,?,?,?' -v  metabolites-2ndmetabolites-binary_numeric.arff > metabolites-2ndmetabolites-binary_numeric-mod.arff

#use a for loop for multiple arff files
for i in *-binary_numeric.arff; do echo $i; grep "?,?,?,?,?,?,?,?,?" -v $i > $i.mod; done


sometimes you may need to find/replace and you can use unix for this:
sed s/'{no,yes}'/'{yes,no}'/g metabolites-2ndmetabolites-binary_numeric-mod.arff > test_file_nm

3. Make command file using all arff files with this format:
desc#classifier1_name 1 2 3 4 5 6 command#weka %s command %s line for classifier 1 desc#classifier2_name 1 2 3 command#weka %s command line for classifier 2

johnny's command file:
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

#use simplified metabolite.command

4. use command file to do a gridsearch with arff file

python ~lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc3.py <command file> <ARFF file> <output name prefix> <output dir for machine learning results>

python ~lloydjo1/scripts/2_Machine_Learning/2_Grid_Search/grid_search_cc3.py metabolite.command2 metabolites-2ndmetabolites-binary_numeric-mod.arff metabolite_all /mnt/home/john3784/Documents/machine_learning/


5. for multiple arff files:
python command_files3.py
python qsub_hpc.py -f submit -u john3784 -c command_files_gridsearch_ARFF.sh -w 120 -m 9 -n 230

6. submit runcc files
python ~shius/codes/qsub_hpc.py -f submit -c <runcc file> -w <walltime in min> -m <memory in gigs> -J <job name>

7. multiple runcc files: make master file in unix
cat results*/metabolites*2nd.runcc > metabolite_all.runcc

8. qsub master file
python qsub_hpc.py -f submit -u john3784 -c metabolite_all.runcc -w 240 -m 12 -n 230

9. parse prediction files - Use pred files to get cross-validation file
each column represents a pair: actual class, predicted class for the test data set (how well does your model work on test data?)

python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/1_cv_sort-batch.py <dir with .pred files> <pos class name> <neg class name> <cross-validation folds in run

python 1_cv_sort-batch.py /mnt/home/john3784/Documents/machine_learning/ yes no 10

For multiple files within multiple folders labeled 'results':
python 1_cv_sort-batch2.py /mnt/home/john3784/Documents/machine_learning yes no 10

10. get AUC-ROC from sorted-cv files

R --vanilla --slave --args <dir with .sorted_cv files> <output name> < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/2_aucroc_calc-batch.R

R --vanilla --slave --args /mnt/home/john3784/Documents/machine_learning/ metabolite-aucroc < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/2_aucroc_calc-batch.R


for multiple directories use a command file
python command_files4.py

python qsub_hpc.py -f submit -u john3784 -c command_files_qsub_auc-roc.sh -w 40 -m 4 -n 230


11. get the best performing run for each classifier
python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/3_get_top_performing.py <auc-roc file>

python 3_get_top_performing.py metabolite-aucroc

for multiple directories that have auc-roc files:

python 3_get_top_performing2.py /mnt/home/john3784/Documents/machine_learning/

11. visualize auc-roc

R --vanilla --slave --args <top aucroc file> <dir with .sorted_cv files> <classifier labels> <SE in legend? y/n> <space around chart? y/n> < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/4_aucroc_and_pr_curves.R
R --vanilla --slave --args metabolite-aucroc2.top ~john3784/Documents/machine_learning/ RF,SVM,log,NBtree,NB,J48 y y < ~lloydjo1/scripts/2_Machine_Learning/3_Performance/4_aucroc_and_pr_curves.R


12. get F measure						
python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/performance_at_thresholds-pred.py <pred file> <pos class name> <neg class name>

python performance_at_thresholds-pred2.py metabolites-2ndmetabolites-binary_numeric-mod2.arff--ran_for_oup7.pred yes no

for multiple files
use python command_files5.py

qsub command_files_fmeasure.sh

OR use a unix loop: 
for i in results*/*.pred; do echo $i; python ~john3784/machine_learning/performance_at_thresholds-pred2.py $i yes no; done

13. top performing f measure
3-get_top_performing_FM.py <dir with results folders with .thresh_perf files>
python 3_get_top_performing_FM.py /mnt/home/john3784/machine_learning/arff_files/SMvsOther/

14. Get SVM weights for each feature
python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/get_full_output-top_file.py <.top file> <.runcc file>

python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/get_full_output-top_file.py metabolite-aucroc2.top metabolite_all4.runcc

less metabolites-2ndmetabolites-binary_numeric-mod2.arff--smo_oup6.full_output

parse .fulloutput file to get weights:
python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/weights_from_SMO.py <.full_output SMO file>

python ~lloydjo1/scripts/2_Machine_Learning/3_Performance/weights_from_SMO.py metabolites-2ndmetabolites-binary_numeric-mod2.arff--smo_oup6.full_output

less metabolites-2ndmetabolites-binary_numeric-mod2.arff--smo_oup6.full_output.weights

For looking at feature importance to see under or over representation, and if you should flip the signs on weights

Turn the matrix into separate files for each column with this script:
python ~lloydjo1/Projects/0_side_projects/1_metabolism_gene_predictions/_scripts/matrix2mld.py <matrix file>
python ~lloydjo1/Projects/0_side_projects/1_metabolism_gene_predictions/_scripts/matrix2mld.py lethal8_binary-w_greencut.matrix
python ~lloydjo1/Projects/0_side_projects/1_metabolism_gene_predictions/_scripts/matrix2mld.py lethal8_continuous.matrix.c_norm
Using the script below, create a file for each feature with three rows: row 1 includes the values for a feature for secondary metabolite genes, row 2 has the values for primary metabolite genes, and row 3 has the values for all other genes
python ~lloydjo1/scripts/pull_out_data_on_files.py <feature file> <output name> y <1-column file with secondary metabolite gene IDs> <1-column file with primary metabolite gene IDs>
  This step can be run with a unix loop: for i in *[suffix]; do echo $i; python ~lloydjo1/scripts/pull_out_data_on_files.py $i $i.grouped y <1-column file with secondary metabolity gene IDs> <1-column file with primary metabolite gene IDs>; done

for i in *[.MLD]; do echo $i; python ~lloydjo1/scripts/pull_out_data_on_files.py $i $i.grouped y secondary_metabolites.txt primary_metabolites.txt; done

Move the resulting binary and numeric value files (these will be suffixed ".grouped") into separate binary and numeric directories
Load the SciPy module before doing the enrichment testing below

In the numeric directory, run one of these scripts to either K-S or MWU test each of the grouped files:

python ~lloydjo1/scripts/_Batch/mwu_test-batch.py <numeric directory> <output file name> 0 1
python ~lloydjo1/scripts/_Batch/mwu_test-batch.py /mnt/home/john3784/Documents/machine_learning/numeric_files/ numeric_feature_importance 0 1
grep "Rest" -v numeric_feature_importance.mwu_test
-or-

python ~lloydjo1/scripts/_Batch/ks_test-batch.py <numeric directory> <output file name> 0 1
python ~lloydjo1/scripts/_Batch/ks_test-batch.py /mnt/home/john3784/Documents/machine_learning/numeric_files/ numeric_feature_importance 0 1
grep "Rest" -v numeric_feature_importance.ks_test

In the binary directory, run this script to Fisher's Exact Test each of the grouped files:

python ~lloydjo1/scripts/_Batch/fisher_exact-batch.py <binary directory> 0 1 <output name> 0 1

python ~lloydjo1/scripts/_Batch/fisher_exact-batch.py /mnt/home/john3784/Documents/machine_learning/binary_files/ 1 0 binary_features_importance 0 1

grep "Rest" -v binary_features_importance.fisher_test

Barplot:

use barplot_features.R with an input of a list of features and their weights (pos or neg)

Support Vector Machine background and feature selection:

For a general kernel it is difficult to interpret the SVM weights, however for the linear SVM there actually is a useful interpretation:
1) Recall that in linear SVM, the result is a hyperplane that separates the classes as best as possible. The weights represent this hyperplane, by giving you the coordinates of a vector which is orthogonal to the hyperplane - these are the coefficients given by svm.coef_. Let's call this vector w.
2) What can we do with this vector? It's direction gives us the predicted class, so if you take the dot product of any point with the vector, you can tell on which side it is: if the dot product is positive, it belongs to the positive class, if it is negative it belongs to the negative class.
3) Finally, you can even learn something about the importance of each feature. This is my own interpretation so convince yourself first. Let's say the svm would find only one feature useful for separating the data, then the hyperplane would be orthogonal (at a right angle, perpendicular to the point of intersection) to that axis. So, you could say that the absolute size of the coefficient relative to the other ones gives an indication of how important the feature was for the separation. For example if only the first coordinate is used for separation, w will be of the form (x,0) where x is some non zero number and then |x|>0.

