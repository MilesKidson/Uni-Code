L=40;
tau=0.01;
N=1000;
h=L/N;
tMax=1000;
x1=-10;
v1=1;
x2=15;
v2=-1;
A1=0.8;
A2=0.5;

x=(-L/2:h:L/2-h);
psi=(A1*sech(A1.*(x-x1)).*exp(1i*v1.*(x-x1)))+(A2*sech(A2.*(x-x2)).*exp(1i*v2.*(x-x2)));

plot(x,abs(psi))

n=[0:N/2-1 -N/2:-1].^2;

n=exp(-1i*tau*4*pi^2/L^2*n);

for tt=1:tMax
    psi=psi.*exp(1i*tau*2*abs(psi).^2);
    
    psi=ifft(n.*fft(psi));
    
    plot(x,abs(psi)),drawnow
end