import pandas as pd

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

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

regressor.fit(X_train, y_train)

print(regressor.intercept_)

print(regressor.coef_)