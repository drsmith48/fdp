import cProfile, pstats, io
import fdp

pro = cProfile.Profile(builtins=False)

d3d = fdp.D3D()
shot = d3d.s176778
pro.enable()
bes = shot.bes
pro.disable()

ps = pstats.Stats(pro)
ps.sort_stats('cumtime').print_stats('fdp')