
import sys

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    try:
        caller = frame.f_back
        caller_name = caller.f_code.co_name
        caller_lineno = caller.f_lineno
        call = frame.f_code # code object in this frame
        call_name = call.co_name # name of code object
        caller_filename = caller.f_code.co_filename
        call_filename = call.co_filename  # filename for code object
    except:
        return
    if call_name == 'write':
        # Ignore write() calls from print statements
        return
    if ('fdp' not in call_filename) or ('fdp' not in caller_filename):
        return
    caller_filename = pathlib.Path(caller.f_code.co_filename)
    call_filename = pathlib.Path(call.co_filename)  # filename for code object
    caller_filename = caller_filename.relative_to('/home/smithdr/fdp/')
    call_filename = call_filename.relative_to('/home/smithdr/fdp/')
    print('{:16s} (line {:03d} in {:20s})  calls  {:16s} in {}'.format(caller_name, caller_lineno, caller_filename.as_posix(),
        call_name, call_filename.as_posix()))
    return

# sys.settrace(trace_calls)
print('*** import fdp')
import fdp
print('*** calling fdp.D3D()')
d3d = fdp.D3D()
print('*** calling shot = d3d.s176778')
shot = d3d.s176778
print('*** calling bes = shot.bes')
bes = shot.bes
print('*** calling signal = bes.slow01')
signal = bes.slow01
print('*** calling signal[:]')
signal[:]
print(signal.shape, signal.size, signal.axes)