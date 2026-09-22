default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24210874502693372465947268711975259143669;rho=21282248556305982115551199327366668840490;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^6+'x^61)+(1)*('x^15+'x^52),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],1609);quit;
