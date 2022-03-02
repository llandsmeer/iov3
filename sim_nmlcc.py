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

def simulate(
        filename = 'model_v2/C51A.cell.nml',
        channels = ('na_s', 'kdr', 'k_s', 'cal', 'cah', 'kca', 'h', 'cacc', 'na_a', 'k_a', 'leak'),
        tfinal = 1000
        ):
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

    def mech(group, name, **kwargs):
        decor.paint(group, arbor.density(name, dict(**kwargs)))

    if 'na_s' in channels:
        mech(SOMA, 'na_s', conductance=0.030)
    if 'kdr' in channels:
        mech(SOMA, 'kdr',  conductance=0.030)
    if 'cal' in channels:
        mech(SOMA, 'cal',  conductance=0.045)
    if 'cah' in channels:
        mech(DEND, 'cah',  conductance=0.010)
    if 'kca' in channels:
        mech(DEND, 'kca',  conductance=0.220)
    if 'h' in channels:
        mech(DEND, 'h',    conductance=0.015, eh=-43)
    if 'cacc' in channels:
        mech(DEND, 'cacc', conductance=0.000)
    if 'na_a' in channels:
        mech(AXON, 'na_a', conductance=0.200)
    if 'k_a' in channels:
        mech(AXON, 'k',    conductance=0.200)
    if 'k_s' in channels:
        mech(SOMA, 'k',    conductance=0.015)
    if 'leak' in channels:
        mech(ALL, 'leak', conductance=1.3e-05, eleak=10)

    decor.set_property(cm=0.01) # Ohm.cm
    decor.set_property(Vm=-65.0) # mV
    decor.paint(ALL, rL=100) # Ohm.cm

    decor.paint(ALL, ion_name='ca', rev_pot=120)
    decor.paint(ALL, ion_name='na', rev_pot=55)
    decor.paint(ALL, ion_name='k', rev_pot=-75)

    mech(ALL, 'ca_conc', initialConcentration=3.7152)

    cell = arbor.cable_cell(morpho, labels, decor)
    m = arbor.single_cell_model(cell)
    m.properties.catalogue.extend(compile_smol_model(), "")

    m.probe('voltage', where='"root"',      frequency=1) # frequency is in kHz
    m.probe('voltage', where='"dend_end"',  frequency=1)
    m.probe('voltage', where='"axon_end"',  frequency=1)

    m.run(tfinal, dt=0.025)

    return m.traces

def main():
    traces = simulate()
    for tr in traces:
        x = np.array(tr.value)
        t = np.array(tr.time) / 1000
        label = tr.location
        plt.plot(t, x, label=label)
    plt.title('nmlcc')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
