default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24211317797119082703071651344995757229507;rho=4489887658704509942933194241162283664987;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^9+'x^58)+(1)*('x^14+'x^53),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
