"""
Tests to make sure model.py works
"""
from popclass.posterior import Posterior
from popclass.model import PopulationModel, validate_asdf_population_model
import numpy as np 
import pytest
import asdf

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


def test_valid_asdf_file():
    """
    Test is validator is working. 
    """

    parameters = ['log10tE', 'log10PiE', 'log10thetaE', 'f_blend_I']
    class_data = {"black_hole": np.random.randn(17, 4),
                  "neutron_star": np.random.randn(21,4),
                   "star": np.random.randn(1255,4),
                  "white dwarf": np.random.randn(178,4)}

    model_name = 'popsycle_singles_sukhboldn20'
    class_weights = {
                "black_hole": 0.011556764106050306,
                "neutron_star": 0.014276002719238613,
                "star": 0.8531611148878314,
                "white_dwarf": 0.12100611828687967
                 }

    valid_tree = {
        "class_data": class_data,
        "parameters": parameters,
        "class_weights": class_weights,
        "model_name": "popsycle_singles_imfr_sukhboldn20"
    }

    invalid_tree = {
        "class_data": class_data,
        "class_weights": class_weights,
        "model_name": "popsycle_singles_imfr_sukhboldn20"
    }

    valid_file = asdf.AsdfFile(valid_tree)
    invalid_file = asdf.AsdfFile(invalid_tree)

    assert(validate_asdf_population_model(valid_file) is True)
    assert(validate_asdf_population_model(invalid_file) is False)