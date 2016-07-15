import os, sys, statistics

start_dir = sys.argv[1]

ranfor_list = []
smo_list = []
RF_se_list = []
smo_se_list = []
RF_file_list = []
smo_file_list = []
for dir in os.listdir(start_dir):
    if dir.startswith("result"):
        dir2 = start_dir + "/" + dir + "/"
        print (dir2)
        for file in os.listdir(dir2):
            print (file)
            if file == "metabolite-aucroc.top":
                path = dir2 + file
                inp=open(path ,"r" )
                for line in inp:
                    L = line.strip().split("\t")
                    run = L[0]
                    #print (run)
                    roc = float(L[1])
                    #print (roc)
                    se = float(L[2])
                    run2 = run.split("--")
                    x = run2[1]
                    #print (x)
                    if x.startswith("ran_for"):
                        #print(run, roc)
                        ranfor_list.append(roc)
                        RF_se_list.append(se)
                        RF_file_list.append(run)
                    elif x.startswith("smo"):
                        #print(run, roc)
                        smo_list.append(roc)
                        smo_se_list.append(se)
                        smo_file_list.append(run)
                    else:
                        pass
                #print (ranfor_list)
                #print (smo_list)
                inp.close()

avg_RF = sum(ranfor_list) / float(len(ranfor_list))
avg_smo = sum(smo_list) / float(len(smo_list))
avg_RF_se = sum(RF_se_list) / float(len(RF_se_list))
avg_smo_se = sum(smo_se_list) / float(len(smo_se_list))


med_RF = statistics.median_high(ranfor_list) #returns the higher of two median values
med_smo = statistics.median_high(smo_list)
i= ranfor_list.index(med_RF)
med_RF_file= RF_file_list[i]
med_RF_se= RF_se_list[i]
j= smo_list.index(med_smo)
med_smo_file= smo_file_list[j]
med_smo_se= smo_se_list[j]

max_RF = max(ranfor_list)
k= ranfor_list.index(max_RF)
max_RF_file= RF_file_list[k]
max_RF_se= RF_se_list[k]
max_smo = max(smo_list)
l= smo_list.index(max_smo)
max_smo_file= smo_file_list[l]
max_smo_se= smo_se_list[l]

min_RF = min(ranfor_list)
m= ranfor_list.index(min_RF)
min_RF_file= RF_file_list[m]
min_RF_se= RF_se_list[m]
min_smo = min(smo_list)
n= smo_list.index(min_smo)
min_smo_file= smo_file_list[n]
min_smo_se= smo_se_list[n]


print ("RF", med_RF, med_RF_file, max_RF, max_RF_file, min_RF, min_RF_file)
print ("SMO", med_smo, med_smo_file, max_smo, max_smo_file, min_smo, min_smo_file)
oup = open("metabolite-aucroc.top.combined.txt", "w")
oup.write("%s\t%s\t%s\n%s\t%s\t%s\n" %(med_RF_file, med_RF, med_RF_se, med_smo_file, med_smo, med_smo_se))
oup.write("%s\t%s\t%s\n%s\t%s\t%s\n" %(max_RF_file, max_RF, max_RF_se, max_smo_file, max_smo, max_smo_se))
oup.write("%s\t%s\t%s\n%s\t%s\t%s\n" %(min_RF_file, min_RF, min_RF_se, min_smo_file, min_smo, min_smo_se))
oup.close()