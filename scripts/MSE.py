# Mean squared error
import math

def loss_funtion (probs, label): # checked hoe ver we van de waarheid (=label) zitten
	loss = 0 # not in for loop, anders blijf je die overschrijven
	if len(probs) != len(labels):
		raise IndexError("labels en probabilities zijn niet even lang")
	for i in range(len(probs)): # we kiezen nu voor index ipv item. Dit is makkelijk omdat we dan beide lijsten kunnen doorlopen. We hadden hier misschien ook zip-functie kunnen gebruiken
		error = labels[i], probs[i]
	squared_err = error**2
	loss += squared_error
	return loss
		
outputs = [9, 7]		
labels = [1,0] # = kruisje
probs = [0.8, 0.2] # probabilities uit de softmax
	
print(loss_function(probe, labels))