cat("
Inputs:
	1 - .top file with top AUC-ROC for each run
	2 - Directory with .sorted_cv files
	3 - Labels list, comma-delimited
	4 - Include standard error in legend? y/n
	5 - Include edge around chart area? y/n

")

### FUNCTIONS #######################
clean_up_labels <- function(raw_labels){
	clean_labels <- gsub("_"," ",raw_labels)
	clean_labels <- gsub("###","\n",clean_labels)
	return(clean_labels)
}

split_str <- function(string,char_split,numbers){
	string_split <- strsplit(string,char_split)
	final_list <- c()
	for(i in string_split[[1]]){
		if(numbers == 1){
			final_list <- c(final_list,as.numeric(i))
		}else{
			final_list <- c(final_list,i)
		}
	}
	return(final_list)
}

get_perf_PR <- function(t){
	ncol = dim(t)[2]
	pred <- prediction( t[,seq(2,ncol,2)],t[,seq(1,ncol,2)])
	perf <- performance(pred, "prec", "rec")
}

get_perf_ROC <- function(t){
	ncol = dim(t)[2]
	pred <- prediction( t[,seq(2,ncol,2)],t[,seq(1,ncol,2)])
	perf <- performance(pred, "tpr", "fpr")
	return(perf)
}

create_plot <- function(y_label,x_label){
	if(edge_inc=='n'){
		plot(0,0,lty="blank",type="l",ylim=c(0.0,1.0),ylab=y_label,xlim=c(0.0,1.0),xlab=x_label,xaxs="i",yaxs="i")
	}else{
		plot(0,0,lty="blank",type="l",ylim=c(0.0,1.0),ylab=y_label,xlim=c(0.0,1.0),xlab=x_label)
	}
	grid(lty="dotted",lwd = 1,col="lightgray")
}

add_aucroc_curve <- function(index){
	dataFile <- read.table(file_list[index], header = FALSE, sep="\t")
	color <- backwardsColors[index]
	perf <- get_perf_ROC(dataFile)
	plot(perf, avg='vertical', spread.estimate='stderror', ylim=c(0,1), col = color,lwd=2, add=TRUE)
}

get_pr_baseline <- function(){
	data_matrix <- read.table(file_list[1], header = FALSE, sep="\t")
	actual_list <- c()
	n_col = dim(data_matrix)[2]
	actual_col <- seq(1,n_col-1,2)
	y = 0
	a = 0
	for(i in actual_col){
		y = y+sum(data_matrix[i]==1)
		a = a+dim(data_matrix[i])[1]
		actual_list <- c(actual_list,data_matrix[i])
	}
	baseline_freq = y/a
	return(baseline_freq)
}

add_pr_curve <- function(index){
	dataFile <- read.table(file_list[index], header = FALSE, sep="\t")
	color <- backwardsColors[index]
	perf <- get_perf_PR(dataFile)
	plot(perf, avg='vertical', spread.estimate='stderror', ylim=c(0,1), col = color,lwd=2,add=TRUE)
	#plot(perf, avg='threshold', spread.estimate='stderror', ylim=c(0,1), col = color,lwd=2,add=TRUE)
	#plot(perf, avg='threshold', ylim=c(0,1), col = color,lwd=2,add=TRUE)
}
############################################



args = commandArgs(TRUE)
top_file <- args[1]
directory <- normalizePath(args[2])
lbls <- clean_up_labels(args[3])
# outStr <- args[4]
str_error_inc <- 'n'
str_error_inc <- args[4]
edge_inc <- 'y'
edge_inc <- args[5]

### GET FILE LIST ##########################
top_file_m <- read.table(top_file,sep="\t",header=FALSE)

file_list <- c()
for(i in as.matrix(top_file_m[1])){
	full_file = paste(directory,"/",i,sep="")
	file_list <- c(file_list,full_file)
}
aucroc_list <- c()
for(i in as.matrix(top_file_m[2])){
	aucroc_list <- c(aucroc_list,round(i,digits=3))
}
for(i in 1:length(aucroc_list)){
	variance <- round(as.matrix(top_file_m[3])[i],digits=3)
	if(str_error_inc == "y"){
		aucroc_list[i] <- c(paste(aucroc_list[i]," +/- ",variance,sep=""))
	}
}
#############################################



### CHART PREP #############################
label_list = split_str(lbls,",",0)
colorLst <- c("cyan","purple","orange","green","blue","red")
# colorLst <- c("gray","purple","orange","green","blue","red")
backwardsColors <- rev(colorLst)
indeces <- 1:length(file_list)
rev_ind <- rev(indeces)
#label_list <-paste(label_list,aucroc_list,sep=", ")
############################################

# library(bitops,lib.loc="/opt/software/R/2.13.2--GCC-4.4.5/lib64/R/library/")
# library(caTools,lib.loc="/opt/software/R/2.13.2--GCC-4.4.5/lib64/R/library/")
# library(gdata,lib.loc="/opt/software/R/2.13.2--GCC-4.4.5/lib64/R/library/")
# library(gtools,lib.loc="/opt/software/R/2.13.2--GCC-4.4.5/lib64/R/library/")
# library(gplots,lib.loc="/opt/software/R/2.13.2--GCC-4.4.5/lib64/R/library/")
# library(ROCR,lib.loc="/opt/software/R/2.13.2--GCC-4.4.5/lib64/R/library/")
library(ROCR)

### AUCROC PLOTS #####################
pdf(paste(top_file,'.roc.pdf',sep=""))
create_plot("True Positive Rate","False Positive Rate")
abline(0,1,lty="longdash",lwd = 2,col="darkgray")
for(i in rev_ind){
	add_aucroc_curve(i)
}
legend("bottomright",paste(label_list,aucroc_list,sep=", "),col=backwardsColors,lty=1,lwd=2,bg="white")
box()
dev.off()
###########################################



### PREC RECALL PLOTS ########################
pdf(paste(top_file,'.pr.pdf',sep=""))
create_plot("Precision","Recall")
pr_bsline <- get_pr_baseline()
abline(pr_bsline,0,lty="longdash",lwd = 2,col="darkgray")
# first_go <- TRUE
for(i in rev_ind){
	add_pr_curve(i)
}
legend("topright",label_list,col=backwardsColors,lty=1,lwd=2,bg="white")
box()
dev.off()
###########################################

