"""
To be replaced by assertion tests later
Example script making a plot with visualization.py
"""

import sys
sys.path.append("..")
import numpy as np
import matplotlib.pyplot as plt

from popclass.model import PopulationModel
from popclass.visualization import plot_population_model

popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20', library_path='../popclass/data/')

plot_population_model(PopulationModel=popmodel, parameters=['log10tE', 'log10piE'], plot_samples=True, bounds=None, legend=True)
plt.show()
