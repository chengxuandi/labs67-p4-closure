default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24211350334853122116256736420968808050273;rho=18987351620583054002267694007344008765649;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^6+'x^61)+(1)*('x^16+'x^51),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
