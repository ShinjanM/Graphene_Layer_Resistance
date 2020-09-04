# 4 probe measurements in bilayer sheets

Calculating resistance of bilayer systems aprroximating them as a coupled network of resistors. Each layer is assumed to have uniform values for the value of each resistor element. The network and the four probes are as follows:

  ![Schematic for the calculation](/master/Schematic.png)

We try to look at the effect on the DUT resistance by varying the various paramters in the system.

## Input paramters
The input paramters are specified in the file **input.dat**.

The various input parameters are:
```        
        Layer 1 size          <number of rows in layer 1>   <number of columns in layer 1>   
        Layer 2 size          <number of rows in layer 2>   <number of columns in layer 2>   
        R_top                 <Resistance in layer 1>  
        R_bottom              <Resistance in layer 2>  
        R_cross               <Resistance in the cross sectional region>   
        I+ position           <layer number>   <row number>   <column number>  
        I- position           <layer number>   <row number>   <column number>  
        V+ position           <layer number>   <row number>   <column number>    
        V- position           <layer number>   <row number>   <column number> 
        Convergence           <Value of convergence threshold>  
        Maximum Iterations    <Maxium number of iterations>  
	Append		       String you want to append to output files	
```	
*Note that if you are scanning over a series of R_cross you can enter all the values seperated by spaces*

## Running the Code
After specifying the input parameters run 
```
        python main.py
	python plot_planes.py
```     
The final voltage distribution will be saved as an image and the Results.txt will contain all the necessary probe data.
