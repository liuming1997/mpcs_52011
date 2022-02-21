// This file is part of MPCS52011

load CountdownBy4.hdl,
output-file CountdownBy4.out,
compare-to CountdownBy4.cmp,
output-list time%S1.4.1 in%D1.6.1 load%B2.1.2 out%D1.6.1;

set in 0,
set load 1,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in 100,
set load 1,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in -12345,
set load 1,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;

set in 0,
set load 0,
tick,
output;

tock,
output;
