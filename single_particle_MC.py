import numpy as np
import matplotlib.pyplot as plt
from particle_MC_functions import particle_path

# esto simula solo una particula

# Parameters
# parameters
N_particles = 10000
sigma_A = 0.3 # absorption cross section [μm]
sigma_E = 0.8 # elastic dispersion cross section [μm]
L_x = 10 # horizontal length [μm]
L_y = 2 # vertical length [μm] (not used)
x_0 = 0 # initial x position [μm]
y_0 = 0.5 # initial y position [μm]
rho_0 = 0 # initial angle of direction [rad]

T = particle_path(sigma_A,sigma_E,L_x,L_y,x_0,y_0,rho_0)
L = len(T)
print(L)
x = T.x[0]
print(x)


#Turn on interactive mode
plt.ion()

#Set up plot
figure, ax = plt.subplots()
#Set scale for x and y axes
intervals_x = [ x for x in range(-1,int(L_x) + 2) ]
intervals_y = [ x for x in range(-1,int(L_y) + 1) ]
plt.xticks(intervals_x)
plt.yticks(intervals_y)
ax.set_ylim(0., L_y)
ax.set_xlim(0., L_x + 1 )

#Draw grid
ax.grid()
#Draw horizontal line
for i in intervals_x:
    ax.vlines(i, 0., L_x)



#Add empty line
lines, = ax.plot([], [], color='r')

xdata = []
ydata = []

for j in range(L):
    xdata.append(T.x[j])
    ydata.append(T.y[j])

    #Update data
    lines.set_xdata(xdata)
    lines.set_ydata(ydata)

    figure.canvas.draw()
    figure.canvas.flush_events()

    if j == L-1:
        while True:
            lines.set_xdata(xdata)
            lines.set_ydata(ydata)

            figure.canvas.draw()
            figure.canvas.flush_events()







