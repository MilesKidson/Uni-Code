L=100;
N=1000;
h=L/N;
tau=h^2/4;
tMax=2000;
x1=-40;
v1=5;
x2=50;
v2=-5;
A1=0.8;
A2=0.5;
S=0;

x=(-L/2:h:L/2-h);
psi=(A1*sech(A1.*(x-x1)).*exp(1i*v1.*(x-x1)))+(A2*sech(A2.*(x-x2)).*exp(1i*v2.*(x-x2)));

conserved1=trapz(abs(psi).^2);
disp( conserved1 )
plot(x,abs(psi))

n=[0:N/2-1 -N/2:-1].^2;

n=exp(-1i*tau*4*pi^2/L^2*n);
tic
for tt=1:tMax
    psi=psi.*exp((1i*tau*2*abs(psi).^2)./(1+S.*sin(abs(psi).^2)));
    
    psi=ifft(n.*fft(psi));
    
    conserved=trapz(abs(psi).^2);
    disp( conserved )
    plot(x,abs(psi)),drawnow
end
toc
disp( conserved1-conserved )