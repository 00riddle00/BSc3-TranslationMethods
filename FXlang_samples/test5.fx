
fx main(int a, int b) ==> int {

    a = &a + &b;
    int a = $$(a + 2);


}


fx foo(int c, int d) ==> bool {
 return True;
}
   # $++a = 2;
   # a = &++b;
   # char b = 't';
   # a = b + a;
   # a = "true" + a;

   # a = foo(2,3) + $c;

   # int$ c;
   # $c = 4;

   # int$ a;
   # int a;
   # a = ++2;
   # int$$$ c;
   # $$c = &++a;
   # $$c = *a;

   # int a = 5;
   # int b = 3;

   # bool c = 5 != 3 AND 3*5 > 10;

   # int z = 2;
   # int$$ c;
   # adresas i pointeri
   # int $$$c;
   # $$$c = 2;

   # c = &z;
   # $$c = 2;

   # int z = 2;
   # $c = 2;
   # c = &z;

   # int a = $$(a + 2);
   # int a = $a + 2;
   # foo($a + 2);

    # int a;
    # ++a = 3;

    # ++a = 3;

    # int a = ++(a + 2); # should not work

    # int a = b + c;

    ###
    if (a+b+c) {
        return 8;
    }

    return (1 + 2) * b;
    ###
