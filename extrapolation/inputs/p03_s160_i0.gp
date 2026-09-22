default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24216927135750198417154400019414551011171;rho=281654310801530530464137510773987300522;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^14+'x^53)+(1)*('x^18+'x^49),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
