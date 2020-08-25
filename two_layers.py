import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt

class Fixed:
    FREE = 0
    A = 1
    B = 2

class Node:
    __slots__ = ["voltage","fixed"]
    def __init__(self, v=0.0, f=Fixed.FREE):
        self.voltage = v
        self.fixed = f

def set_boundary(grid1,grid2):
    grid1[0][0] = Node(1.0, Fixed.A)
    grid2[0][0] = Node(-1.0, Fixed.B)

def V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary):
    """
        m : Row
        n : Column
        p : Layer number
        grid1 : The entire grid of Voltages at each lattice point in layer 1
        grid2 : The entire grid of Voltages at each lattice point in layer 2
        row1: number of rows in layer 1
        col1: number of columns in layer 1
        row2: number of rows in layer 2
        col2: number of columns in layer 2
        R_top : Resistance of top layer
        R_bot : Resistance of bottom layer
        R_cross : Resistance of the cross section
        cross_boundary : [layer1_left, layer1_right, layer2_left, layer2_right]
    """
    Vmnp = 0
    R_inv = 0.0
    if p==0:
        if grid1[m][n].fixed == Fixed.FREE:
            if m!=0:
                Vmnp += grid1[m-1][n].voltage / R_top
                R_inv += 1/R_top
            if n!=0:
                Vmnp += grid1[m][n-1].voltage / R_top
                R_inv += 1/R_top
            if m<(row1-1):
                Vmnp += grid1[m+1][n].voltage / R_top
                R_inv += 1/R_top
            if n<(col1-1):
                Vmnp += grid1[m][n+1].voltage /R_top
                R_inv += 1/R_top
            if ((n>=cross_boundary[0]) and (n<=cross_boundary[1])):
                layer2_position_1 = n - cross_boundary[0]
                layer2_position_2 = cross_boundary[3] - m
                Vmnp += grid2[layer2_position_1][layer2_position_2].voltage / R_cross
                R_inv += R_cross
            Vmnp = Vmnp/R_inv
            diff = abs(grid1[m][n].voltage - Vmnp)
            grid1[m][n].voltage = Vmnp
        else:
            diff = 0
    if p==1:
        if grid2[m][n].fixed == Fixed.FREE:
            if m!=0:
                Vmnp += grid2[m-1][n].voltage / R_bot
                R_inv += 1/R_bot
            if n!=0:
                Vmnp += grid2[m][n-1].voltage / R_bot
                R_inv += 1/R_bot
            if m<(row2-1):
                Vmnp += grid2[m+1][n].voltage / R_bot
                R_inv += 1/R_bot
            if n<(col2-1):
                Vmnp += grid2[m][n+1].voltage /R_bot
                R_inv += 1/R_bot
            if ((n>=cross_boundary[2]) and (n<=cross_boundary[3])):
                layer1_position_1 = cross_boundary[3] - n
                layer1_position_2 = m + cross_boundary[0] - 1
                print(layer1_position_1, layer1_position_2)
                Vmnp += grid1[layer1_position_1][layer1_position_2].voltage / R_cross
                R_inv += R_cross
            Vmnp = Vmnp/R_inv
            diff = abs(grid2[m][n].voltage - Vmnp)
            grid2[m][n].voltage = Vmnp
        else:
            diff = 0
    return diff


