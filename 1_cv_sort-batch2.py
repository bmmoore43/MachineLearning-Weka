import os,sys

print'''
Inputs:
	1 - Directory with .pred files
	2 - Name of positive class
	3 - Name of negative class
	4 - Number of CV folds used in preparation of the .pred files
'''

dir = sys.argv[1] #directory with daughter results directories
pos_class_name = sys.argv[2]
neg_class_name = sys.argv[3]
cv_folds = int(sys.argv[4])

full_dir = os.path.abspath(dir) + "/"

def sort_cv(cv_folds,inp,out,positiveClass,negativeClass):
	outLst = []
	for i in range(0,cv_folds):
		outLst.append([])
	i = 0
	lastInst = 0
	for line in inp:
		if ":" in line:
			
			line = line.strip().replace("+","").replace("*","")
			
			while "  " in line:
				line = line.replace("  "," ")
			
			lineLst = line.split(" ")
			instance,actual,pred,prob = lineLst
			
			yesProb = prob.split(",")[0]
			actual = actual.split(":")[1]
			
			if actual == positiveClass:
				clss = 1
			elif actual == negativeClass:
				clss = 0
			
			if int(instance) > lastInst:
				outLst[i].append([clss,yesProb])
			elif int(instance) < lastInst:
				i += 1
				outLst[i].append([clss,yesProb])
			
			lastInst = int(instance)
	
	for cv_list in outLst:
		cv_list.sort(key=lambda k: (k[1], k[0]), reverse=True)
	
	maxLen = 0
	for list in outLst:
		list.sort(key=lambda k: (k[-1]), reverse=True)
		if len(list) > maxLen:
			maxLen = len(list)
	
	for i in range(0,maxLen-1):
		j = 0
		for list in outLst:
			if j == 0:
				try:
					out.write("%s\t%s" % (list[i][0],list[i][1]))
				except:
					out.write("\t\t")
			else:
				try:
					out.write("\t%s\t%s" % (list[i][0],list[i][1]))
				except:
					out.write("\t\t")
			j += 1
		out.write("\n")

for dir in os.listdir(full_dir):
    if dir.startswith("results"):
        file_dir = full_dir + dir + '/'
        for file in os.listdir(file_dir):
	   if file.endswith(".pred"):
		print "Working on file:",file
		inp = open(file_dir+file)
		out = open(file_dir+file + ".sorted_cv","w")
		sort_cv(cv_folds,inp,out,pos_class_name,neg_class_name)
		inp.close()
		out.close()
