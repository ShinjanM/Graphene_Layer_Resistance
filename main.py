import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt

CONVERGENCE_THRESHOLD = 1e-8

class Fixed:
    FREE = 0
    A = 1
    B = 2
    C = 3
    D = 4

class Node:
    __slots__ = ["voltage","fixed"]
    def __init__(self, v=0.0, f=Fixed.FREE):
        self.voltage = v
        self.fixed = f

def set_boundary(grid1,grid2):
    grid1[8][0] = Node(10.0, Fixed.A)
    grid2[7][0] = Node(0.0, Fixed.B)
    grid1[3][34] = Node(0.0, Fixed.C)
    grid2[3][29] = Node(0.0, Fixed.D)


def find_cross_boundaries(row1, col1, row2, col2):
    L2l = (col2 - row1)//2  
    L2r = L2l + row1 - 1 
    L1l = (col1 - row2)//2 
    L1r = L1l + row2 - 1
    cross = [L1l, L1r, L2l, L2r] 
    return cross
        


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
        if (grid1[m][n].fixed == Fixed.FREE) or (grid1[m][n].fixed == Fixed.C) or (grid1[m][n].fixed == Fixed.D):
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
                R_inv += 1/R_cross
            Vmnp = Vmnp/R_inv
            diff = abs(grid1[m][n].voltage - Vmnp)
            grid1[m][n].voltage = Vmnp
        else:
            diff = 0
    if p==1:
        if (grid2[m][n].fixed == Fixed.FREE) or (grid2[m][n].fixed == Fixed.C) or (grid2[m][n].fixed == Fixed.D):
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
                layer1_position_2 = m + cross_boundary[0]  
                Vmnp += grid1[layer1_position_1][layer1_position_2].voltage / R_cross
                R_inv += 1/R_cross
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
#    plt.matshow(current1, interpolation='spline36',cmap='inferno')
#    plt.colorbar()
#    plt.show()
    for m in range(row2):
        for n in range(col2):
            if m!=0: current2[m][n] += (grid2[m][n].voltage - grid2[m-1][n].voltage)/R_bot
            if n!=0: current2[m][n] += (grid2[m][n].voltage - grid2[m][n-1].voltage)/R_bot
            if m<row2-1: current2[m][n] += (grid2[m][n].voltage - grid2[m+1][n].voltage)/R_bot
            if n<col2-1: current2[m][n] += (grid2[m][n].voltage - grid2[m][n+1].voltage)/R_bot
            if ((n>=cross_boundary[2]) and (n<=cross_boundary[3])):
                current2[m][n] += (grid2[m][n].voltage - grid1[cross_boundary[3]-n][cross_boundary[0]+m].voltage)/R_cross
#    plt.matshow(current2.T,interpolation='spline36', cmap='inferno',origin='lower')
#    plt.colorbar()
#    plt.show()
    return current1, current2

def iterations(number_of_iterations, grid1, grid2, cross_boundary, R_top, R_bot, R_cross):
    row1, col1 = np.shape(grid1)[0], np.shape(grid1)[1]
    row2, col2 = np.shape(grid2)[0], np.shape(grid2)[1]
    for i in range(number_of_iterations):
        diff = 0
        p = 0
        for m in range(row1):
            for n in range(col1):
                diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
        p = 1
        for m in range(row2):
            for n in range(col2):
                diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
        if (i+1)%1000==0:
            print("Step {} with convergence delta = {}".format(i+1,diff))
        if diff<CONVERGENCE_THRESHOLD:
            print("Step {} with convergence delta = {} has converged".format(i+1,diff))
            break
    return


def resistance(num_iter, grid1, grid2, cross, R_top, R_bot, R_cross):
    iterations(num_iter, grid1, grid2, cross, R_top, R_bot, R_cross)
    I1, I2 = current_grid(grid1,grid2,cross,R_bot,R_top,R_cross)
    curA, curB, volC, volD = 0.0, 0.0, 0.0, 0.0
    for i in range(np.shape(grid1)[0]):
        for j in range(np.shape(grid1)[1]):
            if grid1[i][j].fixed == Fixed.A: curA += I1[i][j]
            if grid1[i][j].fixed == Fixed.B: curB += I1[i][j]
            if grid1[i][j].fixed == Fixed.C: volC = grid1[i][j].voltage
            if grid1[i][j].fixed == Fixed.D: volD = grid1[i][j].voltage
    for i in range(np.shape(grid2)[0]):
        for j in range(np.shape(grid2)[1]):
            if grid2[i][j].fixed == Fixed.A: curA += I2[i][j]
            if grid2[i][j].fixed == Fixed.B: curB += I2[i][j]
            if grid2[i][j].fixed == Fixed.C: volC = grid2[i][j].voltage
            if grid2[i][j].fixed == Fixed.D: volD = grid2[i][j].voltage
    cur = curA - curB
    res = 10/cur
    return res, curA, curB, volC, volD


row1 = 10
col1 = 35
row2 = 18
col2 = 30

R_top   = 10
R_bot   = 12
R_cross = 10

print("--------------------------------------------- ")
print("| Layer 1: {} X {}".format(row1,col1))
print("| Layer 2: {} X {}".format(row2,col2))
print("| R_top: {} Ohms \t R_bot: {} Ohms \t R_cross: {} Ohms".format(R_top,R_bot,R_cross))
print("| Convergence Threshold: ", CONVERGENCE_THRESHOLD)
print("--------------------------------------------- \n")
layer1 = [[Node() for i in range(col1)] for j in range(row1)]
layer2 = [[Node() for i in range(col2)] for j in range(row2)]
set_boundary(layer1,layer2)
cross = find_cross_boundaries(row1, col1, row2, col2)

final_resistance, curA, curB, Vplus, Vminus = resistance(500000, layer1, layer2, cross, R_top, R_bot, R_cross)

print("\nThe resistance of the network is %.5f Ohms."%final_resistance)
print("I+ = ", curA)
print("I- = ", curB)
print("V+ = ", Vplus)
print("V- = ", Vminus)
print("DUT Resistance = ", (Vplus-Vminus)/curA)

V1, V2 = np.empty((row1,col1)), np.empty((row2,col2))
for i in range(row1):
    for j in range(col1):
        V1[i][j] = layer1[i][j].voltage
for i in range(row2):
    for j in range(col2):
        V2[i][j] = layer2[i][j].voltage

X1 = [i for i in range(col1)]
Y1 = [i for i in range((col2-row1)//2+row1,(col2-row1)//2,-1)]
x1,y1 = np.meshgrid(X1,Y1)
spacing = 10
X2 = [i for i in range(col1+spacing,col1+row2+spacing)]
Y2 = [i for i in range(col2)]
x2,y2 = np.meshgrid(X2,Y2)

levels = np.arange(-0.005,10.015,0.005)+0.005
plt.contourf(x1,y1,V1,levels,alpha=0.8,cmap='twilight_shifted')
plt.contourf(x2,y2,V2.T,levels,alpha=0.8,cmap='twilight_shifted')
plt.colorbar()
plt.axis('off')
plt.text(-5.3, 16.5, r'I$^+$', fontsize=25)
plt.text(46.5, -2.5, r'I$^-$', fontsize=25)
plt.text(34.5,14,r'V$^+$', fontsize=25)
plt.text(49, 30.3, r'V$^-$', fontsize=25)
#plt.title("Voltage Distribution")
#plt.show()
plt.savefig('Voltage_Distribution.png')