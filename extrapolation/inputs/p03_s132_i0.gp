default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24147858963704910543094145714799537479801;rho=1255447021874557280071962349291556424863;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^8+'x^59)+(1)*('x^29+'x^38),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
