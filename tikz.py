from matplotlib import pyplot as pp
from matplotlib import style
from matplotlib2tikz import save as tikz_save
import numpy as np
fig = pp.figure()
style.use('ggplot')
t = np.arange(0.0, 2.0, 0.1)
s = np.sin(2*np.pi*t)
s2 = np.cos(2*np.pi*t)
pp.plot(t, s, 'o-', lw=4.1)
pp.plot(t, s2, 'o-', lw=4.1)
pp.xlabel('time(s)')
pp.ylabel('Voltage (mV)')
pp.title('Simple plot $\\frac{\\alpha}{2}$')
pp.grid(True)
tikz_save('E:\\mytikz.tex');