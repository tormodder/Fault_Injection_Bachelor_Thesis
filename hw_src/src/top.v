module top (
    input CLK_50,
    input [0:0] SW,
    output [7:0] count_out,
    output clk_out,
    //output o_Tx_Serial,
    output o_Rst
);

    wire [7:0]  w_Count;
    wire        w_Tx_Active;
    wire        w_Tx_Done;
    wire        w_Tx_DV;

    parameter BAUD_RATE = 115200;
    parameter CLOCK_FREQ = 50000000;
    parameter TICKS_PER_BIT = 434; //CLOCK_FREQ / BAUD_RATE;

    counter my_counter (
        .i_Clk(CLK_50),
        .i_Rst(SW),
        .i_Tx_Active(1'b0),
        .o_Tx_DV(w_Tx_DV),
        .o_Count(w_Count)
    );
/*
    uart_tx #(.CLKS_PER_BIT(TICKS_PER_BIT)) uart (
        .i_Clock(CLK_50),
        .i_Tx_DV(w_Tx_DV),
        .i_Tx_Byte(w_Count),
        .o_Tx_Active(w_Tx_Active),
        .o_Tx_Serial(o_Tx_Serial),
        .o_Tx_Done(w_Tx_Done)
    );
*/
    assign clk_out = CLK_50;
    assign o_Rst = SW;
    assign count_out = w_Count;

endmodule