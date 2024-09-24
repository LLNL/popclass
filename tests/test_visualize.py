"""
Tests for the visualization.py functions
"""
import matplotlib.pyplot as plt
import numpy as np
import pytest

from popclass.model import CustomKernelDensity
from popclass.model import PopulationModel
from popclass.uq import NoneClassUQ
from popclass.visualization import get_bounds
from popclass.visualization import plot_population_model
from popclass.visualization import plot_rel_prob_surfaces


def test_get_bounds():
    """
    Check that the bounds function is returning an array of a given shape
    """
    popmodel = PopulationModel.from_library(
        "popsycle_singles_sukhboldn20", library_path="popclass/data/"
    )
    parameters = ["log10tE", "log10piE", "f_blend_I"]
    bounds = get_bounds(PopulationModel=popmodel, parameters=parameters)
    assert isinstance(bounds, np.ndarray)
    assert bounds.shape == (3, 2)


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


def test_model_plot_figure_axes():
    """
    Check plotting returns axes connected to the figure
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE"]
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert ax.figure == fig


def test_model_plot_parameters():
    """
    Check 2D figure labels match parameters
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE"]
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert [ax.get_xlabel(), ax.get_ylabel()] == parameters


def test_model_plot_1D_parameter():
    """
    Check 1D figure is plotted and labels match a density histogram of parameter
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE"]
    fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)
    assert ax.get_xlabel() == parameters[0]
    assert ax.get_ylabel() == "density"


def test_model_plot_samples():
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


def test_model_plot_bounds():
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


def test_model_plot_dimensions():
    """
    Check that ValueError is raised if too many parameters given to visualize
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE", "f_blend_I"]
    with pytest.raises(ValueError):
        fig, ax = plot_population_model(PopulationModel=popmodel, parameters=parameters)


def test_rel_prob_all_figures():
    """
    Check that the relative probability function returns N figures, where N is the number of classes in the input PopulationModel, and that the i-th ax is connected to the i-th figure
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    classes = popmodel.classes
    parameters = ["log10tE", "log10piE"]
    plt.close()
    figs, axes = plot_rel_prob_surfaces(
        PopulationModel=popmodel, parameters=parameters, N_bins=20
    )
    assert len(figs) == len(classes)
    assert len(axes) == len(classes)
    for counter in range(len(classes)):
        assert axes[counter].figure == figs[counter]


def test_rel_prob_parameters():
    """
    Check relative probability 2D plot labels match parameters
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    classes = popmodel.classes
    parameters = ["log10tE", "log10piE"]
    plt.close()
    figs, axes = plot_rel_prob_surfaces(
        PopulationModel=popmodel, parameters=parameters, N_bins=20
    )
    for counter in range(len(classes)):
        ax = axes[counter]
        assert [ax.get_xlabel(), ax.get_ylabel()] == parameters


def test_rel_prob_samples():
    """
    Check that the relative probability function returns figures when the option of plotting samples is on
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    classes = popmodel.classes
    parameters = ["log10tE", "log10piE"]
    plt.close()
    figs, axes = plot_rel_prob_surfaces(
        PopulationModel=popmodel, parameters=parameters, N_bins=20, plot_samples=True
    )
    assert figs
    assert axes


def test_rel_prob_bounds():
    """
    Check that the relative probability function works with user-specified bounds
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    parameters = ["log10tE", "log10piE"]
    bounds = np.array([[0.0, 3.0], [-2.0, 0.0]])
    plt.close()
    figs, axes = plot_rel_prob_surfaces(
        PopulationModel=popmodel, parameters=parameters, bounds=bounds, N_bins=20
    )
    for counter, fig in enumerate(figs):
        figure_bounds = np.array(
            [axes[counter].get_xbound(), axes[counter].get_ybound()]
        )
        np.testing.assert_almost_equal(figure_bounds, bounds)


def test_rel_prob_dimensions():
    """
    Check that ValueError is raised if the given parameters space for relative probability visualization is not 2D
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    with pytest.raises(ValueError):
        figs, axes = plot_rel_prob_surfaces(
            PopulationModel=popmodel, parameters=["log10tE"]
        )
    with pytest.raises(ValueError):
        figs, axes = plot_rel_prob_surfaces(
            PopulationModel=popmodel, parameters=["log10tE", "log10piE", "f_blend_I"]
        )


def test_none_class_all_figures():
    """
    Check that the relative probability function works with the None class, and N+1 figures are returned, where N is the number of classes. (Same as test_rel_prob_all_figures, but with additive UQ and custom kernel density.)
    """
    popmodel = PopulationModel.from_library("popsycle_singles_sukhboldn20")
    classes = popmodel.classes
    parameters = ["log10tE", "log10piE"]
    plt.close()
    figs, axes = plot_rel_prob_surfaces(
        PopulationModel=popmodel,
        parameters=parameters,
        bounds=None,
        N_bins=20,
        create_none_class=NoneClassUQ,
        none_kde=CustomKernelDensity,
        none_kde_kwargs={"kernel": "tophat", "bandwidth": 0.4},
    )

    assert len(figs) == len(classes) + 1
    assert len(axes) == len(classes) + 1
    for counter in range(len(classes) + 1):
        assert axes[counter].figure == figs[counter]
