"""
Line-by-line timing of functions/methods with kernprof/line_profiler
"""

import line_profiler
import fdp

profile = line_profiler.LineProfiler()

# add function/methods or full modules for profiling
profile.add_function(fdp.lib.container.container_factory)
profile.add_function(fdp.lib.container.init_class)
profile.add_function(fdp.lib.container.Container.__init__)

profile.enable()

d3d = fdp.D3D()
shot = d3d.s176778
magnetics = shot.magnetics

profile.disable()

profile.print_stats()