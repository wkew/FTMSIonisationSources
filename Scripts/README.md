# Scripts for Data Processing
Associated Scripts for FTMS Ionisation Sources Comparisons

#### All scripts are shared with the same [license](../LICENSE) as the rest of this repository. This is the GNU GPLv3 License.

### Spectrum Plotter
File [0-SpectrumPlotter.py](0-SpectrumPlotter.py) loads in raw Bruker SolariX fids and plots them using the [Spike](https://pypi.python.org/pypi/spike_py/0.6.3) package.

### Process Data
File [1-Process-Data.py](1-Process-Data.py) reads in the data assigned by Formularity and reprocesses it for ease with other scripts.

File [1-Process-Data-Part2.py](1-Process-Data-Part2.py) does a similar thing but outputs the data in groups (by ionisation source).

File [X-CombinedNegative.py](X-CombinedNegative.py) reads in deprotonated and radical assignments from Formularity and generates a single, combined output. It does not have a conflict resolution method as this was not required in this instance.

### Further Process Data
The various 'HitCollator' files collate the assignments for several statistics to be calculated, i.e. mass errors, number of radicals, or just overall information.

### Visualise Data
File [4-DataVisualisation.py](4-DataVisualisation.py) produces panel plots in the form of van krevelen, DBE vs C number, or AImod vs C number plots.

File [4-DataVisualisation-HeteroClass.py](4-DataVisualisation-HeteroClass.py) produces two types of heteroatomic class plots.

File [4-DataVisualisation-Uniques.py](4-DataVisualisation-Uniques.py) produces van Krevelen and DBE plots of the unique formula for each ionisation source in one plot.

File [4-DataViz-Errors.py](4-DataViz-Errors.py) produces mass error distribution plots.

File [5-DataIntersections.py](5-DataIntersections.py) uses the [PyUpSet](https://github.com/ImSoErgodic/py-upset) package to calculate intersections of assignments and produce UpSet plots. The main source of PyUpSet was modified and is provided in [visualisation.py](visualisation.py) for some aesthetic and practical improvements.

File [6-InteractiveVanKrevelens.py](6-InteractiveVanKrevelens.py) produces interactive van krevelen diagrams based on the [Bokeh](https://bokeh.pydata.org/en/latest/) package, and requires the template files to be present in the output directory.

## Notes

Many of these scripts contain significant sections of commented out code. This was for development and is included for posterity or reference. The scripts should be self-sufficient and run without modification (beyond the obvious pre-requisite of having the relative paths correct)
