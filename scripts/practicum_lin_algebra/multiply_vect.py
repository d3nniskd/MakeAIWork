# start met definieren van 2 3x3 matrices
matr1 = [[1,2,3],[4,5,6],[7,8,9]]
matr2 = [[2,2,3],[1,5,6],[7,1,3]]

print (type(matr1))
# hoe halen we nu het aantal rijen en kolommen uit de lists?
# voor rowIndex --> range(len(matr1))
# voor column Index --> range(len(matr2[0]))

print(len(matr1))
print(len(matr2[0]))

rowIndex = range(len(matr1))
columnIndex = range(len(matr2[0]))

print(rowIndex)
print(columnIndex)

# nu een loopje waarin de som van de producten wordt gemaakt
# eerst nog een resultmatrix anmaken
matr3 = [[0,0,0],[0,0,0],[0,0,0]]
print (type(matr3))

# voorbeeld code van frank
# for rowIndex in range(len(matrix_A)):
#     for columnIndex in range(len(matrix_B[0])):
#         for termIndex in range(len(matrix_A[0])):
#             result[rowIndex][columnIndex] += matrix_A[rowIndex][termIndex] * matrix_B[termIndex][columnIndex]
            
# for row in result:
#     print(row)

for rowIndex in range(len(matr1)):
    for columnIndex in range(len(matr2[0])):
        for termIndex in range(len(matr1[0])):
            matr3[rowIndex][columnIndex] += matr1[rowIndex][termIndex] * matr2[termIndex][columnIndex]
            
for row in matr3:
    print(row)