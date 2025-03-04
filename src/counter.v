module counter (
    input clk,
    input rst,
    output reg [16:0] count
);

    always @ (posedge clk)
    begin
        if (rst)
            count <= 0;
        else if (count == 100000)
            count <= 0;
        else
            count <= count+1;
    end
endmodule