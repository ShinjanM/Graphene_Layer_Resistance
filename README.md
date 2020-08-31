# Graphene_Layer_Resistance
Calculating resistance of bilayer grahene sheets aprroximating them as a coupled network of resistors.

Run main.py to generate the current and voltage distributions

## Input paramters
The input paramters are specified in the file **input.dat**.

The various input parameters are:

> -**Layer 1 size**  < number of rows in layer 1 >   < number of columns in layer 1 >  
> -**Layer 2 size**  < number of rows in layer 2 >   < number of columns in layer 2 > 
> -**R_top**    Resistance in layer 1 (in Ohms)
> -**R_bottom** Resistance in layer 2 (in Ohms)
> -**R_cross**  Resistance in the cross sectional region (in Ohms) 
> -**I+ position**  < layer number >   < row number >   < column number >
> -**I- position**  < layer number >   < row number >   < column number >
> -**V+ position**  < layer number >   < row number >   < column number >
> -**V- position**  < layer number >   < row number >   < column number >
> -**Convergence**  < Value of convergence threshold >
> -**Maximum Iterations** < Maxium number of iterations >

