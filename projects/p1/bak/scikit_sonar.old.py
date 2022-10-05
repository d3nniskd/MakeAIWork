import pandas as pd

# Location of file
file = "datasets/car_sonar/default.samples"

# Assign column names to the dataset
names = ['sonar1', 'sonar2', 'sonar3', 'angle']

# Read dataset to pandas dataframe
sonarData = pd.read_csv(file, names=names, delim_whitespace=True)

# To see what this dataset actually looks like
sonarData.head()

# splitten van data in X (de input) en y (de controlle aan het eind)
X = sonarData.iloc[:, 0:3] # tot 3
y = sonarData.iloc[:, 3]

# bekijk waarden
print (X)
print (y)

# Laat unieke waarden zien
y.unique()

# Nu kunnen we het NN daadwerkelijk gaan trainen

# Oplossing met lineaire regressie
# from sklearn.neural_network import MLPRegressor
# from sklearn.datasets import make_regression
# from sklearn.model_selection import train_test_split
# X, y = make_regression(n_samples=200, random_state=1)
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
# regr = MLPRegressor(random_state=1, max_iter=20000).fit(X_train, y_train)
# regr.predict(X_test[:2])
# regr.score(X_test, y_test)
# print(regr.predict)
# print(regr.score)

# Oplossing met categorien
