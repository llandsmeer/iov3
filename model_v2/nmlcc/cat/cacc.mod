NEURON {
  SUFFIX cacc
  USEION ca READ cai VALENCE 2
  NONSPECIFIC_CURRENT icl
  RANGE conductance
}

PARAMETER {
  conductance = 0.00001 (uS)
}

BREAKPOINT {
  LOCAL gates_m_steadyState_x, g, ecl
  ecl = -43.0
  gates_m_steadyState_x = (1 + exp(1.1111111405455043 * (3.700000047683716 + -1000000 * cai)))^-1
  g = conductance * gates_m_steadyState_x
  icl = 1000 * g * (v + -1 * ecl) * 0
}

