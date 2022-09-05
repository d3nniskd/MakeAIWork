# wat hebben we nodig voor optellen van vectoren?
# lists om de vectoren in op te slaan
# 
# het kan ook met numpy

# import numpy

vector1 = [0,3,1]
vector2 = (1,4,7)

# print('the 2 vectors are :\n','vector1:',vector1 ,'\n', 'vector2:',vector2)

# somvector= NumPy.add(vector1,vector2)
# print('De som van beide vectoren is: ',[somvector])

print('hallo')
print(type(vector1))
print(type(vector2))

# vector2 even opnieuw definieren als list
vector2 = [1,4,7]

# eerst de simpele oplossing: per index optellen

# print(vector1.index(0))
desom = [vector1[0] + vector2[0], vector1[1] + vector2[1], vector1[2] + vector2[2]]
print (desom)

# ok die doet het, en nou nog via 'append' met een loopje

res_list = []
for i in range(0, len(vector1)):
    res_list.append(vector1[i] + vector2[i])
  
print ("Resultant list is : " + str(res_list))

# de oplosseing van jeroen:
# def addVectors(v1, v2):
#     # start met lege vector
#     resultaat = []
    
#     # voor elke rij
#     for i 
    
# v1 = list[1, 2]
# v2 = list[2, 1]
# w = addVectors(v1, v2)
