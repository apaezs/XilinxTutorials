#include <ap_int.h>

extern "C" void counter(
    bool rst,
    bool en,
    ap_uint<8> &count
) {
#pragma HLS INTERFACE ap_none port=rst
#pragma HLS INTERFACE ap_none port=en
#pragma HLS INTERFACE ap_none port=count
#pragma HLS INTERFACE ap_ctrl_none port=return

    static ap_uint<8> reg = 0;

    if (rst) {
        reg = 0;
    } else if (en) {
        reg = reg + 1;
    }

    count = reg;
}