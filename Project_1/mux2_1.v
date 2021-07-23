// File: mux2_1.v
// Generated by MyHDL 0.11
// Date: Mon Jun  7 22:40:04 2021


`timescale 1ns/10ps

module mux2_1 (
    Output,
    a,
    b,
    selector
);


output [3:0] Output;
reg [3:0] Output;
input [3:0] a;
input [3:0] b;
input [1:0] selector;




always @(a, selector, b) begin: MUX2_1_COMB
    case (selector)
        'h0: begin
            Output = a;
        end
        'h1: begin
            Output = b;
        end
        default: begin
            Output = 0;
        end
    endcase
end

endmodule