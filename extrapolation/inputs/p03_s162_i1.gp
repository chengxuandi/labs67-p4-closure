default(parisizemax,1000000000);default(realprecision,100);
read("Gentry_Szydlo.gp");
read("D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/certificate_kernel.gp");
nf=nfinit(polcyclo(67));R=24213898224368675384208178366150683540049;rho=5360426610193231179408704089916274994657;alpha=Mod(17+(1)*('x^1+'x^66)+(1)*('x^14+'x^53)+(1)*('x^23+'x^44),nf.pol);
id=idealhnf(nf,R,'x-rho);make_cert(id,alpha,[R,Mod('x-rho,nf.pol)],1609);quit;
