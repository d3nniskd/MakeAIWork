import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing

path_to_file = 'datasets/car_lidar/default.samples'

names = ['lidar1', 'lidar2', 'lidar3', 'lidar4', 'lidar5', 'lidar6', 'lidar7', 'lidar8', 'lidar9', 'lidar10', 'lidar11', 'lidar12', 'lidar13', 'lidar14', 'lidar15', 'lidar16', 'angle']

lidarData = pd.read_csv(path_to_file, names=names, delim_whitespace=True)

lidarData.head()

X = lidarData.iloc[:, 0:16] # tot 16
y = lidarData.iloc[:, 16]

print (X)
print (y)

# Train/Test-split to avoid over-fitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

print(X_train)
print(y_train)

model = LinearRegression()

# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# scaler.fit(X_train)

model.fit(X_train, y_train)

# making predictions
predictions = model.predict(X_test)

# model evaluation
print(
  'mean_squared_error : ', mean_squared_error(y_test, predictions))
print(
  'mean_absolute_error : ', mean_absolute_error(y_test, predictions))

# opslaan van model
import pickle
pickle.dump(model, open('lidar_model.pkl', 'wb'))
