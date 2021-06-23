##########################################################################
#Scorer
#A tool to develope target-specific weights for scoring by AutoDock Vina
#v. 1.0
#Copyright (C) 2015  Jamal Shamsara
#
#Usage of Scorer is free without any limitations
#There is NO warranty
###########################################################################
import os
import fileinput
import shutil
import csv
from rescore_functions import *
def vina_targeted (project_path, user_actives_path, user_autodockscripts_path, user_receptor_path,user_decoys_path,recfile,recfile2,gauss1,gauss2 ,repulsion ,hydrophobic , hydrogen ,rot, CDIR):
	#this function for having two groups, actives and decoys
	W = ["Actives" , "Decoys"]
	for w in W :
		mypath = project_path + "/" + w
		molecules_path = mypath + "/Molecules"
		receptor_path = mypath + "/Receptor"

		make_directory_if_not_exists(mypath)
		subdirs = ["Molecules", "Vina" , "Autodock" , "Receptor"]
		for subs in subdirs:
			newpath2 = mypath + "/" + subs
			make_directory_if_not_exists(newpath2)
		copy_files (user_receptor_path, receptor_path , recfile)
		#copy_files (user_autodockscripts_path, mypath + "/Autodock" , ".py")
		#copy_files (user_autodockscripts_path, mypath + "/Autodock" , ".exe")
		if w == "Actives":
			copy_files (user_actives_path, molecules_path , ".mol2")
		elif w == "Decoys":
			copy_files (user_decoys_path,  molecules_path , ".mol2")
		# receptor to pdbqt
		receptor2pdbqt (receptor_path + "/" + recfile , receptor_path + "/" + recfile2)
		for line in fileinput.input(receptor_path + "/" + recfile2, inplace =1):
			line = line.replace ("0.000 Zn" , "2.000 Zn" )
			line = line.replace ("0.000 Ca" , "2.000 Ca" )
			print (line)
		makefile ("conf.txt", mypath + "/Autodock", "cpu = 1" + "\nreceptor = " + receptor_path + "/" + recfile2 + " \nweight_gauss1 = " + str (gauss1) + " \nweight_gauss2 = " + str (gauss2) +  " \nweight_repulsion = " + str (repulsion) + " \nweight_hydrophobic = " + str (hydrophobic) + " \nweight_hydrogen = " +  str (hydrogen) + " \nweight_rot = " + str (rot))
		for ligfile in os.listdir(molecules_path):
			if ligfile.endswith(".mol2")or ligfile.endswith (".pdb")or ligfile.endswith (".pdbqt"):
				# ligands to pdbqt
				ligand2pdbqt (molecules_path + "/" + ligfile , mypath + "/Autodock/" + ligfile + ".pdbqt")
				# Performing Vina Rescoring
				Vina_t (mypath + "/Autodock/conf.txt", mypath + "/Autodock/" + ligfile + ".pdbqt" , mypath + "/Vina/" + "vina" + ligfile + ".txt", CDIR)
		#Vina
		extraction ("kcal/mol", mypath + "/Vina", mypath + "/vina_output.csv")
def vina_targeted3 (project_path, user_actives_path, user_autodockscripts_path, user_receptor_path,user_decoys_path,recfile,recfile2,gauss1,gauss2 ,repulsion ,hydrophobic , hydrogen ,rot, CDIR):
	# For only one group
	W = ["Actives"]
	for w in W :
		mypath = project_path + "/" + w
		molecules_path = mypath + "/Molecules"
		receptor_path = mypath + "/Receptor"
		make_directory_if_not_exists(mypath)
		subdirs = ["Molecules", "Vina" , "Autodock" , "Receptor"]
		for subs in subdirs:
			newpath2 = mypath + "/" + subs
			make_directory_if_not_exists(newpath2)
		copy_files (user_receptor_path, receptor_path , recfile)
		if w == "Actives":
			copy_files (user_actives_path, molecules_path , ".mol2")
		elif w == "Decoys":
			copy_files (user_decoys_path,  molecules_path , ".mol2")
		#receptor to pdbqt
		receptor2pdbqt (receptor_path + "/" + recfile , receptor_path + "/" + recfile2)
		for line in fileinput.input(receptor_path + "/" + recfile2, inplace =1):
			line = line.replace ("0.000 Zn" , "2.000 Zn" )
			line = line.replace ("0.000 Ca" , "2.000 Ca" )
			print (line)
		makefile ("conf.txt", mypath + "/Autodock", "receptor = " + receptor_path + "/" + recfile2 + " \nweight_gauss1 = " + str (gauss1) + " \nweight_gauss2 = " + str (gauss2) +  " \nweight_repulsion = " + str (repulsion) + " \nweight_hydrophobic = " + str (hydrophobic) + " \nweight_hydrogen = " +  str (hydrogen) + " \nweight_rot = " + str (rot))
		for ligfile in os.listdir(molecules_path):
			if ligfile.endswith(".mol2")or ligfile.endswith (".pdb")or ligfile.endswith (".pdbqt"):
				#ligands to pdbqt
				ligand2pdbqt (molecules_path + "/" + ligfile , mypath + "/Autodock/" + ligfile + ".pdbqt")
				#Performing Vina Rescoring
				Vina_t (mypath + "/Autodock/conf.txt", mypath + "/Autodock/" + ligfile + ".pdbqt" , mypath + "/Vina/" + "vina" + ligfile + ".txt", CDIR)
		#Vina
		extraction ("kcal/mol", mypath + "/Vina", mypath + "/vina_output.csv")
