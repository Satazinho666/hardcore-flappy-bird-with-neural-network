import numpy as np
import random as rd
import math
import decimal
from decimal import *

MUTATION_RATE = 0.7
MUTATION_IMPACT = 0.01
REQUIREMENT = 0.5

def lg(x):
    '''
        Logistic function to map real line into (0,1) interval
    '''
    return float(1/(1+np.exp(Decimal(-x))))

class AI:
    def __init__(self):
        arr = np.zeros((2,2,2))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    arr[i,j,k]=Decimal(rd.uniform(-10,10))
        self.weigth = arr #matrix of weights of the values received by each
                           #neuron. weigths[i,j,k] is the weigth of the k-th
                           #neuron of the (j-1)-th layer given by the i-th n
                           #euron of the i-th layer
    

    def N1_L1(self,v1,v2):
        return lg(self.weigth[0,0,0]*v1 + self.weigth[0,0,1]*v2)

    def N2_L1(self,v1,v2):
        return lg(self.weigth[1,0,0]*v1 + self.weigth[1,0,1]*v2)

    def N1_L2(self,v1,v2):
        return lg(self.weigth[0,1,0]*v1 + self.weigth[0,1,1]*v2)

    def Output(self,inp0,inp1):
        final_input = (self.N1_L1(inp0,inp1),self.N2_L1(inp0,inp1))
        if self.N1_L2(final_input[0],final_input[1])>REQUIREMENT:
            return True
        else:
            return False

    def mutation(self):
        r = rd.random()
        if r < MUTATION_RATE: 
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        mutation_in_ijk = rd.random()
                        if mutation_in_ijk<MUTATION_IMPACT:
                            # mutation_factor = 1.5*rd.uniform(-1,1)
                            w = self.weigth.shape[0]
                            h = self.weigth.shape[1]
                            mutation_factor = 1.5 * (2*np.random.rand(w, h)-1)
                            self.weigth += mutation_factor
