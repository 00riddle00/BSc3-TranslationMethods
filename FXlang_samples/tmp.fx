
fx main() ==> void {

  ++(($a));
  ++($($($a)));
  $a = 2;
  $($$a) = 3;
  $a = $($fn_call(++b));
  $(a) = $($b) + ++c;
  $a = $(a+b);
  a = $(a+b);
  $(foo(123)) = 456;
  ++a = fn(call(&b));

}
