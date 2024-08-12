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
    path='popclass/data/'

    model_from_library = PopulationModel.from_library(model_name=model_name,library_path=path)
    model_from_asdf = PopulationModel.from_asdf(path=f'popclass/data/{model_name}.asdf')

    assert(model_from_asdf.classes == model_from_library.classes)
    assert(model_from_asdf.parameters == model_from_library.parameters)

    parameters = model_from_asdf.parameters

    for class_name in model_from_asdf.classes:
        assert(np.allclose(model_from_asdf.samples(class_name,parameters),
        model_from_library.samples(class_name,parameters)))


def test_load_model_not_in_libaray():
    """
    Test model not in library raise value error 
    """
    with pytest.raises(ValueError):
        model_from_library = PopulationModel.from_library(model_name="model_not_there")


def test_props():
    """
    Test that the properties of the class match expectations
    """
    models = ['popsycle_singles_sukhboldn20','popsycle_singles_spera15',
             'popsycle_singles_raithel18']

    test_params = ['log10tE', 'log10piE', 'log10thetaE', 'f_blend_I']
    class_list = ['black_hole', 'neutron_star', 'star', 'white_dwarf']

    for model in models:
        model_from_library = PopulationModel.from_library(model_name=model)
        assert(list(model_from_library.classes) == class_list)
        assert(list(model_from_library.parameters) == test_params)