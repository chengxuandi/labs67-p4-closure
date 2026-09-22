default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24147779601722609270541764195232968510369;rho=518496099282001483432833453800560290653;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^5+'x^62)+(1)*('x^11+'x^56),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
