# gets fmeasure for each threshold score in a list
import sys, os, fn
inp_file= open(sys.argv[1], 'r')
output = open(str(sys.argv[1])+'.FMbyThresh.txt', 'w')
pos_list=[]
neg_list=[]
pos_gene={}
neg_gene={}
def get_dict(inp, pos_gene, neg_gene, pos_list, neg_list):
    for line in inp:
        L= line.strip().split('\t')
        #print (L)
        gene = L[0]
        cl = L[1]
        if L[2] != 'NA':
            score = float(L[2])
            if cl == "yes":
                pos_list.append(score)
                pos_gene[gene]=score
            elif cl == "no":
                neg_list.append(score)
                neg_gene[gene]=score
            else:
                pass

get_dict(inp_file, pos_gene, neg_gene, pos_list, neg_list)                       
print (pos_list)
print (neg_list)

thresh_dict = fn.calc_performance_for_lists(pos_list,neg_list)
 # returns: dict{[threshold]:[prec,recall,fmeas,kappa]
print (thresh_dict)

output.write("threshold\tprecision\trecall\tFmeas\tkappa\tfnr\tfpr\n")
for thresh in thresh_dict:
    data_list = thresh_dict[thresh]
    data_list2= []
    print (data_list)
    for i in data_list:
        data_list2.append(str(i))
    data_str = '\t'.join(data_list2)
    output.write('%s\t%s\n' %(thresh, data_str))
    
output.close()
inp_file.close()
            