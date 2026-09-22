default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24147925091713037895636537771523653384881;rho=5166192668432749510717634084978554022517;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^14+'x^53)+(1)*('x^16+'x^51),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],269);quit;
