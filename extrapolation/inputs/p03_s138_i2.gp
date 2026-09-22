default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24219041882819638080772220628963377013829;rho=12338143573788386827457282365195666353382;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^9+'x^58)+(1)*('x^16+'x^51),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
