cat("
Inputs:
	1 - Directory with .sorted_cv files
	2 - Output name

")
args = commandArgs(TRUE)

wd = args[1]
out_name = paste(wd,args[2],sep="/")
library(ROCR)

# setwd(wd)
dirs = list.files(wd)

end_of_string <- function(x, n){
	substr(x, nchar(x)-n+1, nchar(x))
}

get_aucroc_object <- function(file_name){
	t <- read.table(file_name,header=FALSE,sep="\t")
	ncol = dim(t)[2]
	pred <- prediction(t[,seq(2,ncol,2)],t[,seq(1,ncol,2)])
	auc_obj <- performance(pred, "auc")
	return(auc_obj)
}

get_aucroc_list <- function(auc_obj){
	auc <- auc_obj@y.values
	auc_list <- c()
	for(i in auc){
		auc_list <- c(auc_list,i)}
	return(auc_list)
}

sink(file=out_name)
for(dir_name in dirs){
	# cat(paste(dir_name,"\n",sep=""))
	end_of_dir = end_of_string(dir_name,16)
	# cat(paste(end_of_dir,"\n",sep=""))
	if(end_of_dir == "arff_grid_search"){
		full_sub_dir = paste(wd,dir_name,sep="/")
		sub_files = list.files(full_sub_dir)
		for(file_name in sub_files){
			end_of_file = end_of_string(file_name,9)
			if(end_of_file == "sorted_cv"){
				full_sub_dir_file = paste(full_sub_dir,file_name,sep="/")
				auc_obj <- get_aucroc_object(full_sub_dir_file)
				auc_list <- get_aucroc_list(auc_obj)
				
				meanAUC <- mean(auc_list)
				std_err_meanAUC <- sd(auc_list)/sqrt(length(auc_list))
				
				out_str <- paste(file_name,meanAUC,std_err_meanAUC,"\n",sep="\t")
				cat(out_str)
			}
		}
		
	}
}
sink()
