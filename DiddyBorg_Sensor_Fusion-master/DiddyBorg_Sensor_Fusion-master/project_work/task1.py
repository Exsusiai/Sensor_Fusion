import numpy as np
import csv

csvFile = open('../../data/task1/imu_reading_task1.csv')
Dataset = csv.reader(csvFile)
Dataset = np.array([[float(x) for x in row] for row in Dataset])

gyro_angular_velocity = Dataset[:, 6:9]
gyro_bias = np.mean(gyro_angular_velocity, axis=0)

gyro_angular_velocity_x = gyro_angular_velocity[:, 0]
gyro_angular_velocity_y = gyro_angular_velocity[:, 1]
gyro_angular_velocity_z = gyro_angular_velocity[:, 2]

Var = [np.var(gyro_angular_velocity_x), np.var(gyro_angular_velocity_y), np.var(gyro_angular_velocity_z)]
gyro_Var = np.diag(Var)

