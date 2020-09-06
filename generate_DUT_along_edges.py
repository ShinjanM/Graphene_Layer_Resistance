import numpy as np
from parse_input import parse

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

def set_boundary(grid1,grid2,Ip_layer,Ip_pos1,Ip_pos2,Im_layer,Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2):
    if Ip_layer==1:
        grid1[Ip_pos1][Ip_pos2] = Node(10.0, Fixed.A)
    else:
        grid2[Ip_pos1][Ip_pos2] = Node(10.0, Fixed.A)
    if Im_layer==1:
        grid1[Im_pos1][Im_pos2] = Node(0.0, Fixed.B)
    else:
        grid2[Im_pos1][Im_pos2] = Node(0.0, Fixed.B)

def set_probes(grid1,grid2,Ip_layer,Ip_pos1,Ip_pos2,Im_layer,Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2):
    if Vp_layer==1:
        grid1[Vp_pos1][Vp_pos2].fixed = Fixed.C
    else:
        grid2[Vp_pos1][Vp_pos2].fixed = Fixed.C
    if Vm_layer==1:
        grid1[Vm_pos1][Vm_pos2].fixed = Fixed.D
    else:
        grid2[Vm_pos1][Vm_pos2].fixed = Fixed.D

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

def resistance(num_iter, grid1, grid2, cross, R_top, R_bot, R_cross):
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

def find_cross_boundaries(row1, col1, row2, col2):
    L2l = (col2 - row1)//2
    L2r = L2l + row1 - 1
    L1l = (col1 - row2)//2
    L1r = L1l + row2 - 1
    cross = [L1l, L1r, L2l, L2r]
    return cross

row1, col1, row2, col2, R_top, R_bot, R_cross_range, Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2, CONVERGENCE_THRESHOLD, max_iter, append = parse('input.dat')

cross = find_cross_boundaries(row1, col1, row2, col2)

R_cross = 2000
V1 = np.loadtxt('V1_2000_run3_restart.txt')
V2 = np.loadtxt('V2_2000_run3_restart.txt')

#d_mat = np.zeros((col1-cross[1]-1,col2-cross[3]-1))
#d_mat=np.zeros((row1,row2))
#d_mat = np.zeros((row1,col2-cross[3]-1))
d_mat = np.zeros((col1-cross[1]-1,row2))
layer1 = [[Node() for p in range(col1)] for q in range(row1)]
layer2 = [[Node() for p in range(col2)] for q in range(row2)]
set_boundary(layer1,layer2,Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2)
for k in range(row1):
    for l in range(col1):
        layer1[k][l].voltage = V1[k][l]
for k in range(row2):
    for l in range(col2):
        layer2[k][l].voltage = V2[k][l]

for i in range(cross[1]+1,col1):
#for i in range(row1):
    Vp_pos1 = 19
    Vp_pos2 = i
#    for j in range(cross[3]+1,col2):
    for j in range(row2):
        Vm_pos1 = j
        Vm_pos2 = 79
        set_probes(layer1,layer2,Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2)
        final_resistance, curA, curB, Vplus, Vminus = resistance(max_iter, layer1, layer2, cross, R_top, R_bot, R_cross)
        DUT = (Vplus-Vminus)/curA
        #d_mat[i-cross[1]-1][j-cross[3]-1] = DUT
        #d_mat[i][j] = DUT
        #d_mat[i][j-cross[3]-1] = DUT
        d_mat[i-cross[1]-1][j] = DUT
        if Vp_layer==1:
            layer1[Vp_pos1][Vp_pos2].fixed = Fixed.FREE
        else:
            layer2[Vp_pos1][Vp_pos2].fixed = Fixed.FREE
        if Vm_layer==1:
            layer1[Vm_pos1][Vm_pos2].fixed = Fixed.FREE
        else:
            layer2[Vm_pos1][Vm_pos2].fixed = Fixed.FREE
        print(i,j,DUT)
np.savetxt("DUT_9.txt",d_mat)

