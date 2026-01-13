#include <iostream>
#include <ap_int.h>

extern "C" void adder(ap_uint<4> a, ap_uint<4> b, ap_uint<5> &sum);

int main() {
    ap_uint<5> s;

    adder(3, 7, s);
    if (s != 10) return 1;

    adder(15, 1, s);
    if (s != 16) return 1;

    std::cout << "SIM PASSED\n";
    return 0;
}