import sys
import trace_calls

sys.settrace(trace_calls.trace_calls)

import fdp
d3d = fdp.D3D()
shot = d3d.s176778
bes = shot.bes