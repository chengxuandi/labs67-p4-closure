default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24925694622714930338466930608806253008559;rho=120365057984034399563065173368900631530;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^12+'x^55)+(1)*('x^13+'x^54),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
