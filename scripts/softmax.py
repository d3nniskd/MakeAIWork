import math
def softmax(outputs)
	exponentials = []
	for item in outputs:
		exponentials.append(math.exp(item))
	sum_exponentials = sum(exponentials)
	probabilities = []
	for item in exponentials
		probabilities.append(item/sum_exponentials)
	return probabilities

# softmax(8,8)