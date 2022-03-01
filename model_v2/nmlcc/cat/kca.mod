NEURON {
  SUFFIX kca
  USEION ca READ cai
  USEION k WRITE ik READ ek
  RANGE conductance
}

PARAMETER {
  conductance = 0.00001 (uS)
}

STATE { gates_z_q }

INITIAL {
  LOCAL gates_z_forwardRate_ca_norm, gates_z_forwardRate_r, gates_z_inf

  gates_z_forwardRate_ca_norm = 19.999999494757503 * cai
  if (gates_z_forwardRate_ca_norm > 0.009999999776482582) {
    gates_z_forwardRate_r = 0.009999999776482582
  } else {
    if (gates_z_forwardRate_ca_norm <= 0.009999999776482582) {
      gates_z_forwardRate_r = gates_z_forwardRate_ca_norm
    } else {
      gates_z_forwardRate_r = 0
    }
  }
  gates_z_inf = gates_z_forwardRate_r * (0.014999999664723873 + gates_z_forwardRate_r)^-1
  gates_z_q = gates_z_inf
}

DERIVATIVE dstate {
  LOCAL gates_z_forwardRate_ca_norm, gates_z_forwardRate_r, gates_z_inf, gates_z_tau

  gates_z_forwardRate_ca_norm = 19.999999494757503 * cai
  if (gates_z_forwardRate_ca_norm > 0.009999999776482582) {
    gates_z_forwardRate_r = 0.009999999776482582
  } else {
    if (gates_z_forwardRate_ca_norm <= 0.009999999776482582) {
      gates_z_forwardRate_r = gates_z_forwardRate_ca_norm
    } else {
      gates_z_forwardRate_r = 0
    }
  }
  gates_z_inf = gates_z_forwardRate_r * (0.014999999664723873 + gates_z_forwardRate_r)^-1
  gates_z_tau = (0.014999999664723873 + gates_z_forwardRate_r)^-1
  gates_z_q' = (gates_z_inf + -1 * gates_z_q) * gates_z_tau^-1
}

BREAKPOINT {
  SOLVE dstate METHOD cnexp
  LOCAL g

  g = conductance * gates_z_q
  ik = g * (v + -1 * ek)
}

