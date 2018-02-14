

def test_bes(setup_nstx):
    nstx = setup_nstx
    dir(nstx.s141240.bes)
    for signal in nstx.s141240.bes:
        pass
    nstx.s141240.bes.ch01[:]
    nstx.s204320.bes.ch01[:]
