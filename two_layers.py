class Fixed:
    FREE = 0
    A = 1
    B = 2

class Node:
    __slots__ = ["voltage","fixed"]
    def __init__(self, v=0.0, f=Fixed.FREE):
        self.voltage = v
        slef.fixed = f

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
                Vmnp += grid1[m+1][n] / R_top
                R_inv += 1/R_top
            if n<(col1-1):
                Vmnp += grid1[m][n+1] /R_top
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
                Vmnp += grid2[m-1][n].voltage / R_bottom
                R_inv += 1/R_bottom
            if n!=0:
                Vmnp += grid2[m][n-1].voltage / R_bottom
                R_inv += 1/R_bottom
            if m<(row2-1):
                Vmnp += grid2[m+1][n] / R_bottom
                R_inv += 1/R_bottom
            if n<(col2-1):
                Vmnp += grid2[m][n+1] /R_bottom
                R_inv += 1/R_bottom
            if ((n>=cross_boundary[2]) and (n<=cross_boundary[3])):
                layer1_position_1 = cross_boundary[3] - n
                layer2_position_2 = m + cross_boundary[0]
                Vmnp += grid1[layer1_position_1][layer1_position_2].voltage / R_cross
                R_inv += R_cross
            Vmnp = Vmnp/R_inv
            diff = abs(grid2[m][n].voltage - Vmnp)
            grid2[m][n].voltage = Vmnp
        else:
            diff = 0
    return diff

def iterations(number_of_iterations, grid1, grid2, cross_boundary, R_top, R_bot, R_cross):
    row1, col1 = np.shape(grid1)[0], np.shape(grid1)[1]
    row2, col2 = np.shape(grid2)[0], np.shape(grid2)[1]
    for i in range(number_of_iterations):
        diff = 0
        for p in range(2):
            if p==0:
                for m in range(row1):
                    for n in range(col1):
                        if (m+n)%2 == 0:
                            diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
                for m in range(row1):
                    for n in range(col1):
                        if (m+n)%2 != 0:
                            diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
            if p==1:
                for m in range(row2):
                    for n in range(col2):
                        if (m+n)%2 == 0:
                            diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
                for m in range(row2):
                    for n in range(col2):
                        if (m+n)%2 != 0:
                            diff += V_mnp(m,n,p,grid1,grid2,row1,col1,row2,col2,R_top,R_bot,R_cross,cross_boundary)
    
    return
                
        

