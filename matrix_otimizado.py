import pyximport
pyximport.install(language_level = 3)

from math import cos, sin
from testec import mult_v, mult_m, mult_m_v, mult_v_v
from random import random

class Vector():
    __slots__ = ("vector", "resp")
    """
    Define um vetor com certas propriedades.
    Uma observação importante é que não existe vetor transposto nessa engine.
    """
    def __init__(self, vector):
        """
        Para iniciar um vetor você precissa passar uma lista ou tupla.
        """
        self.vector = tuple(vector)
        self.resp = []

    def __add__(self, obj):
        """
        Soma e retorna um novo vetor.
        Você pode passar um vetor de tamanho igual ou um valor unico se preferir.
        """
        self.resp = []

        if type(obj) == Vector:
            if len(self.vector) == len(obj.vector):
                for i in range(len(self.vector)):
                    self.resp.append(self.vector[i] + obj.vector[i])
                return Vector(self.resp)
            
            print("The width of the vectors is not equal")

        elif type(obj) == float or type(obj) == int:
            for i in range(len(self.vector)):
                self.resp.append(self.vector[i] + obj)
            return Vector(self.resp)
                
    def __sub__(self, obj):
        """
        Subtrai e retorna um novo vetor.
        Você pode passar um vetor de tamanho igual ou um valor unico se preferir.
        """
        self.resp = []

        if type(obj) == Vector:
            if len(self.vector) == len(obj.vector):
                for i in range(len(self.vector)):
                    self.resp.append(self.vector[i] - obj.vector[i])
                return Vector(self.resp)                
        
            print("The width of the vectors is not equal")

        elif type(obj) == float or type(obj) == int:
            for i in range(len(self.vector)):
                self.resp.append(self.vector[i] - obj)
            return Vector(self.resp)

    def __mul__(self, obj):
        """
        Faz uma multiplicação, ele entende quando é um escalar, multiplicação de vetores ou multiplicação de matrizes.
        """
        self.resp = []

        if type(obj) == Vector:
##            if len(self.vector) == len(obj.vector):
##                for i in range(len(self.vector)):
##                    self.resp.append(self.vector[i] * obj.vector[i])
##                return Vector(self.resp)
            return Vector(mult_v(self.vector, obj.vector))
        
##            print("The width of the vectors is not equal")

        if type(obj) == Matrix:
            return (obj.__invert__()).__mul__(self.__invert__())
        
        if type(obj) == float or type(obj) == int:
            for i in range(len(self.vector)):
                self.resp.append(self.vector[i] * obj)

            return Vector(self.resp)

        if type(obj) == list or type(obj) == tuple:
            obj = Vector(obj)
            if len(self.vector) == len(obj.vector):
                for i in range(len(self.vector)):
                    self.resp.append(self.vector[i] * obj.vector[i])
                return Vector(self.resp)                
        
            print("The width of the vectors is not equal")
            
    def __truediv__(self, obj):
        """
        Faz uma divisão, ele entende quando é um escalar ou multiplicação de vetores.
        """
        self.resp = []
        
        if type(obj) == float or type(obj) == int:
            for i in range(len(self.vector)):
                self.resp.append(self.vector[i]/obj)

            return Vector(self.resp)

        if type(obj) == Vector:
            if len(self.vector) == len(obj.vector):
                for i in range(len(self.vector)):
                    self.resp.append(self.vector[i]/obj.vector[i])
                return Vector(self.resp)                
        
            print("The width of the vectors is not equal")

    def __neg__(self):
        """
        Inverte vetor.
        """
        self.resp = []

        for i in range(len(self.vector)):
            self.resp.append(-self.vector[i]) 

        return Vector(self.resp)

    def __invert__(self):
        """
        Transpõe a matriz.
        """
        self.resp = []
        for i in range(len(self.vector)):
            self.resp.append([self.vector[i]])
            
        return Matrix(self.resp)

    def __len__(self):
        """
        Obtem o tamanho do vetor
        """
        return len(self.vector)

    def __eq__(self, obj):
        """
        Compara se é igual
        """
        if len(self.vector) == len(obj.vector) and type(obj) == Vector:
            for i in range(len(self.vector)):
                if float(self.vector[i]) != float(obj.vector[i]):
                    return False
            return True
        print("The width of the vectors is not equal")

    def __getitem__(self,index):
        """
        Obtem um valor do vetor
        """
        if type(index) == int:
            return self.vector[index]

    def __repr__(self):
        """
        Representação do vetor.
        """
        return str(self.vector)


