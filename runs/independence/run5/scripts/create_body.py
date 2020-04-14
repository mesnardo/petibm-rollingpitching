"""Create the body and write the coordinates to a file."""

import pathlib

import petibmpy

import rodney


# Set the simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]

# Create the configuration for the wing kinematics.
wing = rodney.WingKinematics(nt_period=2000)

# Discretize the body.
wing.create_body(ds=0.01, thickness=0.03, sort_points=True)
x, y, z = wing.get_coordinates()

# Save the coordinates into a file.
filepath = simudir / 'wing.body'
petibmpy.write_body(filepath, x, y, z)
