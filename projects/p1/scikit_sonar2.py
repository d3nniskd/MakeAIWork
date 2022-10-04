import pandas as pd

# Location of file
file = './datasets/car_sonar/default.samples.csv'
# absoluut pad
# file = '/Users/dennis/Repo/MakeAIWork/projects/p1/datasets/car_sonar/default.samples'

# Assign column names to the dataset
names = ['sonar1', 'sonar2', 'sonar3', 'angle']

# Read dataset to pandas dataframe
# sonarData = pd.read_csv(file, names=names, delim_whitespace=True)
sonarData = pd.read_csv(file, names=names)
# sep=','
 
# To see what this dataset actually looks like
sonarData.head()

# splitten van data in X (de input) en y (de controlle aan het eind)
X = sonarData.iloc[:, 0:3] # tot 3
# y = sonarData.select_dtypes(include=[object])
y = sonarData.iloc[:, 3]

# bekijk waarden
print (X)
print (y)

# Train/Test-split to avoid over-fitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

# Laat unieke waarden zien
y.unique()

# Feature scaling slaan we over? Nee is nodig
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

# Nu kunnen we het NN daadwerkelijk gaan trainen
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
mlp.fit(X_train, y_train.values.ravel())
# The first parameter, hidden_layer_sizes, is used to set the size of the hidden layers.
# In our script we will create three layers of 10 nodes each.
# Try different combinations and see what works best.
# The second parameter to MLPClassifier specifies the number of iterations, or the epochs.
# By default the 'relu' activation function is used with 'adam' cost optimizer.
# You can change these functions using the activation and solver parameters, respectively.
# In the third line the fit function is used to train the algorithm on our training data
# The final step is to make predictions on our test data. To do so, execute the following script:
predictions = mlp.predict(X_test)

# Evaluate the algorithm
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))

print(predictions)


# opslaan van model
import pickle

pickle.dump(mlp, open('pickle_model.pkl', 'wb'))

# methode Amat
# Save to file in the current working directory
# pkl_filename = "pickle_model.pkl"
# with open(pkl_filename, 'wb') as file:
#     pickle.dump(mlp.fit, file)

# Load from file
# with open(pkl_filename, 'rb') as file:
#     pickle_model = pickle.load(file)
    
# Calculate the accuracy score and predict target values
# score = pickle_model.score(Xtest, Ytest)
# print("Test score: {0:.2f} %".format(100 * score))
# Ypredict = pickle_model.predict(Xtest)