"""
Tests to make sure model.py works
"""
import fnmatch
import os

import asdf
import numpy as np
import pytest
from scipy.stats import norm

from popclass.model import AVAILABLE_MODELS
from popclass.model import PopulationModel
from popclass.model import validate_asdf_population_model
from popclass.posterior import Posterior


def test_model_saving():
    """
    Test for saving a population model to an ASDF file.

    Writes a temporary asdf file to the tests directory and tests to makes sure the saved file is valid.
    """
    population_samples_raw = norm.rvs(size=int(2e2), loc=0, scale=1).reshape((100, 2))
    class_names = ["a", "b"]
    population_samples = {key: population_samples_raw for key in class_names}
    class_weights = [0.5, 0.5]
    parameters = ["1", "2"]
    test_model = PopulationModel(
        population_samples=population_samples,
        class_weights=class_weights,
        parameters=parameters,
    )
    output_fp = os.path.dirname(os.path.realpath(__file__)) + "/tmp.asdf"
    test_model.to_asdf(output_fp, "tmp")

    with asdf.open(output_fp, lazy_load=False, copy_arrays=True) as tree:
        assert validate_asdf_population_model(tree)

    os.remove(output_fp)


def test_model_library_supported_options():
    """Test to ensure there is consistency between the models packaged with popclass
    match the options enumerated in the software in models.py
    """
    data_dir = os.path.dirname(os.path.realpath(__file__)) + "/../popclass/data/"
    model_data_tags = []
    for file in os.listdir(data_dir):
        if fnmatch.fnmatch(file, "*.asdf"):
            model_data_tags.append(file[:-5])
    AVAILABLE_MODELS_sorted = AVAILABLE_MODELS.sort()
    model_data_tags_sorted = model_data_tags.sort()
    assert len(AVAILABLE_MODELS) == len(model_data_tags)
    assert np.all(AVAILABLE_MODELS_sorted == model_data_tags_sorted)


def test_load_model():
    """
    Test to load a model using both classmethods.
    """
    model_name = "popsycle_singles_sukhboldn20"
    path = "popclass/data/"

    model_from_library = PopulationModel.from_library(
        model_name=model_name, library_path=path
    )
    model_from_asdf = PopulationModel.from_asdf(path=f"popclass/data/{model_name}.asdf")

    assert model_from_asdf.classes == model_from_library.classes
    assert model_from_asdf.parameters == model_from_library.parameters

    parameters = model_from_asdf.parameters

    for class_name in model_from_asdf.classes:
        assert np.allclose(
            model_from_asdf.samples(class_name, parameters),
            model_from_library.samples(class_name, parameters),
        )


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
    models = [
        "popsycle_singles_sukhboldn20",
        "popsycle_singles_spera15",
        "popsycle_singles_raithel18",
    ]

    test_params = ["log10tE", "log10piE", "log10thetaE", "f_blend_I"]
    class_list = ["black_hole", "neutron_star", "star", "white_dwarf"]

    for model in models:
        model_from_library = PopulationModel.from_library(model_name=model)
        assert list(model_from_library.classes) == class_list
        assert list(model_from_library.parameters) == test_params


def test_valid_asdf_file():
    """
    Test is validator is working.
    """

    parameters = ["log10tE", "log10PiE", "log10thetaE", "f_blend_I"]
    class_data = {
        "black_hole": np.random.randn(17, 4),
        "neutron_star": np.random.randn(21, 4),
        "star": np.random.randn(1255, 4),
        "white dwarf": np.random.randn(178, 4),
    }

    model_name = "popsycle_singles_sukhboldn20"
    class_weights = {
        "black_hole": 0.011556764106050306,
        "neutron_star": 0.014276002719238613,
        "star": 0.8531611148878314,
        "white_dwarf": 0.12100611828687967,
    }

    valid_tree = {
        "class_data": class_data,
        "parameters": parameters,
        "class_weights": class_weights,
        "model_name": "popsycle_singles_sukhboldn20",
    }

    invalid_tree = {
        "class_data": class_data,
        "class_weights": class_weights,
        "model_name": "popsycle_singles_sukhboldn20",
    }

    valid_file = asdf.AsdfFile(valid_tree)
    invalid_file = asdf.AsdfFile(invalid_tree)

    assert validate_asdf_population_model(valid_file) is True
    assert validate_asdf_population_model(invalid_file) is False


def test_all_population_model_files_are_valid():
    """
    Test all library population model files are valid
    """
    for model in AVAILABLE_MODELS:
        print(model)
        with asdf.open(f"popclass/data/{model}.asdf") as tree:
            print(tree)
            assert validate_asdf_population_model(tree) is True


def test_model_name_match():
    """
    Be sure that the model name in both the filepath and metadata match
    """
    for model in AVAILABLE_MODELS:
        print(model)
        with asdf.open(f"popclass/data/{model}.asdf") as f:
            assert f["model_name"] == model


def test_evaluate_transpose():
    """Testing whether changing the order of the data/parameters/classes and the order of the density evaluation changes the value of the PDF, as it should not."""
    # Configuration 1
    classes = ["A", "B", "C"]
    class_vals = {"A": np.array([2, 3]), "B": np.array([4, 5]), "C": np.array([6, 7])}

    population_samples = {
        key: norm.rvs(size=20, loc=0, scale=1).reshape((10, 2)) * class_vals[key]
        for key in classes
    }
    class_weights = {key: 1.0 / 3.0 for key in classes}
    parameters = ["parameter_1", "parameter_2"]
    model1 = PopulationModel(
        population_samples=population_samples,
        class_weights=class_weights,
        parameters=parameters,
    )

    # Configuration 2 - permutate classes by 1 and flip the parameters
    classes2 = [classes[i] for i in [1, 2, 0]]
    parameters2 = [parameters[i] for i in [1, 0]]
    population_samples2 = {key: population_samples[key][:, [1, 0]] for key in classes2}
    class_weights2 = {key: 1.0 / 3.0 for key in classes2}
    model2 = PopulationModel(
        population_samples=population_samples2,
        class_weights=class_weights2,
        parameters=parameters2,
    )

    # Check all classes and pairs of parameters
    for key in classes:
        assert model1.evaluate_density(
            key, parameters, np.array([[2, 0]])
        ) == model2.evaluate_density(key, parameters, np.array([[2, 0]]))
        flipped = list([parameters[1], parameters[0]])
        assert round(
            model1.evaluate_density(key, flipped, np.array([[0, 2]]))[0], 10
        ) == round(model2.evaluate_density(key, parameters, np.array([[2, 0]]))[0], 10)

    # Check all classes and single parameters
    for key in classes:
        for parameter in parameters:
            assert model1.evaluate_density(
                key, parameter, np.array([[2]])
            ) == model2.evaluate_density(key, parameter, np.array([[2]]))
