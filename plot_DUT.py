import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
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
    if Vp_layer==1:
        grid1[Vp_pos1][Vp_pos2] = Node(0.0, Fixed.C)
    else:
        grid2[Vp_pos1][Vp_pos2] = Node(0.0, Fixed.C)
    if Vm_layer==1:
        grid1[Vm_pos1][Vm_pos2] = Node(0.0, Fixed.D)
    else:
        grid2[Vm_pos1][Vm_pos2] = Node(0.0, Fixed.D)

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

def find_cross_boundaries(row1, col1, row2, col2):
    L2l = (col2 - row1)//2
    L2r = L2l + row1 - 1
    L1l = (col1 - row2)//2
    L1r = L1l + row2 - 1
    cross = [L1l, L1r, L2l, L2r]
    return cross

row1, col1, row2, col2, R_top, R_bot, R_cross_range, Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2, CONVERGENCE_THRESHOLD, max_iter, append = parse('input.dat')
