"""
Test that base visualization produces a figure
"""
import pytest
import numpy as np
from popclass.model import PopulationModel
from popclass.visualization import plot_population_model

def test_plot_population_model():
    """
    Check that figure exists when calling the function
    """

    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20', library_path='popclass/data/')
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=['log10tE', 'log10piE'], bounds=None, legend=True)

    assert(fig)

def test_figure_axes():
    """
    Check plotting returns axes connected to the figure
    """
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    parameters = ['log10tE', 'log10piE']
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert(ax.figure == fig)
    
def test_parameters():
    """
    Check 2D figure labels match parameters
    """
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    parameters = ['log10tE', 'log10piE']
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert([ax.get_xlabel(), ax.get_ylabel()] == parameters)
    
def test_bounds():
    """
    Check figure bounds are adjusted as specified
    """
    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20')
    parameters = ['log10tE', 'log10piE']
    bounds = np.array([[0., 3.], [-2., 0.]])
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters, bounds = bounds)
    figure_bounds = np.array([ax.get_xbound(), ax.get_ybound()])
    np.testing.assert_almost_equal(figure_bounds, bounds)