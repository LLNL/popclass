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