module tb_instMem;

wire [31:0] inst;
reg [31:0] address;
reg [31:0] data_in;
reg [0:0] write_enable;

initial begin
    $from_myhdl(
        address,
        data_in,
        write_enable
    );
    $to_myhdl(
        inst
    );
end

instMem dut(
    inst,
    address,
    data_in,
    write_enable
);

endmodule
