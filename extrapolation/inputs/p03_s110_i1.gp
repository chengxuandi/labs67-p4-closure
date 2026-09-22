default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24209977619894851705113889026909868818119;rho=11891649756166878023970157055670838611584;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^6+'x^61)+(1)*('x^25+'x^42),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
