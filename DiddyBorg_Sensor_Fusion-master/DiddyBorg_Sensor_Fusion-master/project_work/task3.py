import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd

Dataset = pd.read_csv('../../data/task3/camera_module_calibration_task3.csv', header=None)

Distance_detect = Dataset.values[:, 0].astype(np.float64)
height_pixel = Dataset.values[:, 1].astype(np.float64)

for i in range(0, Distance_detect.shape[0]):
    Distance_detect[i] = Distance_detect[i] + 1.6 + 5

for i in range(height_pixel.shape[0]):
    height_pixel[i] = 1/height_pixel[i]

y = Distance_detect
x = height_pixel

slope, intercept, r_value, p_value, std_err = st.linregress(x, y)

Distance_predict = []
error = []
for i in range(height_pixel.shape[0]):
    Distance_predict.append(slope*height_pixel[i] + intercept)
    error.append(Distance_predict[i]-Distance_detect[i])

h0 = 11.5
focal_length = slope/h0

print('gradient is ： {}'.format(slope))
print('bias is ： {}'.format(intercept))
print('r^2 ： {}'.format(r_value**2))
print('focal length is {} pixel'.format(focal_length))

plt.plot(x, y, 'bo', label='data')
plt.plot(x, x*slope+intercept, 'r-', label='Linear Regression')
plt.plot(x, error, 'g+', label='error')
plt.plot(x, x*0, 'k-', linewidth=0.5)
plt.xlabel('1/height,(1/pixel)')
plt.ylabel('distance(cm)')
plt.legend()
plt.show()
