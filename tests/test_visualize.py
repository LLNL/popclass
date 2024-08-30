"""
Test to check visualization.py works
"""

from popclass.model import PopulationModel
from popclass.visualization import plot_population_model
import matplotlib.pyplot as plt

def test_plotting_figure():
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=['log10tE', 'log10piE'], plot_samples=True, bounds=None, legend=True)
    assert(plt.gcf().number == 1)

