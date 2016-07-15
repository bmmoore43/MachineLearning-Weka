print'''
inp1 = pred file
inp2 = positive class name
inp3 = negative class name
'''
import os,sys

pred_file = sys.argv[1]
pos_name = sys.argv[2]
neg_name = sys.argv[3]

def clean_line(ln):
	while "  " in ln:
		ln = ln.replace("  "," ")
	ln = ln.strip()
	return ln

def get_score_list(fl):
	inp = open(fl)
	cs_l = []
	for line in inp:
		if ":" in line:
			cl_line = clean_line(line)
			lineLst = cl_line.split(" ")
			actual = lineLst[1].split(":")[1]
			score = lineLst[-1].replace("*","").split(",")[0]
			cs_l.append([actual,float(score)])
	inp.close()
	cs_l.sort(key=lambda k: (k[1]), reverse=True)
	print cs_l
	return cs_l

def list_split(list):
	i0_l = []
	i1_l = []
	for pair in list:
		i0 = pair[0];i0_l.append(i0)
		i1 = pair[1];i1_l.append(i1)
	return i0_l,i1_l

def get_split_list(yp_l):
	sp_l = []
	for i in range(0,len(yp_l)-1):
		if yp_l[i] != yp_l[i+1]:
			sp_l.append(i+1)
	return sp_l

def populate_counts(list):
	cnt1 = 0.0
	cnt0 = 0.0
	for item in list:
		if item == pos_name:
			cnt1 += 1.0
		elif item == neg_name:
			cnt0 += 1.0
	return cnt1,cnt0

def get_tpfnfptn(class_lst,split_index):
	pred_pos = class_lst[0:split_index]
	pred_neg = class_lst[split_index:]
	tp,fp = populate_counts(pred_pos)
	fn,tn = populate_counts(pred_neg)
	return tp,fn,fp,tn

def calcKappa(tp,fn,fp,tn):
	predictedCorrect = tp+tn
	allPredictions = tp+fn+fp+tn
	class1freq = (tp+fn)/allPredictions
	class2freq = (fp+tn)/allPredictions
	numPredC1 = tp+fp
	numPredC2 = fn+tn
	ranC1cor = numPredC1*class1freq
	ranC2cor = numPredC2*class2freq
	randomCorrect = ranC1cor+ranC2cor
	extraSuccesses = predictedCorrect-randomCorrect
	kappa = extraSuccesses/(allPredictions-randomCorrect)
	return kappa

def perf_at_thresh(fl_nm,split_l,score_l,class_l):
	out = open(fl_nm+".thresh_perf","w")
	out.write("threshold\tkappa\tfm\tprec\trec\n")
	for split_ind in split_l:
		threshold = score_l[split_ind-1]
		print threshold
		tp,fn,fp,tn = get_tpfnfptn(class_l,split_ind)
		
		kappa = calcKappa(tp,fn,fp,tn)
		prec = tp/(tp+fp)
		rec = tp/(tp+fn)
		if prec == 0 and rec == 0:
			fm = "NC"
		else:
			fm = (2*prec*rec)/(prec+rec)
		# print threshold,kappa,fm,prec,rec,tp,fn,fp,tn
		
		out.write("%s\t%s\t%s\t%s\t%s\n"%(threshold,kappa,fm,prec,rec))
	out.close()

class_score_list = get_score_list(pred_file)
class_list,score_list = list_split(class_score_list)
# print class_list,score_list
split_list = get_split_list(score_list)
perf_at_thresh(pred_file,split_list,score_list,class_list)
