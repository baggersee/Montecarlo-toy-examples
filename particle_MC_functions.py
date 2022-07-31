import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.special 


# function that computes the history of one single particle
# it returns the region where the particle is absorbed, -1 if reflected and 11 if transmitted 
def particle_path(sgmA,sgmE,Lx,Ly,x0,y0,rho0):
    # initializing the vector with the trajectory
    
    # computing events probabilities
    sgmT = sgmA + sgmE # total cross section [μm]
    PA = sgmA/sgmT # absortion probability
    PD = sgmE/sgmT # dispersion probability

    # original state of the particle -> state = (coordinate x, coordinate y,ngle of direction)
    r = np.array([x0,y0,rho0,0], dtype='float32') 
    # picking up the spatial coordinates
    H = [[r[0],r[1]]]
    H = pd.DataFrame(H,columns=['x','y'])
    
    while True:

        # (1) computing the total distance it walks until an event
        n1 = np.random.random() # random number between 0 and 1
        dist = - np.log(1-n1)/sgmT # distance formula (from its pdf)
       
        # moving the particle to its new location
        r[0] = r[0] + dist*np.cos(r[2])
        r[1] = r[1] + dist*np.sin(r[2])

        R = [[r[0],r[1]]]
        R = pd.DataFrame(R,columns=['x','y'])
        H = pd.concat([H,R],ignore_index= 1)
       
        
        # (2) checking if it escapes through the left edge --> reflexion
        if r[0] <= 0:
            #R = [['R','R']]
            #R = pd.DataFrame(R,columns=['x','y'])
            #H = pd.concat([H,R],ignore_index= 1)

            return H
        
        # checking if it escapes through the right edge --> transmission
        if r[0] >= Lx:
            #R = [['T','T']]
            #R = pd.DataFrame(R,columns=['x','y'])
            #H = pd.concat([H,R],ignore_index= 1)
            return H

        # checking if it hits any vertical limit --> bouncing
        # from below y = Ly (FUTURA MEJORA: ESTOY SEGURO DE CON ALGO DE ASTUCIA SE PUEDEN ACOPLAR LOS DOS CASOS)
        if r[1] > Ly:
            r[1] = Ly
            r[0] = r[0]  + (r[1] - Ly)/np.tan(r[2])
            r[2] = - r[2]
            # replacing that step in the DataFrame
            H = H.iloc[:-1,]
            R = [[r[0],r[1]]]
            R = pd.DataFrame(R,columns=['x','y'])
            H = pd.concat([H,R],ignore_index= 1)
            continue

        if r[1] < 0:
            r[1] = 0
            r[0] = r[0] - r[1]/np.tan(r[2])
            r[2] = - r[2]
            # replacing that step in the DataFrame
            H = H.iloc[:-1,]
            R = [[r[0],r[1]]]
            R = pd.DataFrame(R,columns=['x','y'])
            H = pd.concat([H,R],ignore_index= 1)
            continue

        
        # (3) gets here if still in the material --> event
        n2 = np.random.random() # random number between 0 and 1

        if n2 < PA:
            # absorption
            #R = [['A','A']]
            #R = pd.DataFrame(R,columns=['x','y'])
            #H = pd.concat([H,R],ignore_index= 1)
            return H

        else:
            # elastic dispersion --> computing the new direction
            #n3 = np.random.random() # random number between 0 and 1
            #r[2] = n3*2*np.pi # new angle (for constant angular pdf)
            # for an angular gaussian distribution it can be implemented analitically or simply with the numpy normal function:
            #r[2] = scipy.special.erfinv(2*n3 - scipy.special.erf(10/np.sqrt(2)))*np.sqrt(2)*np.pi/10 + np.pi # new angle
            r[2] = np.random.normal(0,np.pi/2)
            
    return 0


# main function --> computes recursively the single particle history function and tracks the results
def particles_stats(N_par,sgmA,sgmE,Lx,Ly,x0,y0,rho0):
    
    # vector of N_par components that will record the ending of every particle
    N_hist = np.zeros(N_par,dtype='int') 

    for j in range(N_par):
        N_hist[j] = particle_path(sgmA,sgmE,Lx,x0,y0,rho0)
        j = j+1

    return N_hist