default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24219069365193651050931997718396361424423;rho=12719997794805876672834511917064218624092;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^8+'x^59)+(1)*('x^26+'x^41),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
