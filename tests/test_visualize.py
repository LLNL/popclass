"""
Test that base visualization produces a figure
"""
import numpy as np
import pytest

from popclass.model import PopulationModel
from popclass.visualization import plot_population_model


def test_plot_population_model():
    """
    Check that figure exists when calling the function
    """

    popmodel = PopulationModel.from_library(
        "popsycle_singles_sukhboldn20", library_path="popclass/data/"
    )
    fig, ax = plot_population_model(
        PopulationModel=popmodel,
        parameters=["log10tE", "log10piE"],
        bounds=None,
        legend=True,
    )

    assert fig


def test_figure_axes():
    """
    Check plotting returns axes connected to the figure
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE"]
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert ax.figure == fig


def test_parameters():
    """
    Check 2D figure labels match parameters
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE"]
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert [ax.get_xlabel(), ax.get_ylabel()] == parameters


def test_1D_parameter():
    """
    Check 1D figure is plotted and labels match a density histogram of parameter
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE"]
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert ax.get_xlabel() == parameters[0]
    assert ax.get_ylabel() == "density"


def test_plot_samples():
    """
    Check plotting functions return a figure when visualizing full sample distributions instead of density estimates
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    fig1, ax1 = plot_population_model(
        PopulationModel=popmodel,
        parameters=["log10tE", "log10piE"],
        plot_samples=True,
        plot_kdes=False,
    )
    fig2, ax2 = plot_population_model(
        PopulationModel=popmodel,
        parameters=["log10tE"],
        plot_samples=True,
        plot_kdes=False,
    )
    assert fig1
    assert fig2


def test_bounds():
    """
    Check figure bounds are adjusted as specified
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE"]
    bounds = np.array([[0.0, 3.0], [-2.0, 0.0]])
    fig, ax = plot_population_model(
        PopulationModel=popmodel, parameters=parameters, bounds=bounds
    )
    figure_bounds = np.array([ax.get_xbound(), ax.get_ybound()])
    np.testing.assert_almost_equal(figure_bounds, bounds)


def test_dimensions():
    """
    Check that ValueError is raised if too many parameters given to visualize
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE", "f_blend_I"]
    with pytest.raises(ValueError):
        fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
