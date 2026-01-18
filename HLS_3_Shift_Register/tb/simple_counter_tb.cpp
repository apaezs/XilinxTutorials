#include <iostream>
#include <ap_int.h>

extern "C" void counter(bool rst, bool en, ap_uint<8> &count);

int main() {
    ap_uint<8> c;

    // Reset
    counter(1, 0, c);
    if (c != 0) return 1;

    // Enable counting
    for (int i = 1; i <= 5; i++) {
        counter(0, 1, c);
        if (c != i) return 1;
    }

    // Hold value when disabled
    counter(0, 0, c);
    if (c != 5) return 1;

    // Reset again
    counter(1, 0, c);
    if (c != 0) return 1;

    std::cout << "SIM PASSED\n";
    return 0;
}
