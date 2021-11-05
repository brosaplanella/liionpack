import liionpack as lp
import numpy as np
import pybamm

# Generate the netlist
netlist = lp.setup_circuit(Np=16, Ns=2, Rb=1e-4, Rc=1e-2, Ri=5e-2, V=3.2, I=80.0)

output_variables = [  
    'X-averaged total heating [W.m-3]',
    'Volume-averaged cell temperature [K]',
    'X-averaged negative particle surface concentration [mol.m-3]',
    'X-averaged positive particle surface concentration [mol.m-3]',
    'X-averaged electrolyte concentration [mol.m-3]',
    ]

# Heat transfer coefficients
htc = np.ones(32) * 10
#initial_eleConc=np.ones(32) * 1000.0
initial_eleConc=np.array([1000., 1000., 2000., 2000., 1000., 1000., 1000., 1000., 1000.,
       1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000.,
       1000., 1000., 1000., 1000., 1000., 3000., 3000., 3000., 1000.,
       1000., 1000., 1000., 1000., 1000.])

# Cycling experiment, using PyBaMM
experiment = pybamm.Experiment(
    ["Charge at 50 A for 30 minutes", "Rest for 15 minutes", "Discharge at 50 A for 30 minutes", "Rest for 30 minutes"],
    period="10 seconds",
)

# PyBaMM parameters
chemistry = pybamm.parameter_sets.Chen2020
parameter_values = pybamm.ParameterValues(chemistry=chemistry)

# Solve pack
output = lp.solve(netlist=netlist,
                  parameter_values=parameter_values,
                  experiment=experiment,
                  output_variables=output_variables,
                  htc=htc,initial_eleConc=initial_eleConc)
lp.plot_output(output)