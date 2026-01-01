`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// AXI4-Stream Inverter with TLAST
//////////////////////////////////////////////////////////////////////////////////

module inverter #(
    parameter DATA_WIDTH = 32
)(
    input  wire                     axi_clk,
    input  wire                     axi_reset_n,

    // AXI4-Stream Slave Interface
    input  wire                     s_axis_valid,
    input  wire [DATA_WIDTH-1:0]    s_axis_data,
    input  wire                     s_axis_tlast,
    output wire                     s_axis_ready,

    // AXI4-Stream Master Interface
    output reg                      m_axis_valid,
    output reg  [DATA_WIDTH-1:0]    m_axis_data,
    output reg                      m_axis_tlast,
    input  wire                     m_axis_ready
);

    integer i;

    assign s_axis_ready = m_axis_ready;

    always @(posedge axi_clk) begin
        if (!axi_reset_n) begin
            m_axis_valid <= 1'b0;
            m_axis_data  <= {DATA_WIDTH{1'b0}};
            m_axis_tlast <= 1'b0;
        end else if (s_axis_valid && s_axis_ready) begin
            for (i = 0; i < DATA_WIDTH/8; i = i + 1)
                m_axis_data[i*8 +: 8] <= 8'hFF - s_axis_data[i*8 +: 8];

            m_axis_valid <= 1'b1;
            m_axis_tlast <= s_axis_tlast;
        end else if (m_axis_valid && m_axis_ready) begin
            m_axis_valid <= 1'b0;
            m_axis_tlast <= 1'b0;
        end
    end
endmodule