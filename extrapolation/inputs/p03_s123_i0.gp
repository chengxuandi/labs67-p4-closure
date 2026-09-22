default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24925687905145162685246439158166586953059;rho=6220685949439267775382614131322541688355;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^8+'x^59)+(1)*('x^9+'x^58),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