#def vina_targeted2 (project_path,gauss1,gauss2 ,repulsion ,hydrophobic , hydrogen ,rot, n, t): #def for fast rescoring using vina equation
#    W = ["Actives" , "Decoys"]
#	for w in W :
#       mypath = project_path + "/" + w
#        contributions (w, mypath,gauss1,gauss2 ,repulsion ,hydrophobic , hydrogen ,rot, n, t)
#def ROC (project_path, user_actives_path, user_autodockscripts_path, xscore_parameter_path, user_receptor_path,user_decoys_path,recfile,recfile1,recfile2):
#	W = ["Actives" , "Decoys"]
#	for w in W :
#		mypath = project_path + "/" + w
#		molecules_path = mypath + "/Molecules"
#		receptor_path = mypath + "/Receptor"
#
#		make_directory_if_not_exists(mypath)
#		subdirs = ["Molecules", "Xscore" , "DSX" , "Vina" , "Autodock" , "Receptor"]
#		for subs in subdirs:
#			newpath2 = mypath + "/" + subs
#			make_directory_if_not_exists(newpath2)
#
#		copy_files (user_receptor_path, receptor_path , recfile)
#		copy_files (user_autodockscripts_path, mypath + "/Autodock" , ".py")
#		if w == "Actives":
#			copy_files (user_actives_path, molecules_path , ".mol2")
#		elif w== "Decoys":
#			copy_files (user_decoys_path,  molecules_path , ".mol2")
#
#
#		#fix receptor pdb file for xscore
#		Xscore_fixrec (receptor_path + "/" + recfile , receptor_path + "/" + recfile1 , xscore_parameter_path)
#
#		#receptor to pdbqt
#		receptor2pdbqt (receptor_path + "/" + recfile , receptor_path + "/" + recfile2 , mypath + "/Autodock")
#
#		for line in fileinput.input(receptor_path + "/" + recfile2, inplace =1):
#       	 		line = line.replace ("0.000 Zn" , "2.000 Zn" )
#			line = line.replace ("0.000 Ca" , "2.000 Ca" )
#      		  	print (line)
#		makefile ("conf.txt", mypath + "/Autodock", "receptor = " + receptor_path + "/" + recfile2 + " \nweight_repulsion = 0.84024500000000002 \nweight_hydrophobic = -0.035069000000000003 \nweight_hydrogen = -0.58743900000000004 \nweight_rot = 0.058459999999999998")
#
#		for ligfile in os.listdir(molecules_path):
#			if ligfile.endswith(".mol2"):
#				#Performing DSX
#				DSX (receptor_path + "/" + recfile , molecules_path + "/" + ligfile , mypath + "/DSX" , "/home/jamal/Softs/dsx/pdb_pot_0511" , "-v")
#				#fix ligand mol2 files for xscore
#				Xscore_fixmol2 (molecules_path + "/" + ligfile , mypath + "/Xscore/" + ligfile , xscore_parameter_path)
#				#Performing xscore on molecules
#				Xscore (receptor_path + "/" + recfile1 , mypath + "/Xscore/" + ligfile , mypath + "/Xscore/" + ligfile + ".txt", xscore_parameter_path)
#				#ligands to pdbqt
#				ligand2pdbqt (molecules_path + "/" + ligfile , mypath + "/Autodock/" + ligfile + ".pdbqt" , mypath + "/Autodock")
#				#Performing Vina Rescoring
#				Vina (receptor_path + "/" + recfile2 , mypath + "/Autodock/" + ligfile + ".pdbqt" , mypath + "/Vina/" + "vina" + ligfile + ".txt")
#				#Performing Autodock Rescoring
#				Autodock (receptor_path + "/" + recfile2 , mypath + "/Autodock/" + ligfile + ".pdbqt" , mypath + "/Autodock/Autodock-rescore.txt", mypath + "/Autodock/")
#
#		#Xscore
#		extraction ("kcal/mol", mypath + "/Xscore/", mypath + "/xscore_output.csv")
#		#DSX
#		extraction ("|  none  |", mypath + "/DSX", mypath + "/dsx_output.csv")
#		#Vina
#		extraction ("kcal/mol", mypath + "/Vina", mypath + "/vina_output.csv")
#		#Autodock
#		fff= open(mypath + "/autodock_output.csv", "w")
#		out = csv.writer(fff)
#		out.writerow (["name" , "energy"])
#		f = open (mypath + "/Autodock/Autodock-rescore.txt", "r")
#		i = 0
#		for line in f:
#			i = i + 1
#			if i > 1 :
#				words = line.split()
#				out.writerow ([words[0] , words[1]])
#		f.close()
#		fff.close()


