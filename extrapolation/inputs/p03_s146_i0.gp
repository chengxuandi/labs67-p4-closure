default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24147903241774579212468222858216737193623;rho=12602978438409317232828905846568743713038;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^10+'x^57)+(1)*('x^21+'x^46),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
