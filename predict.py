#!/usr/bin/env python
from __future__ import print_function
import keras
from keras import backend as K
import os
import h5py
from keras.models import load_model
from peptotensor import *

predict_pdb = open("results/input.dat", "r").readlines()
prediction=[]
os.system("rm results/predict_num -rf")
batch_size = 2048
img_rows, img_cols = 20, 31
model = load_model('models/binary_20170502.h5')
count=0
for (i,line) in enumerate(predict_pdb):
	if i%batch_size!=0 and i!=(len(predict_pdb)-1) :	
		prediction.append(line.strip()+" 0")
	else:
		count=count+batch_size
		print(count)
		prediction.append(line.strip()+" 0")
		(x_prediction, y_prediction)=peptoblosum(prediction)
		x_prediction = x_prediction.reshape(x_prediction.shape[0], img_rows, img_cols, 1)
		classes =model.predict(x_prediction,batch_size=batch_size)
		output=open("results/predict_num",'a')
		for i,num in enumerate(classes.argmax(axis=1)):
			output.write(str(num)+"\t"+str(classes[i][num])+"\n")
		prediction=[]