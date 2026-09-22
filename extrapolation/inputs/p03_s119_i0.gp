default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24211417873617938133303856230137159357299;rho=12152124088482739126863190292818775902310;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^7+'x^60)+(1)*('x^24+'x^43),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
