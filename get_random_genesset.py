# get a random gene set from a list of genes
import sys, os, random

gene_file = open(sys.argv[1], 'r') #gene file with all genes
output = open(sys.argv[2], 'w') #file with random subset of genes

#get your genes

gene_list = []

for line in gene_file:
    if line.startswith('AT1'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    if line.startswith('AT2'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    if line.startswith('AT3'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    if line.startswith('AT4'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    if line.startswith('AT5'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    if line.startswith('ATM'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    if line.startswith('ATC'):
        L = line.strip().split("\t")
        gene = L[0]
        if gene not in gene_list:
                gene_list.append(gene)
        else:
            pass
    else: 
        pass

print (gene_list)
#pick any number of random genes -> or match the number of genes in your pos set
n = 31 # number of genes to draw from negative list

gene_list_random = []

#get random set of negative genes
for i in range(1, n):
    a = random.choice(gene_list)
    gene_list_random.append(a)
    gene_list.remove(a)
    


for gene in gene_list_random:
    output.write(str(gene) + '\n')

output.close() 
