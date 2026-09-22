default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24189940806366871258086034556205818280577;rho=12806833144182369423748298945643675562702;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^3+'x^64)+(1)*('x^14+'x^53),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
