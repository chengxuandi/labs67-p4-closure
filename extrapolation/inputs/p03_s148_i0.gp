default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24146656458050057248914683960034347069153;rho=5022350192811179714394054982029705569087;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^10+'x^57)+(1)*('x^28+'x^39),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
