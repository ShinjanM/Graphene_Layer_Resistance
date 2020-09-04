import matplotlib
matplotlib.use('tkagg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from parse_input import parse

row1, col1, row2, col2, R_top, R_bot, R_cross_range, Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2, CONVERGENCE_THRESHOLD, max_iter,append = parse('input.dat')


for R_cross in R_cross_range:
    V1 = np.loadtxt('V1_%03d'%R_cross+append+'.txt')
    V2 = np.loadtxt('V2_%03d'%R_cross+append+'.txt')
    
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
    spacing = 20
    X2 = [i for i in range(col1+spacing,col1+row2+spacing)]
    Y2 = [i for i in range(col2)]
    x2,y2 = np.meshgrid(X2,Y2)

    levels = np.arange(-0.015,10.015,0.005)+0.005
    if Ip_layer==1:
        plt.text(Ip_pos2-8,(col2-row1)//2+row1-Ip_pos1,r'I$^+$',fontsize=25)
    else:
        plt.text(Ip_pos1+spacing+col1-1.5,Ip_pos2-3,r'I$^+$',fontsize=25)

    if Im_layer==1:
        plt.text(Im_pos2-8,(col2-row1)//2+row1-Im_pos1,r'I$^-$',fontsize=25)
    else:
        plt.text(Im_pos1+spacing+col1-1.5,Im_pos2-12,r'I$^-$',fontsize=25)

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
    ax2.contourf(x1,y1,V1,levels,alpha=0.8,cmap='hsv',antialiased=True)
    ax2.contourf(x2,y2,V2.T,levels,alpha=0.8,cmap='hsv',antialiased=True)
    ax2.axis('off')
    ax2.set_ylim(0,col2+1)
    ax2.set_xlim(0,col1+row2+spacing+5)
    ax2.set_aspect('equal')
    plt.show()
