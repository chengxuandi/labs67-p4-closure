default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24197910293515046222216767007200864310743;rho=21808537619666467793787839025980224692451;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^3+'x^64)+(1)*('x^30+'x^37),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
