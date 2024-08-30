"""
Test to check visualization.py works
"""
import sys
sys.path.append("..")
from popclass.model import PopulationModel
from popclass.visualization import plot_population_model
import matplotlib.pyplot as plt
import numpy as np

def test_plotting_figure():
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    parameters = ['log10tE', 'log10piE']
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert(ax.figure == fig)
    
def test_parameters():
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    parameters = ['log10tE', 'log10piE']
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert([ax.get_xlabel(), ax.get_ylabel()] == parameters)
    
def test_bounds():
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    parameters = ['log10tE', 'log10piE']
    bounds = np.array([[0, 3], [-2, 0]])
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters, bounds = bounds)
    figure_bounds = np.array([ax.get_xbound(), ax.get_ybound()])
    np.testing.assert_almost_equal(figure_bounds, bounds)