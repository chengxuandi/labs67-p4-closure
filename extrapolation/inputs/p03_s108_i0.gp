default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24211344835444904758201755859725434659943;rho=5010005044515957295638383740982081236558;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^6+'x^61)+(1)*('x^21+'x^46),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