class Matrix():
    """
    Define uma matriz.
    Uma matriz é uma tupla de vetores.
    """
    __slots__ = ("matrix", "resp")
    def __init__(self, matrix):
        """
        Para iniciar um vetor você precissa passar uma tuplas de tuplas ou listas de listas.
        """
        self.matrix = []
        for i in range(len(matrix)):
            self.matrix.append(Vector(matrix[i]))
        self.matrix = tuple(self.matrix)
        
        self.resp = []

    def __add__(self, obj):
        """
        Soma e retorna uma nova matriz.
        Você pode passar uma matriz de tamanho igual ou um valor unico se preferir.
        """
        self.resp = []

        if type(obj) == Matrix:
            if len(self.matrix) == len(obj.matrix[0].vector) and len(self.matrix[0].vector) == len(obj.matrix):
                for i in range(len(self.matrix)):
                    temp = []
                    for j in range(len(self.matrix[0])):
                        temp.append(self.matrix[i].vector[j] + obj.matrix[i].vector[j])
                    self.resp.append(temp)
                return Matrix(self.resp)
            
            print("The width of the matrix is not equal")

        elif type(obj) == float or type(obj) == int:
            for i in range(len(self.matrix)):
                temp = []
                for j in range(len(self.matrix[0])):
                    temp.append(self.matrix[i].vector[j] + obj)
                self.resp.append(temp)
            return Matrix(self.resp)
                
    def __sub__(self, obj):
        """
        Subtrai e retorna uma nova matriz.
        Você pode passar uma matriz de tamanho igual ou um valor unico se preferir.
        """
        self.resp = []

        if type(obj) == Matrix:
            if len(self.matrix) == len(obj.matrix) and len(self.matrix[0].vector) == len(obj.matrix[0].vector):
                for i in range(len(self.matrix)):
                    temp = []
                    for j in range(len(self.matrix[0])):
                        temp.append(self.matrix[i].vector[j] - obj.matrix[i].vector[j])
                    self.resp.append(temp)
                return Matrix(self.resp)
            
            print("The width of the matrix is not equal")

        elif type(obj) == float or type(obj) == int:
            for i in range(len(self.matrix)):
                temp = []
                for j in range(len(self.matrix[0])):
                    temp.append(self.matrix[i].vector[j] - obj)
                self.resp.append(temp)
            return Matrix(self.resp)

    def __mul__(self, obj):
        """
        Faz uma multiplicação, ele entende quando é um escalar, multiplicação de vetores ou multiplicação de matrizes.
        """
        self.resp = []

        if type(obj) == Matrix:
##            if len(self.matrix[0].vector) == len(obj.matrix):
##                for i in range(len(self.matrix)):
##                    temp = []
##                    for j in range(len(obj.matrix[0])):
##                        numb = 0
##                        for k in range(len(self.matrix[0])):
##                            numb += self.matrix[i].vector[k] * obj.matrix[k].vector[j]
##                        temp.append(numb)
##                    self.resp.append(temp)
##                return Matrix(self.resp)
            return Matrix(mult_m(self.matrix, obj.matrix))
        
            print("The width of the matrix is not equal")

        if type(obj) == Vector:
            if len(self.matrix[0].vector) == len(obj.vector):
                for i in range(len(self.matrix)):
                    self.resp.append(mult_v_v(self.matrix[i].vector, obj.vector))
                return Vector(self.resp)
            print("The width of the matrix is not equal")

        if type(obj) == float or type(obj) == int:
            for i in range(len(self.matrix)):
                temp = []
                for j in range(len(self.matrix[0])):
                    temp.append(self.matrix[i].vector[j] * obj)
                self.resp.append(temp)
                
            return Matrix(self.resp)

        if type(obj) == list or type(obj) == tuple:
            obj = Vector(obj)
            if len(self.matrix[0].vector) == len(obj.vector):
                for i in range(len(self.matrix)):
                    numb = 0
                    for j in range(len(self.matrix[0])):
                        numb += self.matrix[i].vector[j] * obj.vector[j]
                    self.resp.append(numb)
                return Vector(self.resp)

    def __neg__(self):
        """
        Inverte a matriz.
        """
        self.resp = []

        for i in range(len(self.matrix)):
            temp = []
            for j in range(len(self.matrix)):
                temp.append(-self.matrix[i].vector[j])
            self.resp.append(temp)

        return Matrix(self.resp)        

    def __getitem__(self,index):
        """
        Obtem um valor da matriz
        """
        if type(index) == int:
            return self.matrix[index]
        if type(index) == tuple and len(index) == 2:
            return self.matrix[index[0]][index[1]]

    #def __len__(self):
    #    print(str(len(self.matrix))+"x"+str(len(self.matrix[0].vector)))
    #    return len(self.matrix)

    def __invert__(self):
        """
        Transpõe a matriz.
        """
        self.resp = [[0 for i in range(len(self.matrix))] for j in range(len(self.matrix[0]))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.resp[j][i] = self.matrix[i].vector[j]
            
        return Matrix(self.resp)

    def __repr__(self):
        """
        Representação da matriz.
        """
        return str(self.matrix)

    def __str__(self):
        """
        Printa a matrix.
        """
        for i in range(len(self.matrix)):
            print(self.matrix[i])
        return ""

if __name__ == "__main__":
    a = Vector([1,2,3])
    b = Vector([10,30,50])

    h = Matrix([[1,2,3],[4,5,6],[7,8,9]])
    n = Matrix([[10,20,30],[40,50,60],[70,80,90]])

    o = Matrix([[1,2,3],[4,5,6]])
    p = Matrix([[1,2],[3,4],[5,6]])

    from time import time

    k = time()
    for i in range(1000000):
        h.__mul__(a)

    k_ = time()

    print(k_ - k)

