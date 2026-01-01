#include <ap_int.h>

extern "C" void adder(
    ap_uint<4> a,
    ap_uint<4> b,
    ap_uint<5> &sum
) {
#pragma HLS INTERFACE ap_none port=a
#pragma HLS INTERFACE ap_none port=b
#pragma HLS INTERFACE ap_none port=sum
#pragma HLS INTERFACE ap_ctrl_none port=return

    sum = a + b;
}