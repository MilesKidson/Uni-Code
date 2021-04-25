from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from numpy import cos, pi, sin, sqrt, exp, random
import matplotlib
matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

n=1
a=0.001
b=10

N=50
h=(b-a)/N
print('h',h)

r_span=np.array([a,b])
rs=np.arange(a,b,h)

alpha=0
beta=1
p_0=(beta-alpha)/(b-a)
print('p_0', p_0)
ICs=np.array([alpha,p_0,0,1])


def f(r,u,v):
    return -((1/r)*v + (u/(1-u**2))*(v**2 - (n**2)/(r**2)) + u*(1-u**2))

def df_du(r,u,v):
    return -((1+u**2)/((1-u**2)**2)*(v**2 - (n**2)/(r**2)) + (1-3*u**2))

def df_dv(r,u,v):
    return -((1/r) + u/(1-u**2)*(2*v))

u_1=0 #just used so the while doesn't break the first loop around
tol=1e-5
maxIter=200
k=1
while k <= maxIter and (abs(u_1-b)>tol):
    def du_dr(R,y):
        U=y[0]
        V=y[1]
        Z=y[2]
        W=y[3]
        return np.array([V, f(R,U,V), W, df_du(R,U,V)*Z + df_dv(R,U,V)*W])

    soln=solve_ivp(du_dr, r_span, ICs, t_eval=rs)

    if k==1:
        u_0=soln.y[0]
    
    u=soln.y[0]
    u_1=u[-1] # Last element
    z=soln.y[2]
    z_1=z[-1]

    p_0=p_0-(u_1-beta)/(z_1)
    print(p_0)
    # print(u[-1])
    ICs[1]=p_0
    
    print(k)
    k+=1

print("p_0",p_0)
print('z_1', z_1)

t=soln.t
v=soln.y[1]
w=soln.y[3]

plt.plot(t, u, label='u')
# plt.plot(t, u_0, label='u0')

plt.legend()
plt.show()
