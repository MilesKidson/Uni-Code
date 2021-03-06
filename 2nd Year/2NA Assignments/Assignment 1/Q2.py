from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('pgf')
matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

x = np.linspace(-10, 10, 500)
y = np.linspace(-10, 10, 500)

def y1(x):
    return (x**2)-2
def y2(x):
    return np.sqrt(x+2)
def y3(x):
    return 2/(x-1)
def y4(x):
    return (2/x)+1

y32 = y3(x)[~np.isnan(y3(x))]

plt.plot(x, y1(x), color='r', lw=0.5, label='$y = g_1(x)$')
plt.plot(x, y2(x), color='b', lw=0.5, label='$y = g_2(x)$')
plt.plot(x, y32, color='y', lw=0.5, label='$y = g_3(x)$')
plt.plot(x, y4(x), color='g', lw=0.5, label='$y = g_4(x)$')
plt.plot(x, np.zeros(500), color='black')
plt.plot(np.zeros(500), y, color='black')
plt.plot(x, y, label='$y = x$')

plt.ylim(-10, 10)
plt.xlim(-10, 10)
plt.xlabel('x')
plt.ylabel('y', rotation=0)
plt.legend()
plt.savefig('2NA Assignments\Assignment 1\Q2 Plot.pgf')
# plt.show()