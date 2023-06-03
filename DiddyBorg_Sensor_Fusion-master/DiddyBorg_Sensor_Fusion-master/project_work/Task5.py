import csv
import numpy as np
import math as mat
import matplotlib.pyplot as plt

csv_file1 = open('../../data/task5/camera_localization_task5.csv')
csv_reader1 = csv.reader(csv_file1)
csv_file2 = open('../../data/qr_code_position_in_global_coordinate.csv')
csv_reader2 = csv.reader(csv_file2)

QR_reading = []
for raw in csv_reader1:
    QR_reading.append(raw)
QR_data = [[float(x) for x in row] for row in QR_reading]
QR_data = np.array(QR_data)

QR_Pos_reading = []
for raw in csv_reader2:
    QR_Pos_reading.append(raw)
QR_Pos = [[float(x) for x in row] for row in QR_Pos_reading]
QR_Pos = np.array(QR_Pos)

QR_20 = []
QR_21 = []
QR_25 = []
QR_26 = []
QR_27 = []
QR_31 = []
QR_32 = []
for i in range(701):
    if QR_data[i,1] == 20:
        QR_20.append(QR_data[i])
    if QR_data[i,1] == 21:
        QR_21.append(QR_data[i])
    if QR_data[i,1] == 25:
        QR_25.append(QR_data[i])
    if QR_data[i,1] == 26:
        QR_26.append(QR_data[i])
    if QR_data[i,1] == 27:
        QR_27.append(QR_data[i])
    if QR_data[i,1] == 31:
        QR_31.append(QR_data[i])
    if QR_data[i,1] == 32:
        QR_32.append(QR_data[i])
QR_20 = np.array(QR_20)
QR_21 = np.array(QR_21)
QR_25 = np.array(QR_25)
QR_26 = np.array(QR_26)
QR_27 = np.array(QR_27)
QR_31 = np.array(QR_31)
QR_32 = np.array(QR_32)

QR_20_P = QR_Pos[10,1:3]
QR_21_P = QR_Pos[11,1:3]
QR_25_P = QR_Pos[12,1:3]
QR_26_P = QR_Pos[13,1:3]
QR_27_P = QR_Pos[14,1:3]
QR_31_P = QR_Pos[15,1:3]
QR_32_P = QR_Pos[16,1:3]

QR = np.array([QR_20_P,QR_21_P,QR_25_P,QR_26_P,QR_27_P,QR_31_P,QR_32_P])
QR = np.concatenate((np.zeros((7,1)),QR),axis=1)
h0 = 11.5
f = 544.85
sigma = 0.5 # we use the same standard deviation for all measurement
R = sigma*sigma*np.eye(2) # measurement variance
R_inv = np.eye(2)/(sigma*sigma) #cache the inverse
x_history = np.zeros((701,4))
x_history[0,:] = np.array([0,0,0,0])
QR_data = np.concatenate((QR_20,QR_21,QR_25,QR_26,QR_27,QR_31,QR_32),axis=0)
y = np.zeros((701,2))
y[:,0] = QR_data[:,5]
y[:,1] = QR_data[:,2]

def g(x,i):
    hi = h0*f/mat.sqrt((QR[i,1]-x[1])**2+(QR[i,2]-x[2])**2)
    Cxi = f*mat.tan(mat.atan((QR[i,2]-x[2])/(QR[i,1]-x[1]))-x[3])
    return [hi,Cxi]

def G(x,i):
    G = np.array([[-(f * h0 * (2 * x[1] - 2 * QR[i, 1])) / (2 * ((x[1] - QR[i, 1])**2 + (x[2] - QR[i, 2])**2)**(3 / 2)),
             -(f * h0 * (2 * x[2] - 2 * QR[i, 2])) / (2 * ((x[1] - QR[i, 1])**2 + (x[2] - QR[i, 2])**2)**(3 / 2)),
             0],
            [-(f * (x[2] - QR[i, 2]) * (np.tan(x[3] - np.arctan((x[2] - QR[i, 2]) / (x[1] - QR[i, 1])))**2 + 1)) / (
                        (x[1] - QR[i, 1])**2 * ((x[2] - QR[i, 2])**2 / (x[1] - QR[i, 1])**2 + 1)),
             (f * (np.tan(x[3] - np.arctan((x[2] - QR[i, 2]) / (x[1] - QR[i, 2])))**2 + 1)) / (
                         (x[1] - QR[i, 1]) * ((x[2] - QR[i, 2])**2 / (x[1] - QR[i, 1])**2 + 1)),
             -f * (np.tan(x[3] - np.arctan((x[2] - QR[i, 2]) / (x[1] - QR[i, 1])))**2 + 1)]])
    return G


for j in range(701):
    if j < 96:
        i = 1
    elif j >= 96 & j<186:
        i = 2
    elif j >= 186 & j < 290:
        i = 3
    elif j >= 290 & j < 388:
        i = 4
    elif j >= 388 & j < 492:
        i = 5
    elif j >= 492 & j < 597:
        i = 6
    else:
        i = 7
    gj = np.mat(g(x_history[j,:],i))
    Gj = np.mat(G(x_history[j,:],i))
    x_history[j+1,:] = x_history[j,:] + np.linalg.solve((Gj.T@R_inv@Gj),Gj.T@R_inv@(y[j]-gj))

