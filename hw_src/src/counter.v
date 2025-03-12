module counter (
    input i_Clk,
    input i_Rst,
    input i_Tx_Active,
    output reg o_Tx_DV,
    output reg [7:0] o_Count
);

    always @ (posedge i_Clk)
    begin
        if (i_Rst)
            begin
                o_Count <= 0;
                o_Tx_DV <= 0;
            end
        else if (!i_Tx_Active)
            begin
                o_Count <= (o_Count == 8'hFF) ? 0 : o_Count + 1;
                o_Tx_DV <= 1; // Trigger UART
            end
        else
            begin
                o_Tx_DV <= 0;
            end
    end
endmodule