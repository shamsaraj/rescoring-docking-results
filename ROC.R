##########################################################################
#Scorer
#A tool to develope target-specific weights for scoring by AutoDock Vina
#v. 1.0
#Copyright (C) 2015  Jamal Shamsara
#
#Usage of Scorer is free without any limitations
#There is NO warranty
###########################################################################

#loading ROCR library
#loading enrichvs library
args=(commandArgs(TRUE))
library("ROCR")# package for ROC curve 
library (enrichvs)# package for calculation of enrichment factor
project_path2 <- args[1]#"/home/jamal/Desktop/ROC-curve"
selection <- args[2]
count <- args[3]
t <- args[4]
project_path <- args[5]
#selection = 2
#ROC<- function (path, choice)
setwd(project_path2)#working directory
path1 = paste (project_path2 , "/Actives", sep="")
path2 = paste (project_path2 , "/Decoys" , sep="")
if (selection == 11){
header <- c ("Vina" , "Autodock", "DSX" , "Xscore")#manualy defined headers
inputfile <- c ("/vina_output.csv" , "/autodock_output.csv", "/dsx_output.csv" , "/xscore_output.csv")
}
if (selection == 1 || selection == 2 || selection == 17 || (selection == 13 && count == 0)){
header <- c ("Vina" )#manualy defined headers
inputfile <- c ("/vina_output.csv" )
}
if ((selection == 13 && count != 0) || selection == 14) {
header <- c ("Vina" )#manualy defined headers
inputfile1 <-paste ("/", t, "vina_output_" , count, ".csv", sep="")
inputfile <- c (inputfile1)
}
l<-length(header)
for (i in (1:l)){#a loop for reading all columns 
title <- header[i]
activesfile<- paste (path1 , inputfile[i] , sep="")###### inputfile name for actives
decoysfile<-paste (path2 , inputfile[i] , sep="")######	input file name for decoys
table1 <- read.csv(activesfile,  sep=",", header=T)
score1 <- table1 [,2]
GGG1 <- score1[!is.na(score1)]#omiting NAs
table2 <- read.csv(decoysfile,  sep=",", header=T)
score2 <- table2 [,2]
GGG2 <- score2[!is.na(score2)]
y <- length (GGG1)
z <- length (GGG2)
x <- c("actives", "decoys")
xx <- c(1,0)
GGG <- c (GGG1, GGG2)
labels <- (rep(x ,c(y,z)))#build a vector for ROCR labels
labels2 <- (rep(xx ,c(y,z)))#build a vector for enrichvs labels
#calculation of enrichment factors at different levels and auc using enrichvs
ef100<-enrichment_factor(GGG, labels2, top=1.0, decreasing=FALSE)
ef20<-enrichment_factor(GGG, labels2, top=0.2, decreasing=FALSE)
ef10<-enrichment_factor(GGG, labels2, top=0.1, decreasing=FALSE)
ef2<-enrichment_factor(GGG, labels2, top=0.02, decreasing=FALSE)
ef1<-enrichment_factor(GGG, labels2, top=0.01, decreasing=FALSE)
auc1<-auc(GGG, labels2, decreasing=FALSE, top=1.0)
#write headers for output file
if (i==1){
filelines<-paste("Scoring-function", "AUC","EF100%", "EF20%", "EF10%", "EF2%", "EF1%", sep=",")
write (project_path2, file= paste (t, "output.csv" , sep=""), append = TRUE)
write (filelines, file= paste (t, "output.csv" , sep=""), append = TRUE)
}
#write results
filelines<-paste(title, auc1, ef100, ef20, ef10, ef2, ef1, sep=",")
outputfile1 <-paste (t, "output.csv" , sep="")
write (filelines, file= outputfile1, append = TRUE) 
if (selection == 1 ){
#variable for python
write (auc1, file= "targeted_auc.txt", append = TRUE)
filelines1<-paste(project_path2, auc1, ef100, ef20, ef10, ef2, ef1, sep=",")
outputfile2 <-paste (project_path, "/All.csv" , sep="")
write (filelines1, file= outputfile2, append = TRUE) 
}
if (selection == 13 && count == 0){
#variable for python
write (auc1, file= "targeted_auc.txt", append = TRUE)
}
if ((selection == 13 &&  count != 0)|| selection == 14){
file2 <-paste ("targeted_auc_" , count, ".txt", sep="")
write (auc1, file= file2, append = TRUE)
}
#calculation of AUC and ploting ROC curve by ROCR
pred <- prediction (GGG, labels)
perf <- performance (pred, "tpr", "fpr")
#plot (perf, colonize=T)
# changing params for the ROC plot - width, etc
par(mar=c(5,5,2,2),xaxs = "i",yaxs = "i",cex.axis=1.3,cex.lab=1.4)
# plotting the ROC curve
imagetitle<-paste( title, "png", sep=".")
png (imagetitle)
plot(perf,col="black",lty=3, lwd=3)
# calculating AUC
auc <- performance(pred,"auc")
# now converting S4 class to vector
auc <- unlist(slot(auc, "y.values"))
# adding min and max ROC AUC to the center of the plot
AUC <- round(auc, digits = 2)
AUC <- paste(c("AUC = "),AUC,sep="")
legend(0.5,0.3,c(AUC),border="white",cex=1.7,box.col = "white")
dev.off()
}
#clean up
dev.off()
if (file.exists("Rplots.pdf")) {
file.remove("Rplots.pdf")
}
if (selection == 13 || selection == 14){
if (file.exists(imagetitle)) {
file.remove(imagetitle)
}
}
#if (file.exists("targeted_auc.txt")) {
#file.remove("targeted_auc.txt")
#}
