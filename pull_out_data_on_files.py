print'''
Inputs:
	1 - Data with identifiers in column one and data in the proceeding rows
	2 - Outfile name (.grouped will be added)
	3 - Prioritize lists? y/n
	4 and on - Identifier lists for grouping, prioritized
'''

import os,sys

data_file = sys.argv[1]
# out = open(data_file+".grouped","w")
out_desc = sys.argv[2]
if sys.argv[3] == "y":
	prioritize = True
elif sys.argv[3] == "n":
	prioritize = False
else:
	print "Prioritize command not recognized:",sys.argv[3]
	sys.exit()
id_files_list = sys.argv[4:]

### GET PRIORITIZED LIST OF IDENTIFIERS ###################
def pop_list(file):
	list = []
	inp = open(file)
	header = None
	for line in inp:
		if line.startswith("#"):
			header = line.strip().replace("#","").replace(" ","_")
		else:
			id = line.strip()
			if id not in list:
				list.append(id)
	inp.close()
	return [header,list]

group_header_list = []
full_id_list = []
for file in id_files_list:
	header,id_list = pop_list(file)
	full_id_list.append(id_list)
	group_header_list.append(header)

if prioritize == True:
	prioritized_full_id_list = [full_id_list[0]]
	trumped_list = full_id_list[0]
	for id_list in full_id_list[1:]:
		non_trumped_list = []
		for id in id_list:
			if id not in trumped_list:
				non_trumped_list.append(id)
		trumped_list = trumped_list+id_list
		prioritized_full_id_list.append(non_trumped_list)
	working_list = prioritized_full_id_list[:]
elif prioritize == False:
	working_list = full_id_list[:]

selected_id = []
for id_list in working_list:
	selected_id = selected_id+id_list
working_list.append([])
group_header_list.append("Rest")

	
###########################################################



### PROCESS DATA FILES ####################################

def populate_unselected_list(file,sel_id,w_list):
	inp = open(file)
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			id = lineLst[0]
			if id not in sel_id:
				w_list[-1].append(id)
	inp.close()

def pop_dict(file):
	dict = {}
	inp = open(file)
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			id = lineLst[0]
			value_list = lineLst[1:]
			if id not in dict:
				dict[id] = value_list
			else:
				print id,"appears more than once"
	print len(working_list[-1])
	inp.close()
	return dict

populate_unselected_list(data_file,selected_id,working_list)
value_dict = pop_dict(data_file)

if out_desc.endswith(".grouped"):
	out = open(out_desc,"w")
else:
	out = open(out_desc + ".grouped","w")

i = 0
for id_list in working_list:
	out.write("%s\t" % (group_header_list[i]))	
	for id in id_list:
		if id in value_dict:
			value_list = value_dict[id]
			for value in value_list:
				if value != "NA" and value != "?" and value != "" and value != "None":
					out.write(value + "\t")
	out.write("\n")
	i += 1

out.close()

# def pop_list(file):
	# list = []
	# inp = open(file)
	# header = None
	# for line in inp:
		# if line.startswith("#"):
			# header = line.strip().replace("#","")
		# else:
			# id = line.strip()
			# if id not in list:
				# list.append(id)
	# inp.close()
	# return [header,list]

# group_header_list = []
# full_id_list = []
# for file in id_files_list:
	# header,id_list = pop_list(file)
	# full_id_list.append(id_list)
	# group_header_list.append(header.replace(" ","_"))

# prioritized_full_id_list = [full_id_list[0]]
# trumped_list = [full_id_list[0]]
#i = 0
# for id_list in full_id_list[1:]:
	# non_trumped_list = []
	# for id in id_list:
		# if id not in trumped_list:
			# non_trumped_list.append(id)
	# trumped_list = trumped_list+id_list
#		if id in full_id_list[i]:
#			trumped_id.append(id)
#		elif id not in trumped_id:
#			non_trumped_list.append(id)
#		else:
#			print "trumped earlier"
	# prioritized_full_id_list.append(non_trumped_list)
#	i += 1

# selected_id = []
# for id_list in prioritized_full_id_list:
	# selected_id = selected_id+id_list
# prioritized_full_id_list.append([])
# group_header_list.append("Rest")

# def pop_dict(file):
	# dict = {}
	# inp = open(file)
	# head_list = None
	# for line in inp:
		# if line.startswith("#"):
			# lineLst = line.strip().split("\t")
			# head_list = lineLst[1:]
		# else:
			# lineLst = line.strip().split("\t")
			# id = lineLst[0]
			# if id not in selected_id:
				# prioritized_full_id_list[-1].append(id)
			# value_list = lineLst[1:]
			# with_gene_list = []
			# for value in value_list:
				# combo = id + "," + value
				# with_gene_list.append(combo)
			# if id not in dict:
				# dict[id] = value_list
			# else:
				# print id,"appears more than once"
	# inp.close()
	# return [head_list,dict]

# data_header_list,value_dict = pop_dict(data_file)

# print group_header_list
# print data_header_list

# i = 0
# for id_list in prioritized_full_id_list:
	# cat_len = len(id_list)
	# out.write("%s\t" % (group_header_list[i]))	
	# for id in id_list:
		# if id in value_dict:
			# value_list = value_dict[id]
			# for value in value_list:
				# if not value == "NA":
					# out.write(value + "\t")
	# out.write("\n")
	# i += 1
# out.close()

