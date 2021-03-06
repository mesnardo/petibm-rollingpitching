"""Plot the instantaneous force coefficients and compare grid resolutions."""

from matplotlib import pyplot
import pathlib

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]
data = {}

# Process force coefficients for simulation on coarse mesh.
label = 'Coarse'
simudir = maindir / 'run1'
config = rodney.WingKinematics(Re=200.0, St=0.6, psi=90.0, nt_period=2000)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
rodney.print_stats(label, *rodney.get_stats(solution, limits=(4, 5)))
data[label] = dict(config=config, solution=solution,
                   plot_kwargs=dict(linestyle='-', color='C0'))

# Process force coefficients for simulation on intermediate mesh.
label = 'Nominal'
simudir = maindir / 'run3'
config = rodney.WingKinematics(Re=200.0, St=0.6, psi=90.0, nt_period=2000)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
rodney.print_stats(label, *rodney.get_stats(solution, limits=(4, 5)))
data[label] = dict(config=config, solution=solution,
                   plot_kwargs=dict(linestyle='-', color='C3'))

# Process force coefficients for simulation on finer mesh.
label = 'Fine'
simudir = maindir / 'run4'
config = rodney.WingKinematics(Re=200.0, St=0.6, psi=90.0, nt_period=2000)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
rodney.print_stats(label, *rodney.get_stats(solution, limits=(4, 5)))
data[label] = dict(config=config, solution=solution,
                   plot_kwargs=dict(linestyle='--', color='black'))

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim, ylim = (3.0, 5.0), (-6.0, 6.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
for label, subdata in data.items():
    solution, plot_kwargs = subdata['solution'], subdata['plot_kwargs']
    ax1.plot(solution.t, solution.ct, label=label, **plot_kwargs)
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
for label, subdata in data.items():
    solution, plot_kwargs = subdata['solution'], subdata['plot_kwargs']
    ax2.plot(solution.t, solution.cl, label=label, **plot_kwargs)
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
for label, subdata in data.items():
    solution, plot_kwargs = subdata['solution'], subdata['plot_kwargs']
    ax3.plot(solution.t, solution.cz, label=label, **plot_kwargs)
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)

if args.extra_data:
    # Add the force coefficients from Li and Dong (2016).
    # Data were digitized from Figure 9 of the article.
    scatter_kwargs = dict(s=10, facecolors='none', edgecolors='black')
    ax1.scatter(*rodney.li_dong_2016_load_ct(),
                label='Li & Dong (2016)', **scatter_kwargs)
    ax2.scatter(*rodney.li_dong_2016_load_cl(),
                label='Li & Dong (2016)', **scatter_kwargs)
    ax3.scatter(*rodney.li_dong_2016_load_cz(),
                label='Li & Dong (2016)', **scatter_kwargs)

ax1.legend(frameon=False, prop=dict(size=10),
           scatterpoints=3, labelspacing=0.25)
fig.tight_layout()

if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients_compare_dx.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
