"""
Test that visualize will make a plot.
This won't run with the tests for now, 
but will make testing faster
"""

from popclass.model import PopulationModel
from popclass.visualization import plot_population_model

popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')

plot_population_model(PopulationModel=popmodel)