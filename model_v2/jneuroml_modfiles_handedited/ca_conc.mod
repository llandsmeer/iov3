TITLE Mod file for component: Component(id=ca_conc type=fixedFactorConcentrationModel)
COMMENT
    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.7.0
         org.neuroml.model   v1.7.0
         jLEMS               v0.10.2
ENDCOMMENT
NEURON {
    SUFFIX ca_conc
    USEION ca READ cao, ica WRITE cai VALENCE 2
    RANGE cai
    RANGE cao
    GLOBAL initialExtConcentration
    RANGE restingConc                       : parameter
    RANGE decayConstant                     : parameter
    RANGE surfaceArea                       : parameter
    RANGE shellDepth                        : parameter
    RANGE Faraday                           : parameter
    RANGE AREA_SCALE                        : parameter
    RANGE LENGTH_SCALE                      : parameter
    RANGE effectiveRadius                   : derived variable
    RANGE eqshellDepth                      : derived variable
    RANGE innerRadius                       : derived variable
    RANGE shellVolume                       : derived variable
}

UNITS {
    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (A) = (amp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (kHz) = (kilohertz)
    (mM) = (millimolar)
    (um) = (micrometer)
    (umol) = (micromole)
    (S) = (siemens)
}
CONSTANT {
   pi = 3.14159
}
PARAMETER {
    restingConc = 0 (mM)
    decayConstant = 33.333336 (ms)
    Faraday = 0.0964853 (C / umol)
    shellDepth = 0.001 (um)
    AREA_SCALE = 1.0E12 (um2)
    LENGTH_SCALE = 1000000 (um)
    diam (um)
}
ASSIGNED {
    rate_concentration (mM/ms)
    initialExtConcentration (mM)
    surfaceArea 
    effectiveRadius                   : derived variable
    eqshellDepth                      : derived variable
    innerRadius                       : derived variable
    shellVolume                       : derived variable
}
STATE {
    extConcentration (mM) 
    cai
}
INITIAL {
    cai = 3.7152
    initialExtConcentration = cao
    surfaceArea = pi*diam*diam/4
    rates(ica)
    rates(ica) ? To ensure correct initialisation.
    extConcentration = initialExtConcentration
}
BREAKPOINT {
    SOLVE states METHOD cnexp
    if (cai  < 0) {
        cai = 0 ? standard OnCondition
    }
}
DERIVATIVE states {
    rates(ica)
    cai' = rate_concentration
}
PROCEDURE rates(ica) {
    LOCAL iCa
    iCa = -1 * (0.01) * ica * surfaceArea :   iCa has units (nA) ; ica (built in to NEURON) has units (mA/cm2)...
    effectiveRadius = LENGTH_SCALE  * (surfaceArea/(  AREA_SCALE   * (4 * 3.14159)))^0.5 ? evaluable
    eqshellDepth = shellDepth  - ((  shellDepth   *   shellDepth  ) /   effectiveRadius  ) ? evaluable
    innerRadius = effectiveRadius  -  eqshellDepth ? evaluable
    shellVolume = (4 * (  effectiveRadius   *  effectiveRadius  *   effectiveRadius  ) * 3.14159 / 3) - (4 * (  innerRadius   *  innerRadius  *   innerRadius  ) * 3.14159 / 3) ? evaluable
    rate_concentration = iCa / (2 *  Faraday  *   shellVolume  ) - ((  cai   -   restingConc  ) /   decayConstant  ) ? Note units of all quantities used here need to be consistent!
}
