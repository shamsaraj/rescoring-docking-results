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
from prepare_ligand4_m import*
from prepare_receptor4_m import *
def make_directory_if_not_exists(path):
    while not os.path.isdir(path):
        try:
            os.makedirs(path)
            break    
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        except WindowsError:
            print "got WindowsError"
            pass 
def copy_files (src, dest, ext) :
	src_files = os.listdir(src)
	for file_name in src_files:
		if file_name.endswith(ext):
				full_file_name = os.path.join(src, file_name)
				if (os.path.isfile(full_file_name)):
					shutil.copy2(full_file_name, dest)
def move_files (src, dest, ext) :
	src_files = os.listdir(src)
	for file_name in src_files:
		if file_name.endswith(ext):
    			full_file_name = os.path.join(src, file_name)
    			if (os.path.isfile(full_file_name)):
        			shutil.move(full_file_name, dest)
def makefile (name, path, text):
	os.chdir(path)
	newfile = open(name, "w")
	newfile.write(text)
	newfile.close()
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      count += 1
  return count
def Vina (receptor , ligand , log):
	cmd = "vina --receptor " + receptor + " --ligand " + ligand + " --score_only --log " + log
	os.system(cmd)
def Vina_t (conf, ligand , log, scriptpath):
	os.chdir(scriptpath)
	cmd = "vina --config " + conf + " --ligand " + ligand + " --score_only --log " + log
	os.system(cmd)
def receptor2pdbqt (RF , OF):
	PR (RF, OF)
	#os.chdir(scriptpath)
	#cmd = python_path + "python prepare_receptor4.py -r " + receptor + " -o " + out #+ " -p Zn " #+ " -A 'hydrogens' 'bonds' 'hydrogens_bonds'"
	#os.system(cmd)
def ligand2pdbqt (LF, OF):
	#os.chdir(scriptpath)
	PL (LF, OF)
	#cmd = python_path + "python prepare_ligand4.py -l " + ligand + " -o " + out #+ " -A 'hydrogens' 'bonds' 'hydrogens_bonds'"
	#os.system(cmd)
def extraction (keyword, datapath , output):
	os.chdir (datapath)
	ff = open (output, "w")	
	out = csv.writer(ff)
	out.writerow (["name" , "energy"])		
	for filename in os.listdir (datapath):
		if filename.endswith(".txt"):
			f = open (filename, "r")
			for line in f:
				if keyword in line:
					words = line.split()
					for word in words:
						answer = is_number(word)
						if answer == True:
							if abs(float(word)) > 1:		
								out.writerow ([filename , word])
                        f.close()
	ff.close()	
def make_csv (name, output):
    ff = open (output, "w")	
    out = csv.writer(ff)
    out.writerow (["name" , "energy"])		
    for nn in range (0,m1):
            if name == "Actives":
                out.writerow ([nn , actives[nn]])
            elif name == "Decoys":
                out.writerow ([nn , decoys[nn]])
    ff.close()	
