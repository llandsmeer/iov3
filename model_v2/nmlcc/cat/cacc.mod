NEURON {
  SUFFIX cacc
  USEION cl READ ecl WRITE icl
  RANGE conductance
}

PARAMETER {
  conductance = 0.00001 (uS)
}

BREAKPOINT {
  LOCAL gates_m_steadyState_x, g

  gates_m_steadyState_x = (1 + exp(1.1111111405455043 * (3.700000047683716 + -1000000 * cai)))^-1
  g = conductance * gates_m_steadyState_x
  icl = g * (v + -1 * ecl)
}

