#!/usr/bin/env python3

import os
import glob
import subprocess

import numpy as np
import matplotlib.pyplot as plt

import arbor
from arbor import mechanism as mech
from arbor import location as loc

ARBOR_BUILD_CATALOGUE = 'arbor-build-catalogue'
def compile_smol_model():
    expected_fn = './nmlccv2-catalogue.so'
    if os.path.exists(expected_fn):
        needs_recompile = False
        for src in glob.glob('model_v2/nmlcc/cat/*.mod'):
            if os.path.getmtime(src) > os.path.getmtime(expected_fn):
                print(src, 'is newer than compiled library')
                needs_recompile = True
        if not needs_recompile:
            return arbor.load_catalogue(expected_fn)
    res = subprocess.getoutput(f'{ARBOR_BUILD_CATALOGUE} nmlccv2 model_v2/nmlcc/cat')
    path = res.split()[-1]
    print(res)
    assert path[0] == '/' and path.endswith('.so')
    return arbor.load_catalogue(path)

filename = 'model_v2/C51A.cell.nml'

nml = arbor.neuroml(filename)

cell_id, = nml.cell_ids()
morpho_data = nml.cell_morphology(cell_id)
morpho = morpho_data.morphology

morpho_segments = morpho_data.segments()
morpho_named = morpho_data.named_segments()
morpho_groups = morpho_data.groups()

labels = arbor.label_dict()
labels.append(morpho_segments)
labels.append(morpho_named)
labels.append(morpho_groups)

labels['stim_site'] = '(location 1 0.5)' # site for the stimulus, in the middle of branch 1.
labels['axon_end']  = '(restrict (terminal) (region "axon_group"))' # end of the axon.
labels['dend_end']  = '(restrict (terminal) (region "dendrite_group"))' # end of the dendrite.
labels['root']      = '(root)' # the start of the soma in this morphology is at the root of the cell.

decor = arbor.decor()
SOMA = '"soma_group"'
DEND = '"dendrite_group"'
AXON = '"axon_group"'
ALL = '"all"'

decor.paint(SOMA, arbor.density('na_s'))
decor.paint(SOMA, arbor.density('kdr'))
decor.paint(SOMA, arbor.density('k'))
decor.paint(SOMA, arbor.density('cal'))
decor.paint(DEND, arbor.density('cah'))
decor.paint(DEND, arbor.density('kca'))
decor.paint(DEND, arbor.density('h'))
decor.paint(DEND, arbor.density('cacc'))
decor.paint(AXON, arbor.density('na_a'))
decor.paint(AXON, arbor.density('k'))
decor.paint(ALL, arbor.density('leak'))
decor.set_property(cm=0.01) # Ohm.cm
decor.set_property(Vm=-65.0) # mV
decor.paint(SOMA, rL=100) # Ohm.cm
decor.paint(DEND, rL=100) # Ohm.cm
decor.paint(AXON, rL=100) # Ohm.cm
decor.paint(ALL, arbor.density('ca_conc'))

cell = arbor.cable_cell(morpho, labels, decor)
m = arbor.single_cell_model(cell)
m.properties.catalogue.extend(compile_smol_model(), "")

m.probe('voltage', where='"root"',      frequency=1) # frequency is in kHz
m.probe('voltage', where='"dend_end"',  frequency=1)
m.probe('voltage', where='"axon_end"',  frequency=1)

print('Simulation start.')
m.run(1000, dt=0.025)
print('Simulation done.')

dend_end = [str(x) for x in cell.locations('"dend_end"')]
for tr in m.traces:
    x = np.array(tr.value)
    print(x)
    t = np.array(tr.time) / 1000
    label = tr.location
    if str(tr.location) in dend_end:
        label = f'{label} dend'
    plt.plot(t, x, label=label)
plt.title('nmlcc')
plt.legend()
plt.show()
