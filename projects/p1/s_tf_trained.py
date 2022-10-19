import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

keras = tf.keras

filename = '/Users/boyfrankclaesen/MakeAIWork/simulations/car/control_client/s_test_data.samples'

sonarData = np.loadtxt(filename, dtype=float, max_rows= 1000, usecols= (0,1,2,))
sonarSteeringAngle = np.loadtxt(filename, dtype=float, max_rows= 1000, usecols= (3,))

sonarDataVal = sonarData[500:700]
sonarSteeringAngleVal = sonarSteeringAngle[500:700]

# Opbouw NN
model = tf.keras.Sequential([
  tf.keras.Input(shape=(3,)),   # input; sensoren 1 t/m 3.
  tf.keras.layers.Dense(32, activation='relu'), # hidden layer nr1. Relu is het NN trainingsproces koppeld gewichten aan de output.
  tf.keras.layers.Dense(32, activation='relu'), # hidden layer nr2.
  tf.keras.layers.Dense(16, activation='relu'), # hidden layer nr3.
  tf.keras.layers.Dense(1)   # output; 1 x stuurhoek.
])

model.compile(optimizer='adam',   # Adam is een vervanger van gradient decent met als voordeel deze minder 'snel' blijft hangen tussen bepaalde waarde. 
  loss=tf.keras.losses.MeanSquaredError(),  # De loss functie verteld hoeveel de voorspelde output in het model verschilt met de 'echte' output. 
  metrics=['accuracy'])

# Trainen model
model.fit(sonarData, sonarSteeringAngle, epochs=150)

print()
print('Evaluation:')
model.evaluate(sonarDataVal, sonarSteeringAngleVal)
print()

# model.save('/Users/boyfrankclaesen/MakeAIWork/simulations/car/control_client/s_tf_model')

#plot
predictions = model.predict(np.array(sonarDataVal))
plt.figure()
plt.plot(sonarSteeringAngleVal)
plt.plot(predictions, 'r')
plt.show()




'''
#compiler option 2
model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001),
  loss=tf.keras.losses.MeanSquaredError(),
  metrics=['accuracy'])
'''

# use the below code in the drivingAgent.
#model.save('/Users/boyfrankclaesen/MakeAIWork/simulations/car/control_client/s_tf_model')
#predictions = new_model.predict([sonar_data])

#push test

