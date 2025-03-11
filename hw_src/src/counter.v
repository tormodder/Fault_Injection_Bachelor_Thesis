module counter (
    input clk,
    input rst,
    output reg [15:0] count
);

    always @ (posedge clk)
    begin
        if (rst)
            count <= 0;
        else if (count == 16'hFFFF)
            count <= 0;
        else
            count <= count+1;
    end
endmodule