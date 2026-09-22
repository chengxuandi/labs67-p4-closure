default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24189102009274872633073418079084802254509;rho=147586863905298208945893474920695902359;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^3+'x^64)+(1)*('x^20+'x^47),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
