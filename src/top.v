module top (
    input CLK_50,
    input [0:0] SW,
    output [16:0] count_out,
    output clk_out,
    output uart_tx
);

    counter my_counter (
        .clk(CLK_50),
        .rst(SW),
        .count(count_out)
    );

    uart_tx uart (
        .clk(CLK_50),
        .rst(SW),
        .data(count_out[7:0]),
        .tx(uart_tx)
    );

    assign clk_out = CLK_50;
endmodule