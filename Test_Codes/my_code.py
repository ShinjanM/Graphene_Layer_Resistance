import numpy as np
from mpi4py import MPI
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt

class Fixed:
    FREE = 0 
    A = 1 
    B = 2

class Node:
    __slots__ = ["voltage", "fixed"]
    def __init__(self, v=0.0, f=Fixed.FREE):
        self.voltage = v
        self.fixed = f

def set_boundary(grid):
    grid[2][3] = Node(1.0, Fixed.A)
    grid[6][7] = Node(-1.0, Fixed.B)

def V_mn(m,n,grid,row,col,R_vert,R_hor):
    if grid[m][n].fixed == Fixed.FREE:
        Vmn = 0
        R_inv = 0.0
        if m!=0: 
            Vmn += grid[m-1][n].voltage / 2.0 #Resistance[m-1][n]
            R_inv += 1/2.0 # Resistance[m-1][n]
        if n!=0:
            Vmn += grid[m][n-1].voltage / 2.0 #Resistance[m][n-1]
            R_inv += 1/2.0 # Resistance[m][n-1]
        if m<row-1:
            Vmn += grid[m+1][n].voltage / 2.0 #Resistance[m+1][n]
            R_inv += 1/2.0 # Resistance[m+1][n]
        if n<col-1:
            Vmn += grid[m][n+1].voltage / 2.0 #Resistance[m][n+1]
            R_inv += 1/2.0 # Resistance
        Vmn = Vmn/R_inv
        diff = (grid[m][n].voltage - Vmn)
        grid[m][n].voltage = Vmn
    else:
        diff = 0
    return diff


def current_grid(grid,R_vert,R_hor):
    current = np.zeros(np.shape(grid))
    for i in range(np.shape(grid)[0]):
        for j in range(np.shape(grid)[1]):
            if i!=0: current[i][j] += (grid[i][j].voltage - grid[i-1][j].voltage)/2.0
            if j!=0: current[i][j] += (grid[i][j].voltage - grid[i][j-1].voltage)/2.0
            if i<np.shape(grid)[0]-1: current[i][j] += (grid[i][j].voltage - grid[i+1][j].voltage)/2.0
            if j<np.shape(grid)[1]-1: current[i][j] += (grid[i][j].voltage - grid[i][j+1].voltage)/2.0
    plt.matshow(current,interpolation='spline36',cmap='inferno')
    plt.colorbar()
    plt.title('Current in the circuit')
    plt.show()
    return current

def iterations(number_of_iterations, grid, R_vert, R_hor):
    row = np.shape(grid)[0]
    col = np.shape(grid)[1]
    for i in range(number_of_iterations):
        diff = 0
        for p in range(row):
            for q in range(col):
                if (p+q)%2 == 0:
                    diff += V_mn(p,q,grid,row,col,R_vert,R_hor)
        for p in range(row):
            for q in range(col):
                if (p+q)%2 != 0:
                    diff += V_mn(p,q,grid,row,col,R_vert,R_hor)
    return

def resistance(number_of_iterations, grid, R_vert, R_hor):
    iterations(number_of_iterations, grid, R_vert, R_hor)
    current = current_grid(grid, R_vert, R_hor)
    curA, curB = 0.0, 0.0
    for i in range(np.shape(grid)[0]):
        for j in range(np.shape(grid)[1]):
            if grid[i][j].fixed == Fixed.A: curA += current[i][j]
            if grid[i][j].fixed == Fixed.B: curB += current[i][j]
    cur = curA - curB
    res = 2/cur
    return res


m = 10
n = 10
mesh = [[Node() for j in range(m)] for i in range(n)]
set_boundary(mesh)
final = resistance(30000,mesh,0,0)
V = np.empty((n,m))
for i in range(m):
    for j in range(n):
        V[j][i] = mesh[j][i].voltage

plt.matshow(V,interpolation='spline36')
plt.colorbar()
plt.title('Voltage Distribution')
plt.show()
print("Resistance = ",final)

