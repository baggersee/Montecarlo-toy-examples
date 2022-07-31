import numpy as np
import matplotlib.pyplot as plt
from particle_MC_functions import particle_path

# Parameters
# parameters
N_PARTICLES = 20
SIGMA_A = 0.1 # absorption cross section [μm]
SIGMA_E = 0.8 # elastic dispersion cross section [μm]
LX = 10 # horizontal length [μm]
LY = 1 # vertical length [μm] (not used)
X0 = 0 # initial x position [μm]
Y0 = LY/2 # initial y position [μm]
RHO_0 = 0 # initial angle of direction [rad]

def path_maker(Nparts,sgmA,sgmE,Lx,Ly,x0,y0,rho0):
    
    # initializing the absorption, relfexion and transmission coeficients
    A,R,T = 0,0,0

    # getting the DataFrame with the path of one particle
    #T = particle_path(sigma_A,sigma_E,L_x,L_y,x_0,y_0,rho_0)
    #L = len(T)

    # DYNAMIC PLOTTING
    #Turn on interactive mode
    plt.ion()

    #Set up plot
    figure, ax = plt.subplots()
    #Set scale for x and y axes
    intervals_x = [ x for x in range(-1,int(Lx) + 2) ]
    intervals_y = [ x for x in range(-1,int(Ly) + 1) ]
    plt.xticks(intervals_x)
    plt.yticks(intervals_y)
    ax.set_ylim(0., Ly)
    ax.set_xlim(0., Lx + 1 )
    caption = 'n = 1' + ' '*2 + 'A = ' + str(int(A)) + ' '*2 + 'R = ' + str(int(R)) + ' '*2 + 'T = ' + str(int(T)) 
    plt.title(caption)

    #Draw grid
    ax.grid()
    #Draw horizontal line
    for i in intervals_x:
        ax.vlines(i, 0., Lx)

    #Add empty line
    lines, = ax.plot([], [], color='r')

    for n in range (Nparts):
        Tr = particle_path(SIGMA_A,SIGMA_E,LX,LY,X0,Y0,RHO_0)
        L = len(Tr)
        # getting the result --> abroption,transmission and reflexion
        if Tr.iloc[L-1,0] < 0:
            R = R + 1

        elif Tr.iloc[L-1,0] > Lx:
            T = T + 1

        else:
            A = A + 1

        xdata = []
        ydata = []

        for j in range(L):
            xdata.append(Tr.x[j])
            ydata.append(Tr.y[j])

            #Update data
            lines.set_xdata(xdata)
            lines.set_ydata(ydata)

            figure.canvas.draw()
            figure.canvas.flush_events()

        # updating title
        caption = 'n = ' + str(int(n+2)) + ' '*2 + 'A = ' + str(int(A)) + ' '*2 + 'R = ' + str(int(R)) + ' '*2 + 'T = ' + str(int(T)) 
        plt.title(caption)

    
    
    # in this way the figure does not automatically close itself when the final particle ends
    while True:
        lines.set_xdata(xdata)
        lines.set_ydata(ydata)
        caption = 'n = ' + str(int(n+1)) + ' '*2 + 'A = ' + str(int(A)) + ' '*2 + 'R = ' + str(int(R)) + ' '*2 + 'T = ' + str(int(T)) 
        plt.title(caption)
        figure.canvas.draw()
        figure.canvas.flush_events()
        

path_maker(N_PARTICLES,SIGMA_A,SIGMA_E,LX,LY,X0,Y0,RHO_0)












