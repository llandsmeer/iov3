#!/usr/bin/env python3
import arbor as A

import subprocess as sp
from pathlib import Path
from time import perf_counter as pc

# Auto-generated file, please copy to eg main.py

here = Path(__file__).parent

def nml_load_cell():
    nml = A.neuroml(here / 'mrf' / 'C51A.nml').cell_morphology("C51A", allow_spherical_root=True)
    lbl = A.label_dict()
    lbl.append(nml.segments())
    lbl.append(nml.named_segments())
    lbl.append(nml.groups())
    lbl['all'] = '(all)'
    dec = A.load_component(here / 'acc' / 'C51A.acc').component
    return nml.morphology, lbl, dec

def mk_cat():
    sp.run('arbor-build-catalogue local cat', shell=True, check=True)
    res = A.default_catalogue()
    cat = A.load_catalogue(here / 'local-catalogue.so')
    res.extend(cat, '')
    return res

morph, labels, decor = nml_load_cell()

decor.discretization(A.cv_policy_every_segment())

cell = A.cable_cell(morph, labels, decor)
sim  = A.single_cell_model(cell)

sim.properties.catalogue = mk_cat()

# Add probes here (example below)
sim.probe('voltage', '(location 0 0.5)', frequency=10) # probe center of the root (likely the soma)

# Now run the simulation
print('Running simulation for 1s...')
t0 = pc()
sim.run(1000, 0.0025)
t1 = pc()
print(f'Simulation done, took: {t1-t0:.3f}s')

print('Trying to plot...')
try:
  import pandas as pd
  import seaborn as sns

  tr = sim.traces[0]
  df = pd.DataFrame({'t/ms': tr.time, 'U/mV': tr.value})

  sns.relplot(data=df, kind='line', x='t/ms', y='U/mV', ci=None).set_titles('Probe at (location 0 0.5)').savefig('C51A.pdf')
  print('Ok, generated C51A.pdf')
except:
  print('Failure, are seaborn and matplotlib installed?')
