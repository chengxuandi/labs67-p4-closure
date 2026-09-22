default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24219786747187099644135022288218295050899;rho=12246460913360432089093089225154647756580;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^5+'x^62)+(1)*('x^30+'x^37),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
