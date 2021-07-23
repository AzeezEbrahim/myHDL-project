module tb_CPU;

wire [31:0] data;
reg [31:0] data_in;
reg write_enable;
reg clock;
wire reset;

initial begin
    $from_myhdl(
        data_in,
        write_enable,
        clock
    );
    $to_myhdl(
        data,
        reset
    );
end

CPU dut(
    data,
    data_in,
    write_enable,
    clock,
    reset
);

endmodule
