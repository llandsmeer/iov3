import sys

import numpy as np
import matplotlib.pyplot as plt

from sim_jneuroml import simulate as jnml
from sim_nmlcc import simulate as nmlcc

ok = ('na_s', 'kdr', 'k_s', 'na_a')
ok = []
allchannels = (
        'na_s', 'kdr', 'k_s', 'cal',
        'cah', 'kca', 'h', 'cacc',
        'na_a', 'k_a', 'leak')

fig, ax = plt.subplots(nrows=3, ncols=4, sharex=False, sharey=True)
ax = ax.flatten()

for i, channel in enumerate(allchannels):
    channels = [channel] + list(ok)
    tr1 = jnml(channels=channels, tfinal=300)
    tr2 = nmlcc(channels=channels, tfinal=300)
    d = 0
    for j, (t1, t2) in enumerate(zip(tr1, tr2)):
        x = np.array(t1.value)
        y = np.array(t2.value)
        tx = np.array(t1.time)
        ty = np.array(t2.time)
        d = max(d, max(abs(x - y)))
        assert np.allclose(tx, ty)
        label = t1.location
        ax[i].plot(tx, x, color='red')
        ax[i].plot(ty, y, color='blue')
    ax[i].axis('off')
    ax[i].set_title(f'{channel} ({d:.1f}mV)')

tr1 = jnml(channels=allchannels, tfinal=1000)
tr2 = nmlcc(channels=allchannels, tfinal=1000)
d = 0
for t1, t2 in zip(tr1, tr2):
    x = np.array(t1.value)
    y = np.array(t2.value)
    tx = np.array(t1.time)
    ty = np.array(t2.time)
    d = max(d, max(abs(x - y)))
    assert np.allclose(tx, ty)
    label = t1.location
    ax[-1].plot(tx, x, color='red')
    ax[-1].plot(ty, y, color='blue')
ax[-1].axis('off')
ax[-1].set_title(f'io ({d:.1f}mV)')
plt.suptitle(f'Single channel comparison between jNeuroML (red) and nmlcc (blue) + max error')
plt.tight_layout()
plt.show()
