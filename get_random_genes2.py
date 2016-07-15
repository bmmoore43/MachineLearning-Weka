# get a random negative gene set
import sys, os, random

class_file = open(sys.argv[1], 'r') #class file with all negative genes
output = open(sys.argv[2], 'w') #class file with random subset of negative genes

#get your pos and neg genes

pos_gene_list = []
neg_gene_list = []

for line in class_file:
    if line.startswith('AT'):
        L = line.strip().split("\t")
        gene = L[0]
        cl = L[1]
        if cl == 'no':
            if gene not in neg_gene_list:
                neg_gene_list.append(gene)
        else:
            if gene not in pos_gene_list:
                pos_gene_list.append(gene)


#pick any number of random genes -> or match the number of genes in your pos set
n = len(pos_gene_list) + 1 # number of genes to draw from negative list

output.write("gene" + '\t' + "class" + '\n')
#write genes in pos list
for gene in pos_gene_list:
    output.write(str(gene) + '\t' + 'yes' + '\n')

gene_list = []

#get random set of negative genes
for i in range(1, n):
    a = random.choice(neg_gene_list)
    gene_list.append(a)
    neg_gene_list.remove(a)
    


for gene in gene_list:
    output.write(str(gene) + '\t' + 'no' + '\n')

output.close() 

