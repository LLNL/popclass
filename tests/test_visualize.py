"""
Test that base visualization produces a figure
"""
import pytest

from popclass.model import PopulationModel
from popclass.visualization import plot_population_model

def test_plot_population_model():
    """
    Check that figure exists when calling the function
    """

    popmodel = PopulationModel.from_library('popsycle_singles_sukhboldn20', library_path='popclass/data/')

    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=['log10tE', 'log10piE'], bounds=None, legend=True)

    assert(fig)



