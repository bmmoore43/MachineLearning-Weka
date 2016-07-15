cat("
Inputs:
	1 - Directory with .sorted_cv files
	2 - Output name

")
args = commandArgs(TRUE)

wd = args[1]
out_name = args[2]
library(ROCR)

setwd(wd)
files = list.files()

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
for(file_name in files){
	end_of_file = end_of_string(file_name,9)
	if(end_of_file == "sorted_cv"){
		
		auc_obj <- get_aucroc_object(file_name)
		auc_list <- get_aucroc_list(auc_obj)
		
		meanAUC <- mean(auc_list)
		std_err_meanAUC <- sd(auc_list)/sqrt(length(auc_list))
		
		out_str <- paste(file_name,meanAUC,std_err_meanAUC,"\n",sep="\t")
		cat(out_str)
		
	}
}
sink()
