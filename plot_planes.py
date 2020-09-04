import matplotlib
matplotlib.use('tkagg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from parse_input import parse

row1, col1, row2, col2, R_top, R_bot, R_cross_range, Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2, CONVERGENCE_THRESHOLD, max_iter,append = parse('input.dat')

def find_cross_boundaries(row1, col1, row2, col2):
    L2l = (col2 - row1)//2
    L2r = L2l + row1 - 1
    L1l = (col1 - row2)//2
    L1r = L1l + row2 - 1
    cross = [L1l, L1r, L2l, L2r]
    return cross


for R_cross in R_cross_range:
    V1 = np.loadtxt('V1_%03d'%R_cross+append+'_restart.txt')
    V2 = np.loadtxt('V2_%03d'%R_cross+append+'_restart.txt')
   
    spacing = 12

    X1 = [i for i in range(col1)]
    Y1 = [i for i in range((col2-row1)//2+row1,(col2-row1)//2,-1)]
    x1,y1 = np.meshgrid(X1,Y1)
    X2 = [i for i in range((col1-row2)//2,(col1-row2)//2+row2)]
    Y2 = [i for i in range(col2)]
    x2,y2 = np.meshgrid(X2,Y2)
    fig = plt.figure()
    ax2 = fig.add_subplot(1,1,1)
    X1 = [i for i in range(col1)]
    Y1 = [i for i in range((col2-row1)//2+row1,(col2-row1)//2,-1)]
    x1,y1 = np.meshgrid(X1,Y1)
    X2 = [i for i in range(col1+spacing,col1+row2+spacing)]
    Y2 = [i for i in range(col2)]
    x2,y2 = np.meshgrid(X2,Y2)
    
    cross_boundary = find_cross_boundaries(row1, col1, row2, col2)
    if Ip_layer==1:
        plt.text(Ip_pos2-8,(col2-row1)//2+row1-Ip_pos1,r'I$^+$',fontsize=25)
    else:
        plt.text(Ip_pos1+spacing+col1-1.5,Ip_pos2-3,r'I$^+$',fontsize=25)

    if Im_layer==1:
        plt.text(Im_pos2-8,(col2-row1)//2+row1-Im_pos1,r'I$^-$',fontsize=25)
    else:
        plt.text(Im_pos1+spacing+col1-1.5,Im_pos2-7,r'I$^-$',fontsize=25)

    if Vp_layer==1:
        ax2.text(Vp_pos2,(col2-row1)//2+row1-Vp_pos1,r'V$^+$', fontsize=25)
        ax2.plot(Vp_pos2,(col2-row1)//2+row1-Vp_pos1,'ro',c='k')
    else:
        ax2.text(Vp_pos1+spacing+col1,Vp_pos2,r'V$^+$', fontsize=25)
        ax2.plot(Vp_pos1+spacing+col1,Vp_pos2,'ro',c='k')

    if Vm_layer==1:
        ax2.text(Vm_pos2,(col2-row1)//2+row1-Vm_pos1,r'V$^-$', fontsize=25)
        ax2.plot(Vm_pos2,(col2-row1)//2+row1-Vm_pos1,'ro',c='k')
    else:
        ax2.text(Vm_pos1+spacing+col1,Vm_pos2,r'V$^-$',fontsize=25)
        ax2.plot(Vm_pos1+spacing+col1,Vm_pos2,'ro',c='k')
    
    levels = np.arange(-0.015,10.015,0.005)+0.005

    p1 = ax2.contourf(x1,y1,V1,levels,alpha=0.8,cmap='twilight_shifted',antialiased=True)
    rect1 = patches.Rectangle(( cross_boundary[0], (col2-row1)//2+1),cross_boundary[1]-cross_boundary[0],row1-1,linewidth=1,edgecolor='k',facecolor='None')
    ax2.add_patch(rect1)
    p2 = ax2.contourf(x2,y2,V2.T,levels,alpha=0.8,cmap='twilight_shifted',antialiased=True)
    rect2 = patches.Rectangle((spacing+col1,(col2-row1)//2+1),row2-1,cross_boundary[3]-cross_boundary[2],linewidth=1,edgecolor='k',facecolor='None')
    ax2.add_patch(rect2)
    ax2.axis('off')
    ax2.set_ylim(0,col2+1)
    ax2.set_xlim(0,col1+row2+spacing+5)
    ax2.set_aspect('equal')
    cbar_ax = fig.add_axes([0.89, 0.15, 0.05, 0.7])
    fig.colorbar(p1,cax=cbar_ax,ticks=np.array([0,2,4,6,8,10]))
    plt.show()
