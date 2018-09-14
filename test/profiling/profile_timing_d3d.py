"""
Profile execution time of function calls with cProfile (not line-by-line timing)
"""

import cProfile, pstats
import fdp
import time

pro = cProfile.Profile(builtins=False)


d3d = fdp.D3D() # ~ 2 s exec time
shot = d3d.s176778 # ~ 1 ms exec time
mag = shot.magnetics # 50 ms exec time

pro.enable()
ip = mag.ip
ip[:]

pro.disable()

ps = pstats.Stats(pro)
ps.sort_stats('cumtime').print_stats('numpy', 60)
ps.sort_stats('cumtime').print_stats('signal', 60)