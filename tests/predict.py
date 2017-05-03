#!/usr/bin/env python
from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import os, random
import numpy as np
import h5py
from keras.models import load_model
import math
from Bio.SubsMat.MatrixInfo import blosum62 as blosum
############################dealing with peptide to images
amino_acids = {'X':-1,'C':0, 'I':1,  'F':2,  'L':3,  'V':4,  'W':5,  'M':6,  'Y':7, 'A':8,  'G':9,  'H':10,  'T':11,  'S':12, \
'P':13,  'Q':14,  'N':15,  'R':16,  'D':17,  'E':18,  'K':19,  '-':20,'B':20,'U':20,"Z":20,'O':20}
aa_list=['C','I','F','L','V','W','M','Y','A','G','H','T','S','P','Q','N','R','D','E','K']
def peptovec(vector):
	result_vector=[]
	ytemp=[]
	for line in vector:
		line=line.strip()
		xtemp=[]
		for aa in line.split()[2]:
			aa_list=[0]*20
			aa_list[int(amino_acids[aa])+1]=1
			xtemp.append(aa_list)
		ytemp.append(line.split()[-1])
		result_vector.append(np.array(xtemp).T)
	return (np.array(result_vector),np.array(ytemp))
def peptoblosum(vector):
    result_vector=[]
    ytemp=[]
    for line in vector:
        line=line.strip()
        xtemp=[]
        for aa in line.split()[2]:
            aa_list_temp=[0]*20
            for (i,num) in enumerate(aa_list):
                if aa in aa_list:
                    try:
                        aa_list_temp[i]=int((math.exp(float(blosum[(num,aa)]*0.347)))/(math.exp(11*0.347))*256)
                    except:
                        aa_list_temp[i]=int((math.exp(float(blosum[(aa,num)]*0.347)))/(math.exp(11*0.347))*256)
                else:
                    aa_list_temp[i]=int((math.exp(-4*0.347))/(math.exp(11*0.347))*256)
            xtemp.append(aa_list_temp)
        ytemp.append(line.split()[-1])
        result_vector.append(np.array(xtemp).T)
    return (np.array(result_vector),np.array(ytemp))


predict_pdb = open("input.dat", "r").readlines()
prediction=[]
os.system("rm predict_num -rf")
batch_size = 128
num_classes = 2
epochs = 1
img_rows, img_cols = 20, 31
model = load_model('cysteine_active.h5')
for (i,line) in enumerate(predict_pdb):
	if i%2048!=0 and i!=(len(predict_pdb)-1) :	
		prediction.append(line.strip()+" 0")
	else:
		prediction.append(line.strip()+" 0")
#		(x_prediction, y_prediction)=peptovec(prediction)
		(x_prediction, y_prediction)=peptoblosum(prediction)
		x_prediction = x_prediction.reshape(x_prediction.shape[0], img_rows, img_cols, 1)
		classes =model.predict(x_prediction,batch_size=2048)
		output=open("predict_num",'a')
		for i,num in enumerate(classes.argmax(axis=1)):
			output.write(str(num)+"\t"+str(classes[i][num])+"\n")
		prediction=[]
