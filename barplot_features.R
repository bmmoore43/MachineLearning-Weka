#data is feature list with associated pos and neg weights

#read in data
fcq1 <- read.csv("feature_importance_out3.csv",header=T,sep=",")
library("ggplot2")

#order by weight
data <- transform(fcq1, 
                          Feature = reorder(Feature, Weight))

#barplot
p1<-ggplot(data,aes(x=Feature,y=Weight, fill= Weight)) + stat_summary(fun.y=mean,geom="bar") +
  coord_flip()
p1
p2 <- p1 + scale_fill_continuous(low = "blue", high = "red")
p2
p3<- p2 + theme(text = element_text(size =16), 
           axis.text.x = element_text(size = 16, colour = "black"),
           axis.text.y = element_text(size = 16, colour = "blue"))
p3
p4<- p1 + theme(text = element_text(size =16), 
                axis.text.x = element_text(size = 16, colour = "black"),
                axis.text.y = element_text(size = 16, colour = "blue"))
p4
