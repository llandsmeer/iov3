NEURON {
  SUFFIX ca_conc
  USEION ca READ cai, ica, cao
}

STATE { concentration extConcentration }

INITIAL {
  concentration = cai
  extConcentration = cao
}

DERIVATIVE dstate {
  LOCAL effectiveRadius, eqshellDepth, innerRadius, shellVolume

  effectiveRadius = 1000000 * exp(0.00000000000007957753576289935 * area)
  eqshellDepth = 0.0010000000474974513 + -0.0000010000000949949049 * effectiveRadius^-1
  innerRadius = effectiveRadius + -1 * eqshellDepth
  shellVolume = -4.1887868245442705 * innerRadius * innerRadius * innerRadius + 4.1887868245442705 * effectiveRadius * effectiveRadius * effectiveRadius
  concentration' = -0.030000001144409223 * concentration + ica * (0.19297059375 * shellVolume)^-1
}

BREAKPOINT {
  SOLVE dstate METHOD cnexp
  cai = concentration
  cao = extConcentration
}
