default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24212630687933537658348833938942567314817;rho=8789800971811616455585584210191723456084;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^4+'x^63)+(1)*('x^14+'x^53),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
