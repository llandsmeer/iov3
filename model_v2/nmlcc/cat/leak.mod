NEURON {
  SUFFIX leak
  NONSPECIFIC_CURRENT ileak
  RANGE conductance
}

PARAMETER {
  conductance = 0.00001 (uS)
}

BREAKPOINT {
  LOCAL g, eleak

  eleak = 10
  g = conductance
  ileak = g * (v + -1 * eleak)
}

