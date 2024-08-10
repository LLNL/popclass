"""
Tests to make sure model.py works
"""
from popclass.posterior import Posterior
from popclass.model import PopulationModel
import numpy as np 
import pytest

def test_load_model():
    """
    Test to load a model using both classmethods.
    """
    model_name = 'popsycle_singles_sukhboldn20'
    model_from_library = PopulationModel.from_model_library(model_name=model_name)
    model_from_asdf = PopulationModel.from_asdf(path=f'popclass/data/{model_name}.asdf')

    assert(model_from_asdf == model_from_library)

def test_props():
    """
    Test that the properties of the class match expectations
    """

    test_params = ['log10tE', 'log10piE', 'log10thetaE', 'f_blend_I']
    class_list = ['black_hole', 'neutron_star', 'star', 'white_dwarf']

    model_name = 'popsycle_singles_sukhboldn20'
    model_from_library = PopulationModel.from_model_library(model_name=model_name)

    assert(list(model_from_library.classes) == class_list)
    assert(list(model_from_library.parameters) == test_params)