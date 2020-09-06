import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from parse_input import parse
import matplotlib.patches as patches

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

#d_mat = np.loadtxt('DUT.txt')
#d_mat = np.loadtxt('DUT_2.txt')
#d_mat = np.loadtxt('DUT_3.txt')
#d_mat = np.loadtxt('DUT_4.txt')
#d_mat = np.loadtxt('DUT_5.txt')
#d_mat = np.loadtxt('DUT_6.txt')
#d_mat = np.loadtxt('DUT_7.txt')
#d_mat = np.loadtxt('DUT_8.txt')
d_mat = np.loadtxt('DUT_9.txt')
print(np.shape(d_mat))
spacing = 15
X1 = [i for i in range(col1)]
Y1 = [i for i in range((col2-row1)//2+row1,(col2-row1)//2,-1)]
x1,y1 = np.meshgrid(X1,Y1)
X2 = [i for i in range((col1-row2)//2,(col1-row2)//2+row2)]
Y2 = [i for i in range(col2)]
x2,y2 = np.meshgrid(X2,Y2)
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
X1 = [i for i in range(col1)]
Y1 = [i for i in range((col2-row1)//2+row1,(col2-row1)//2,-1)]
x1,y1 = np.meshgrid(X1,Y1)
X2 = [i for i in range(col1+spacing,col1+row2+spacing)]
Y2 = [i for i in range(col2)]
x2,y2 = np.meshgrid(X2,Y2)
levels = np.arange(-0.015,10.015,0.005)+0.005
p1 = ax1.contourf(x1,y1,V1,levels,alpha=0.8,cmap='twilight_shifted',antialiased=True)
rect1 = patches.Rectangle(( cross[0], (col2-row1)//2+1),cross[1]-cross[0],row1-1,linewidth=1,edgecolor='k',facecolor='None')
ax1.add_patch(rect1)

#ax1.arrow( cross[1]+1,(col2-row1)//2+row1+3,col1-cross[1]-2-6.75,0,color='green',width=1.5,head_width=4.5)
ax1.arrow( cross[1]+1,(col2-row1)//2-3,col1-cross[1]-2-6.75,0,color='green',width=1.5,head_width=4.5)
#ax1.arrow( col1+2,cross[3]+1,0,-(row1-2-6.75),color='green',width=1.5,head_width=4.5)

#ax1.arrow(spacing+col1-3,cross[3]+1,0,col2-cross[3]-2-6.75,color='red',width=1.5,head_width=4.5)
ax1.arrow(spacing+col1,col2+2,row2-2-6.75,0,color='red',width=1.5,head_width=4.5)
#ax1.arrow(spacing+col1+row2+2,cross[3]+1,0,col2-cross[3]-2-6.75,color='red',width=1.5,head_width=4.5)

p2 = ax1.contourf(x2,y2,V2.T,levels,alpha=0.8,cmap='twilight_shifted',antialiased=True)
rect2 = patches.Rectangle((spacing+col1,(col2-row1)//2+1),row2-1,cross[3]-cross[2],linewidth=1,edgecolor='k',facecolor='None')
ax1.add_patch(rect2)
ax1.axis('off')
ax1.set_ylim(0,col2+5)
ax1.set_xlim(0,col1+row2+spacing+5)
ax1.set_aspect('equal')
cbar1 = plt.colorbar(p2)
cbar1.set_ticks([0,2,4,6,8,10])
cbar1.set_ticklabels(['0','2','4','6','8','10V'])
ax2 = fig.add_subplot(1,2,2)
im = ax2.imshow(d_mat.T,origin='lower',cmap='inferno',interpolation='bessel')#,extent=[0,col1-cross[1]-1,0,col2-cross[3]-1])
cbar2 = plt.colorbar(im)
#cbar2.set_ticks([-160,-200,-240,-280,-320])
#cbar2.set_ticklabels([r'-160 $\Omega$','-200','-240','-280','-320'])
#ax2.set_xticks([0,3,6,9,12,15,18])
ax2.set_xlabel('V+ displacement along Green arrow')
ax2.set_ylabel('V- displacement along Red arrow')
plt.tight_layout()
plt.show()
