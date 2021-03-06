import numpy as np
from numpy import cos, pi, sin, sqrt, exp, random
from vpython import *
# Constants to be used later, such as start positions and start momenta
r1=vector(1e11,0,0)
r2=vector(2.5e11,0,0)
rStar=vector(0,0,0)
m1=1e30
m2=6e27
mStar=2e30
G = 6.67e-11
p1=m1*vector(0,sqrt(G*mStar/mag(r1-rStar)),0)
p2=m2*vector(0,-sqrt(G*(mStar+m1)/mag(r2-rStar)),2000)
pStar=vector(0,0,0)
rCoM = ((m1*r1)+(m2*r2)+(mStar*rStar))/(m1+m2+mStar)
# Converting to CoM reference frame
vCoM = (p1+p2+pStar)/(m1+m2+mStar)
p1 -= m1*vCoM
p2 -= m2*vCoM
pStar -= mStar*vCoM
# More constants, physical
deltaT = 86400
t = 0
# Creating the objects to be drawn on the canvas, as well as settings for the canvas
planet1 = sphere(pos=r1, radius=1e10, color=color.blue)
planet2 = sphere(pos=r2, radius=1e10, color=color.green)
star = sphere(pos=rStar, radius=1e10, color=color.yellow)
CoM = sphere(pos=rCoM, radius=7e9, color=color.red)
planet1Trail = curve(color=color.blue, radius=1e9)
planet2Trail = curve(color=color.green, radius=1e9)
starTrail = curve(color=color.yellow, radius=1e9)
CoMTrail = curve(color=color.red, radius=1e9)
scene.autoscale = 0
scene.title = 'Planet1 Initial Momentum: '+str(p1)+' Planet1 Mass: '+str(m1)+'\nPlanet2 Initial Momentum: '+str(p2)+' Planet2 Mass: '+str(m2)+\
    '\nStar Initial Momentum: '+str(pStar)+' Star Mass: '+str(mStar)+'\nSystem Initial Momentum: '+str(p1+p2+pStar)
# The loop that calculates new positions based on forces
while t < deltaT*365*15:
    rate(100)
    # Updating positions and trails
    planet1Trail.append(pos=r1)
    planet2Trail.append(pos=r2)
    starTrail.append(pos=rStar)
    CoMTrail.append(pos=rCoM)
    planet1.pos=r1
    planet2.pos=r2
    star.pos=rStar
    CoM.pos=rCoM
    # Force calculations
    F1Star = -G*mStar*m1*(r1-rStar)/(mag(r1-rStar)**3)
    F12 = -G*m1*m2*(r1-r2)/(mag(r1-r2)**3)
    F2Star = -G*m2*mStar*(r2-rStar)/(mag(r2-rStar)**3)
    # Updating planet1 position and momentum
    p1 += (F1Star+F12)*deltaT
    r1 += p1*deltaT/m1
    # Updating planet2 position and momentum
    p2 += (F2Star-F12)*deltaT
    r2 += p2*deltaT/m2
    # Updating star position and momentum
    pStar += (-F1Star-F2Star)*deltaT
    rStar += pStar*deltaT/mStar
    # Finding new CoM position from positions of masses
    rCoM = ((m1*r1)+(m2*r2)+(mStar*rStar))/(m1+m2+mStar)
    # Housekeeping
    t += deltaT
    scene.caption = 't: '+str(round((t/86400),3))+' days'+'\ndeltaT: '+str(deltaT)+'\nSystem Momentum at time t: '+str(p1+pStar) \
        +'\nr1: '+str(r1)+'\nr2:'+str(r2)+'\nrStar: '+str(rStar)