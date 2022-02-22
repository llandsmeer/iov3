NEURON {
  SUFFIX leak
  USEION leak READ eleak WRITE ileak
  RANGE conductance
}

PARAMETER {
  conductance = 0.00001 (uS)
}

BREAKPOINT {
  LOCAL g

    g = conductance
  ileak = g * (v + -1 * eleak)
}

