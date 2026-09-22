default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24571855408068981453998836016485334269211;rho=1316221929686388536723070621537493253522;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^2+'x^65)+(1)*('x^25+'x^42),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
