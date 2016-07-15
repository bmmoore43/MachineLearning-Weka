import os,sys

if len(sys.argv)==1 or "-h" in sys.argv:
	print'''
Inputs:
	1 - Classes file
	2 - Name of class
	3 - Outname stump
	4 and on - file,type strings

	file,type string: file_name,[binary/numeric/discrete(n)]
'''
	sys.exit()

class_file = sys.argv[1]
class_name = sys.argv[2]
outname_stump = sys.argv[3]
file_type_list = sys.argv[4:]

def make_and_prime_dicts(class_file):
	inp = open(class_file)
	class_dict = {}
	data_dict = {}
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			id,clss = lineLst
			if clss == "NA":
				clss = "?"
			class_dict[id] = clss
			data_dict[id] = []
	inp.close()
	return class_dict,data_dict

def get_header_list(file):
	inp = open(file)
	first_line = inp.readline()
	raw_hdr_list = first_line.strip().split("\t")[1:]
	hdr_list = []
	for item in raw_hdr_list:
		clean = item.replace(" ","_").replace(",","-").replace("/","ovr")
		hdr_list.append(clean)
	inp.close()
	return hdr_list

def get_attributes(file,type,attr_list):
	header_list = get_header_list(file)
	if type == "binary":
		type = "{yes,no}"
	elif "discrete" in type:
		type = "numeric"
	for header in header_list:
		attr_line = "@attribute %s %s" % (header,type)
        	attr_list.append(attr_line)

def add_data(dict,file,type):
	inp = open(file)
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			
			key = lineLst[0]
			if type == "binary":
				val_str = "\t".join(lineLst[1:])
				val_str = val_str.replace("1","yes").replace("0","no")
				val = val_str.split("\t")
			else:
				val = lineLst[1:]
			if key in dict:
				dict[key] = dict[key]+val
	inp.close()

def get_max_len(dict):
	maximum = 0
	for key in dict:
			if len(dict[key]) > maximum:
					maximum = len(dict[key])
	return maximum

def fill_short_list(dict):
	max_len = get_max_len(dict)
	for key in dict:
		vals = dict[key]
		while len(vals) < max_len:
			vals.append("?")

def add_classes(data_dict,class_dict):
	for key in class_dict:
		if key in data_dict:
			clss = class_dict[key]
			if clss == "1":
				clss = "yes"
			elif clss == "0":
				clss = "no"
			data_dict[key].append(clss)

# def add_unknowns(data_dict):
	# unk_dict = {}
	# for key in data_dict:
		# unk_dict[key] = data_dict[key][:]
		# unk_dict[key].append("?")
	# return unk_dict

# def write_output(relation,relation_str,attr_list,data_dict,unk_dict):
def write_output(relation,relation_str,attr_list,data_dict):
	out1 = open(relation+".arff","w")
	#out3 = open(relation+".unlabeled.arff","w")
	out1.write(relation_str + "\n\n")
	#out3.write(relation_str + "\n\n")
	out2 = open(relation+".arff.instanceIDs","w")
	for attr in attr_list:
		out1.write(attr + "\n")
		# out3.write(attr + "\n")
	out1.write("\n")
	out1.write("@data\n")
	#out3.write("\n")
	#out3.write("@data\n")
	i = 1
	for key in data_dict:
		data_list = data_dict[key]
		data_str = ",".join(data_list)
		out1.write(data_str+"\n")
		out2.write("%s\t%s\n" % (i,key))
		i += 1
	# for key in unk_dict:
		# data_list = unk_dict[key]
		# data_str = ",".join(data_list)
		# out3.write(data_str+"\n")
		# i += 1
	out1.close()
	out2.close()

class_dict,data_dict = make_and_prime_dicts(class_file)
attribute_list = []
relation_list = []

type_set = set()
for file_type_pair in file_type_list:
	file,type = file_type_pair.split(",")
	relation_list.append(file)
	type_set.add(type)
	get_attributes(file,type,attribute_list)
	add_data(data_dict,file,type)
	fill_short_list(data_dict)

attribute_list.append("@attribute %s {yes,no}" % class_name)
add_classes(data_dict,class_dict)
fill_short_list(data_dict)
# unk_dict = add_unknowns(data_dict)

type_string = "_".join(type_set)
relation = outname_stump+"-"+class_name + "-" + type_string
relation_string = "@relation "+relation
print relation_string

# write_output(relation,relation_string,attribute_list,data_dict,unk_dict)
write_output(relation,relation_string,attribute_list,data_dict)