def current_grid(grid1,grid2,cross_boundary,R_bot,R_top,R_cross):
    row1, col1 = np.shape(grid1)[0], np.shape(grid1)[1]
    row2, col2 = np.shape(grid2)[0], np.shape(grid2)[1]
    current1 = np.zeros(np.shape(grid1))
    current2 = np.zeros(np.shape(grid2))
    for m in range(row1):
        for n in range(col1):
            if m!=0: current1[m][n] += (grid1[m][n].voltage - grid1[m-1][n].voltage)/R_top
            if n!=0: current1[m][n] += (grid1[m][n].voltage - grid1[m][n-1].voltage)/R_top
            if m<row1-1: current1[m][n] += (grid1[m][n].voltage - grid1[m+1][n].voltage)/R_top
            if n<col1-1: current1[m][n] += (grid1[m][n].voltage - grid1[m][n+1].voltage)/R_top
            if ((n>=cross_boundary[0]) and (n<=cross_boundary[1])):
                current1[m][n] += (grid1[m][n].voltage - grid2[n-cross_boundary[0]][cross_boundary[3]-m].voltage)/R_cross
    for m in range(row2):
        for n in range(col2):
            if m!=0: current2[m][n] += (grid2[m][n].voltage - grid2[m-1][n].voltage)/R_bot
            if n!=0: current2[m][n] += (grid2[m][n].voltage - grid2[m][n-1].voltage)/R_bot
            if m<row2-1: current2[m][n] += (grid2[m][n].voltage - grid2[m+1][n].voltage)/R_bot
            if n<col2-1: current2[m][n] += (grid2[m][n].voltage - grid2[m][n+1].voltage)/R_bot
            if ((n>=cross_boundary[2]) and (n<=cross_boundary[3])):
                current2[m][n] += (grid2[m][n].voltage - grid1[cross_boundary[3]-n][cross_boundary[0]+m].voltage)/R_cross
    return current1, current2


def iterations(number_of_iterations, grid1, grid2, cross_boundary, R_top, R_bot, R_cross):
    row1, col1 = np.shape(grid1)[0], np.shape(grid1)[1]
    row2, col2 = np.shape(grid2)[0], np.shape(grid2)[1]
    for i in range(number_of_iterations):
        diff = 0
        p = 0
        for m in range(row1):
            for n in range(col1):
                if (m+n)%2 == 0:
                    diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
        for m in range(row1):
            for n in range(col1):
                if (m+n)%2 != 0:
                    diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
        p = 1
        for m in range(row2):
            for n in range(col2):
                if (m+n)%2 == 0:
                    diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
        for m in range(row2):
            for n in range(col2):
                if (m+n)%2 != 0:
                    diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
    if (i+1)%100==0:
        print("Step {} with diff = {1:.8f}%".format(i,diff))
    return

def resistance(num_iter, grid1, grid2, cross, R_top, R_bot, R_cross):
    iterations(num_iter, grid1, grid2, cross, R_top, R_bot, R_cross)
    I1, I2 = current_grid(grid1,grid2,cross,R_bot,R_top,R_cross)
    curA, curB = 0.0, 0.0
    for i in range(np.shape(grid1)[0]):
        for j in range(np.shape(grid1)[1]):
            if grid1[i][j].fixed == Fixed.A: curA += current[i][j]
            if grid1[i][j].fixed == Fixed.B: curB += current[i][j]
    for i in range(np.shape(grid2)[0]):
        for j in range(np.shape(grid2)[1]):
            if grid2[i][j].fixed == Fixed.A: curA += current[i][j]
            if grid2[i][j].fixed == Fixed.B: curB += current[i][j]
    cur = curA - curB
    res = 2/cur
    return res
              

def find_cross(row1, col1, row2, col2):
    L2l = (col2 - row1)//2  
    L2r = L2l + row1 - 1 
    L1l = (col1 - row2)//2 
    L1r = L1l + row2 - 1
    cross = [L1l, L1r, L2l, L2r] 
    return cross
        


row1 = 2
col1 = 4 
row2 = 1
col2 = 4

R_top   = 1
R_bot   = 2
R_cross = 1

layer1 = [[Node() for i in range(col1)] for j in range(row1)]
layer2 = [[Node() for i in range(col2)] for j in range(col2)]

set_boundary(layer1,layer2)
cross = [2,2,1,2]
print(cross)
final_resistance = resistance(10000, layer1, layer2, cross, R_top, R_bot, R_cross)