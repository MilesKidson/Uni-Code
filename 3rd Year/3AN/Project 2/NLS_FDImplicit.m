L=100;
N=1000;
h=L/N;
tau=h^2/3;
tMax=2000;
x1=-10;
v1=-1;
x2=15;
v2=1;
A1=0.8;
A2=0.5;
S=1;
s=tau/h^2;

x=(-L/2:h:L/2-h);
psi0=((A1*sech(A1.*(x-x1)).*exp(1i*v1.*(x-x1)))+(A2*sech(A2.*(x-x2)).*exp(1i*v2.*(x-x2))))';
psi=zeros(size(psi0));

conserved=trapz(abs(psi0).^2);
disp( conserved )

plot(x,abs(psi0))

A=diag((1+1i*s)*ones(N-2,1),0)+diag(-1i*s/2*ones(N-3,1),1)+diag(-1i*s/2*ones(N-3,1),-1);
tic
for tt=1:tMax
    psi(1)=0;
    psi(2:N-1)=A\(psi0(2:N-1)+1i*tau/(2*h^2).*(psi0(1:N-2)-2.*psi0(2:N-1)+psi0(3:N))+...
        (2*1i*tau*abs(psi0(2:N-1)).^2.*psi0(2:N-1))./(1+S.*sin(abs(psi0(2:N-1)).^2)));
    psi(N)=0;
    psi0=psi;
    
    conserved=trapz(abs(psi0).^2);
    disp( conserved )
    plot(x,abs(psi0)),drawnow
end
toc