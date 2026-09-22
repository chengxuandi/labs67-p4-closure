default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24212438036475502598157601688937224899241;rho=16400619335315350510970852759545264493563;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^4+'x^63)+(1)*('x^27+'x^40),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
