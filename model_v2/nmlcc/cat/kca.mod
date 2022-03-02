NEURON {
  SUFFIX kca
  USEION ca READ cai
  NONSPECIFIC_CURRENT ik
  : USEION k WRITE ik READ ek ? WRONG
  RANGE conductance
}

PARAMETER {
  conductance = 0.00001 (uS)
}

STATE { gates_z_q }

INITIAL {
  LOCAL gates_z_forwardRate_ca_norm, gates_z_forwardRate_r, gates_z_inf

  gates_z_forwardRate_ca_norm = 0.00002 * cai
  if (gates_z_forwardRate_ca_norm > 0.01) {
    gates_z_forwardRate_r = 0.01
  } else if (gates_z_forwardRate_ca_norm <= 0.01) {
      gates_z_forwardRate_r = gates_z_forwardRate_ca_norm
  }
  gates_z_inf = gates_z_forwardRate_r * (0.015 + gates_z_forwardRate_r)^-1
  gates_z_q = gates_z_inf
}

DERIVATIVE dstate {
  LOCAL gates_z_forwardRate_ca_norm, gates_z_forwardRate_r, gates_z_inf, gates_z_tau

  gates_z_forwardRate_ca_norm = 0.00002 * cai
  if (gates_z_forwardRate_ca_norm > 0.01) {
    gates_z_forwardRate_r = 0.01
  } else if (gates_z_forwardRate_ca_norm <= 0.01) {
      gates_z_forwardRate_r = gates_z_forwardRate_ca_norm
  }
  gates_z_inf = gates_z_forwardRate_r * (0.015 + gates_z_forwardRate_r)^-1
  gates_z_tau = (0.015 + gates_z_forwardRate_r)^-1
  gates_z_q' = (gates_z_inf + -1 * gates_z_q) * gates_z_tau^-1
}

BREAKPOINT {
  SOLVE dstate METHOD cnexp
  LOCAL g, ek
  ek = -75

  g = conductance * gates_z_q
  ik = g * (v + -1 * ek)
}