#def contributions (name, mypath, gauss1_e,gauss2_e ,repulsion_e ,hydrophobic_e , hydrogen_e ,rot_e, n, t):
#    if n == "1" : #this speeds up the scripts as it only calcuate energy terms of molecules one time
#        extraction2 ("gauss 1", mypath + "/Vina", ".txt")
#        extraction2 ("gauss 2", mypath + "/Vina", ".txt")
#        extraction2 ("repulsion", mypath + "/Vina", ".txt")
#        extraction2 ("hydrophobic", mypath + "/Vina", ".txt")
#        extraction2 ("Hydrogen", mypath + "/Vina", ".txt")
#    extraction2 ("torsions", mypath + "/Autodock", ".pdbqt")
#    #m1 = directory(mypath + "/Autodock",".pdbqt")
#    for nn in range (0, m1):
#        energy (name, gauss1, gauss2, repulsion,  hydrophobic, Hydrogen, Nrot, nn, gauss1_e,gauss2_e ,repulsion_e ,hydrophobic_e , hydrogen_e ,rot_e)
#    make_csv (name, mypath + "/" + str (t) + "vina_output_" + n + ".csv")
#def Xscore (receptor , ligand , log, parameter):
#	os.chdir(parameter)
#	cmd = "xscore -score " +  receptor + " " + ligand + " >" + log
#	os.system(cmd)
#def DSX (receptor , ligand , out , pdb_pot , swi):
#	os.chdir (out)
#	cmd = "dsx_linux_64.lnx dsx -P " + receptor + " -L " + ligand + " -D " + pdb_pot + " " + swi
#	os.system(cmd)
#def Xscore_fixrec (receptor , out , parameter):
#	os.chdir(parameter)
#	cmd = "xscore -fixpdb " + receptor + " " + out
#	os.system(cmd)
#def Xscore_fixmol2 (ligand , out , parameter):
#	os.chdir(parameter)
#	cmd = "xscore -fixmol2 " + ligand + " " + out
#	os.system(cmd)
#def Autodock (receptor , ligand , log, scripts):
	#os.chdir(scripts)
	#cmd = "python compute_AutoDock41_score.py -r " + receptor + " -l " + ligand + " -o " + log
	#os.system(cmd)
#def extraction2 (keyword, datapath, ext):
#        mm=-1
#        m = directory(datapath,ext)
#        global m1
#        m1 = m
#        if keyword == "gauss 1":
#            global gauss1
#            gauss1 = range(m)
#        elif keyword == "gauss 2":
#            global gauss2
#            gauss2 = range(m)
#        elif keyword == "repulsion":
#            global repulsion
#            repulsion = range(m)
#        elif keyword == "hydrophobic":
#            global hydrophobic
#            hydrophobic = range(m)
#        elif keyword == "Hydrogen":
#            global Hydrogen
#            Hydrogen = range(m)
#        elif keyword == "torsions":
#            global Nrot
#            Nrot = range(m)
#	os.chdir (datapath)
#	for filename in os.listdir (datapath):
#                if filename.endswith(ext):
#                    mm= mm + 1
#		    f = open (filename, "r")
#		    for line in f:
#                        if keyword in line:
#				words = line.split()
#				for word in words:
#					    answer = is_number(word)
#                                            if answer == True:
#						if abs(float(word)) > 1:
#							if keyword == "gauss 1":
#                                                            gauss1[mm] = float (word)
#                                                        elif keyword == "gauss 2":
#                                                            gauss2[mm] = float (word)
#                                                        elif keyword == "repulsion":
#                                                            repulsion[mm] = float (word)
#                                                        elif keyword == "hydrophobic":
#                                                            hydrophobic[mm] = float (word)
#                                                        elif keyword == "Hydrogen":
#                                                            Hydrogen[mm] = float (word)
#                                                        elif keyword == "torsions":
#                                                           Nrot[mm] = float (word)
#
#
#                    f.close()
#def energy (name, term1, term2, term3, term4, term5, term6, indice, gauss1_e,gauss2_e ,repulsion_e ,hydrophobic_e , hydrogen_e ,rot_e):
#    if name == "Actives":
#        if indice == 0:
#            global actives
#            actives = range (m1)
#        actives[indice] = ((term1[indice] * gauss1_e) + (term2[indice] * gauss2_e) + (term3[indice] * repulsion_e) + (term4[indice] * hydrophobic_e) + (term5[indice] * hydrogen_e)) / (1 + ((term6[indice]) * rot_e))
#    if name == "Decoys":
#        if indice == 0:
#            global decoys
#            decoys = range (m1)
#        decoys[indice] = ((term1[indice] * gauss1_e) + (term2[indice] * gauss2_e) + (term3[indice] * repulsion_e) + (term4[indice] * hydrophobic_e) + (term5[indice] * hydrogen_e)) / (1 + ((term6[indice]) * rot_e))



