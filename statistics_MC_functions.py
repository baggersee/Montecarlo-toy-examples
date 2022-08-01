import numpy as np



def particle_history(sgmA,sgmE,Lx,x0,y0,rho0):
    # función que calcula la historia de una partícula
    # devuelve el número de región en la que la partícula es absorbida (1-10), -1 si la partícula es reflejada, u 11 si es transmitida.
    
    # cálculo de las probabilidades de cada event
    sgmT = sgmA + sgmE # sección eficaz total [μm]
    PA = sgmA/sgmT # probabilidad de absorción
    PD = sgmE/sgmT # probabilidad de dispersión

    # estado inicial de la partícula -> estado = (coordenada x, coordenada y, ángulo de dirección en el que se mueve)
    r = np.array([x0,y0,rho0], dtype='float32') 

    
    while True:

        # (1) cálculo de la distancia que recorre en línea recta (en la dirección que tenga) hasta que sufre un evento
        n1 = np.random.random() # número aleatorio entre 0 y 1
        dist = - np.log(1-n1)/sgmT # fórmula de la distancia (a partir de su pdf)
       
        # la partícula se mueve esa distancia en la dirección que tenga --> se actualizan sus coordenadas
        r[0] = r[0] + dist*np.cos(r[2])
        r[1] = r[1] + dist*np.sin(r[2])
        
        # (2) comprobamos si escapa por la frontera izda --> reflexión
        if r[0] <= 0:
            result = -1
            return result
        
        # comprobamos si escapa por la frontera dcha --> transmisión
        if r[0] >= Lx:
            result = 11
            return result

        # (3) la partícula permanece en el material tras el desplazamiento --> evento
        n2 = np.random.random() # número aleatorio entre 0 y 1
        if n2 < PA:
            # absorción
            result = np.floor(r[0]) # devuelve el límite izquierdo del intervalo donde es absorbida --> 0 si cae en [0,1], 1 si cae entre [1,2], etc...
            return result

        else:
            # dispersión elástica --> obtenemos la nueva dirección de movimiento
            n3 = np.random.random() # número aleatorio entre 0 y 1
            r[2] = n3*2*np.pi # ángulo nuevo (pdf angular constante)

    return 0


# main function --> ejecuta recursivamente la función 'particle_history' y almacena los resultados en un vector
def particles_stats(N_par,sgmA,sgmE,Lx,x0,y0,rho0):

    # vector de 'N_par' componentes que guardará el final de cada partícula.
    N_hist = np.zeros(N_par,dtype='int') 

    for j in range(N_par):
        N_hist[j] = particle_history(sgmA,sgmE,Lx,x0,y0,rho0)
        j = j+1

    return N_hist