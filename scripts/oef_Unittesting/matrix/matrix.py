#!/usr/bin/env python

class Matrix:

    def __init__(self, vectorList):
        self.vectorList = vectorList

    def __add__(self, matrix2):
        vectorList2 = matrix2.vectorList
        vectorList3 = [self.addVectors(v1, v2) for (v1, v2) in zip(vectorList1, vectorList2)]
        return Matrix(vectorList3)

    def addVectors(self, v1, v2):
        if len(v1) != len(v2):
            return None
        else:
            v3 = [sum(tup) for tup in zip(v1, v2)]
            return v3

    def multiply(self, matrix2):
        vectorList2 = matrix2.vectorList
        vectorColumn2 = list()

        for i in range(0, len(vectorList2)):
            vectorColumn2.append(vectorList2[i])

        print(vectorColumn2)

        #  columns of matrix2

        vectorList3 = [self.multiplyVectors(v1, v2) for (v1, v2) in zip(vectorList1, vectorColumn2)]
        return Matrix(vectorList3)

    def multiplyVectors(self, v1, v2):
        if len(v1) != len(v2):
            return None
        else:
            v3 = [a*b for (a, b) in zip(v1, v2)]
            return v3

    def __str__(self):
        return f"{self.vectorList}"

vectorList1 = ([1, 1, 1], [1, 1, 1])
vectorList2 = ([1, 2, 3], [4, 5, 6])

matrix1 = Matrix(vectorList1)
matrix2 = Matrix(vectorList2)
matrix3 = matrix1 + matrix2
matrix4 = matrix1.multiply(matrix2)

print(matrix4)
# print(f"Matrix1 {matrix1} + Matrix2 {matrix2} = Matrix3 {matrix3}")
