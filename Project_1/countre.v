// File: countre.v
// Generated by MyHDL 0.11
// Date: Tue Jun  8 18:22:56 2021


`timescale 1ns/10ps

module countre (
    count,
    enable,
    clock,
    reset
);


output [11:0] count;
reg [11:0] count;
input enable;
input clock;
input reset;




always @(posedge clock) begin: COUNTRE_SEQ
    if (reset == 1) begin
        count <= 0;
    end
    else begin
        if (enable) begin
            count <= (count + 1);
        end
    end
end

endmodule