from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from numpy import cos, pi, sin, sqrt, exp, random, power
import matplotlib
matplotlib.use('pgf')
matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
# Extracting all the relevant data, sorting it into our data array, for use later
file = open('Parallel_Freq_Sweep.txt', 'r')
header = file.readline()
lines = file.readlines()
N = len(lines)
i=0
# data[0] is the frequency
# data[1] is the voltage
data = np.zeros((2,N))
# Reading the file, getting the data into the data array
for line in lines:
    line = line.strip()
    columns = line.split()
    data[0][i] = float(columns[0])
    data[1][i] = float(columns[1])
    i += 1
file.close()

p0=[73.62e-3,984.4,93.94e-9,0.5]
pNames=['L','R','C','scaleFactor']
u=data[1]*0.02
tmodel = np.linspace(data[0][0], data[0][-1], N, endpoint=True)
def transfer(omega,L,R,C,scaleFactor):
    return scaleFactor*abs(R*(1-power(2*pi*omega,2)*L*C))/(sqrt((power(R,2)*(power((1-power(2*pi*omega,2)*L*C),2)))+(power(2*pi*omega,2)*power(L,2))))
# Removes random values from the data sets
jackknifeData = np.zeros((4, N, N-1))
for c in range(N):
    r = random.randint(0, N)
    jackknifeData[0, c] = np.delete(data[0], r)
    jackknifeData[1, c] = np.delete(data[1], r)
    jackknifeData[2, c] = np.delete(u, r)
    jackknifeData[3, c] = np.delete(tmodel, r)
# Fitting to the jackknifed datasets
jackknifeFits = np.zeros((N, N-1))
popts = []
for k in range(N):
    popt, pcov = curve_fit(transfer, jackknifeData[0, k], jackknifeData[1, k], p0, sigma=jackknifeData[2, k], absolute_sigma=True)
    jackknifeFits[k] = transfer(jackknifeData[3, k], *popt)
    popts.append(popt)
# Isolates arrays of each optimal fitting parameter
poptNp = np.zeros((4, N))
for d, ds in enumerate(popts):
    poptNp[0, d] = ds[0]
    poptNp[1, d] = ds[1]
    poptNp[2, d] = ds[2]
    poptNp[3, d] = ds[3]
# Calculates means and standard uncertainties
pOptimals = np.zeros((2, 4))
for j, js in enumerate(poptNp):
    mean = np.mean(js)
    pOptimals[0][j] = mean
    sumI = 0
    for i in js:
        sumI += (i-mean)**2
    pOptimals[1][j] = sqrt(float(((N-1)/N)*sumI))/sqrt(N-1)
yfit=transfer(tmodel,*pOptimals[0])
# Printing optimal fit parameters
for p in range(len(p0)):
    print(pNames[p],'=',pOptimals[0][p],'+/-',pOptimals[1][p])
# Determining Q=resFreq*L/R
resIndex=find_peaks(-yfit)[0][0]
resFreq=tmodel[resIndex]
resAngularFreq=2*pi*resFreq
resAngularFreqL=resAngularFreq*pOptimals[0][0]
Q=pOptimals[0][1]/resAngularFreqL
# Uncertainty calculations
resAngularFreqUn=0.02*resAngularFreq
resAngularFreqLUn=resAngularFreqL*sqrt((resAngularFreqUn/resAngularFreq)**2 + (pOptimals[1][0]/pOptimals[0][0])**2)
QUn=Q*sqrt((resAngularFreqLUn/resAngularFreqL)**2 + (pOptimals[1][1]/pOptimals[0][1])**2)

print('The Quality factor is',Q,'+/-',QUn)
print('The Resonant Frequency is',resFreq,'+/-',resFreq*0.02)
print('The Resonant Angular Frequency is',resAngularFreq,'+/-',resAngularFreqUn)
# Plotting the data
plt.figure()
plt.plot(data[0],data[1],color='b',linewidth=0.7,label='Parallel LRC Circuit')
plt.plot(tmodel, yfit,c='r',label='curve\_fit')
plt.xlabel('Frequency (Hz)')
plt.ylabel('$V_{out}/V_{in}$')
plt.legend()
# plt.show()
# plt.savefig('Parallel_Freq_Sweep.pgf')