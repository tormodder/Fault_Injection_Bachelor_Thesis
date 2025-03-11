module uart_tx (
    input wire clk,
    input wire rst,
    input wire [15:0] data,
    output reg tx
);

    parameter BAUD_RATE = 115200;
    parameter CLOCK_FREQ = 50000000;
    parameter TICKS_PER_BIT = CLOCK_FREQ / BAUD_RATE;

    reg [16:0] tx_shift_reg; // 1 start bit 15 data bits 1 stop bit
    reg [15:0] bit_counter; // counter for timing

    reg sending;

    always @(posedge clk) begin
        if (rst)
        begin
            sending <= 0;
            tx <= 1; // set idle high
        end
        else if (!sending)
        begin
            tx_shift_reg <= {1'b1, data[15:0], 1'b0};
            sending <= 1;
            bit_counter <= 0;
        end
        else
        begin
            if (bit_counter < TICKS_PER_BIT)
            begin
                bit_counter <= bit_counter + 1;
            end
            else
            begin
                bit_counter <= 0;
                tx_shift_reg <=  {1'b1, tx_shift_reg[16:1]};
                if (tx_shift_reg == 17'b00000000000000001)
                begin
                    sending <= 0;
                end
            end
            tx <= tx_shift_reg[0]; // send LSB first
        end
    end

endmodule