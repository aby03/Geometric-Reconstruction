function dG = dgauss(sigma)
x = floor(-3*sigma):ceil(3*sigma);
G = exp(-0.5*x.^2/sigma^2);
%G = G/sum(G);
G=G/(sqrt(2*pi)*sigma);
dG = -x.*G/sigma^2;


