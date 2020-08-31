import numpy as np

def parse(fil):
    f = open(fil,'r')
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        if "Layer 1 size" in lines[i]:
            row1 = eval(lines[i].split()[3])
            col1 = eval(lines[i].split()[4])
        if "Layer 2 size" in lines[i]:
            row2 = eval(lines[i].split()[3])
            col2 = eval(lines[i].split()[4])
        if "R_top" in lines[i]:
            R_top = eval(lines[i].split()[1])
        if "R_bottom" in lines[i]:
            R_bot = eval(lines[i].split()[1])
        if "R_cross" in lines[i]:
            R_cross = lines[i].split()
            R_cross.pop(0)
            R_cross = [int(i) for i in R_cross]
        if "I+ position" in lines[i]:
            Ip_layer = eval(lines[i].split()[2])
            Ip_pos1 = eval(lines[i].split()[3])
            Ip_pos2 = eval(lines[i].split()[4])
        if "I- position" in lines[i]:
            Im_layer = eval(lines[i].split()[2])
            Im_pos1 = eval(lines[i].split()[3])
            Im_pos2 = eval(lines[i].split()[4])
        if "V+ position" in lines[i]:
            Vp_layer = eval(lines[i].split()[2])
            Vp_pos1 = eval(lines[i].split()[3])
            Vp_pos2 = eval(lines[i].split()[4])
        if "V- position" in lines[i]:
            Vm_layer = eval(lines[i].split()[2])
            Vm_pos1 = eval(lines[i].split()[3])
            Vm_pos2 = eval(lines[i].split()[4])
        if "Convergence" in lines[i]:
            convergence = eval(lines[i].split()[1])
        if "Maximum Iterations" in lines[i]:
            max_iter = eval(lines[i].split()[2])
    return row1, col1, row2, col2, R_top, R_bot, R_cross, Ip_layer, Ip_pos1, Ip_pos2, Im_layer, Im_pos1, Im_pos2, Vp_layer, Vp_pos1, Vp_pos2, Vm_layer, Vm_pos1, Vm_pos2, convergence, max_iter

