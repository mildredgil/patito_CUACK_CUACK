programa patito;
var ent b, c, d, e;

  funcion ent resta(ent i, ent k)
  var ent j;
  {
    j = i - k;
    regresa(j);
  }

  funcion ent suma(ent i, ent k)
  var ent j;
  {
    j = i + k;
    regresa(j);
  }

  funcion ent especial(ent i, ent k) 
  var ent j;
  {
    j = suma(i, k);
    regresa(j);
  }


principal () {
    b = resta(20,10) + suma(20, 10);
    escribe("b =",b);

    b = suma(20, resta(20,10));
    escribe("b =",b);

    b = suma(suma(2,suma(1,1)), resta(20,10));
    escribe("b =",b);

    b = especial(20, resta(20,10));
    escribe("b =",b);
  }