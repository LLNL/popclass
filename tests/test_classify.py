"""
Test to check that classify.py works *as intended*
"""
import numpy as np

from popclass.classify import classify
from popclass.model import AVAILABLE_MODELS
from popclass.model import PopulationModel
from popclass.posterior import Posterior


def test_full_example():
    """
    test full getting started example
    """

    NUM_POSTERIOR_SAMPLES = 10000

    logtE_posterior_samples = np.random.normal(
        loc=2, scale=0.1, size=NUM_POSTERIOR_SAMPLES
    )
    logpiE_posterior_samples = np.random.normal(
        loc=-1, scale=0.5, size=NUM_POSTERIOR_SAMPLES
    )
    prior_density = 0.028 * np.ones(NUM_POSTERIOR_SAMPLES)
    parameters = ["log10tE", "log10piE"]

    posterior_samples = np.vstack(
        [logtE_posterior_samples, logpiE_posterior_samples]
    ).swapaxes(0, 1)
    posterior = Posterior(samples=posterior_samples, parameter_labels=parameters)
    inference_data = posterior.to_inference_data(prior_density)
    popsycle = PopulationModel.from_library("popsycle_singles_sukhboldn20")

    classification = classify(
        population_model=popsycle, inference_data=inference_data, parameters=parameters
    )

    for class_name in popsycle.classes:
        assert class_name in classification

    assert abs(1.0 - sum(classification.values())) < 0.001


def test_BH_example():
    """
    test high probability black hole

    """

    NUM_POSTERIOR_SAMPLES = 10000

    logtE_posterior_samples = np.random.normal(
        loc=2.2, scale=0.00001, size=NUM_POSTERIOR_SAMPLES
    )
    logpiE_posterior_samples = np.random.normal(
        loc=-1.8, scale=0.00001, size=NUM_POSTERIOR_SAMPLES
    )
    prior_density = 0.028 * np.ones(NUM_POSTERIOR_SAMPLES)
    parameters = ["log10tE", "log10piE"]

    posterior_samples = np.vstack(
        [logtE_posterior_samples, logpiE_posterior_samples]
    ).swapaxes(0, 1)
    posterior = Posterior(samples=posterior_samples, parameter_labels=parameters)
    inference_data = posterior.to_inference_data(prior_density)
    popsycle = PopulationModel.from_library("popsycle_singles_sukhboldn20")

    classification = classify(
        population_model=popsycle, inference_data=inference_data, parameters=parameters
    )

    print(classification)

    assert abs(1.0 - classification["black_hole"]) < 0.0001


def test_star_example():
    """
    test high probability star

    """

    NUM_POSTERIOR_SAMPLES = 10000

    logtE_posterior_samples = np.random.normal(
        loc=0.7, scale=0.00001, size=NUM_POSTERIOR_SAMPLES
    )
    logpiE_posterior_samples = np.random.normal(
        loc=-0.65, scale=0.00001, size=NUM_POSTERIOR_SAMPLES
    )
    prior_density = 0.028 * np.ones(NUM_POSTERIOR_SAMPLES)
    parameters = ["log10tE", "log10piE"]

    posterior_samples = np.vstack(
        [logtE_posterior_samples, logpiE_posterior_samples]
    ).swapaxes(0, 1)
    posterior = Posterior(samples=posterior_samples, parameter_labels=parameters)
    inference_data = posterior.to_inference_data(prior_density)
    popsycle = PopulationModel.from_library("popsycle_singles_sukhboldn20")

    classification = classify(
        population_model=popsycle, inference_data=inference_data, parameters=parameters
    )

    assert abs(1.0 - classification["star"]) < 0.0001
    assert classification["black_hole"] < 0.0001


def test_class_probs_sum_to_unity():
    """
    Test all class probabilities sum to unity for each library model.
    """

    NUM_POSTERIOR_SAMPLES = 10000

    logtE_posterior_samples = np.random.normal(
        loc=1.5, scale=0.1, size=NUM_POSTERIOR_SAMPLES
    )
    logpiE_posterior_samples = np.random.normal(
        loc=-1.0, scale=0.1, size=NUM_POSTERIOR_SAMPLES
    )
    prior_density = 0.028 * np.ones(NUM_POSTERIOR_SAMPLES)
    parameters = ["log10tE", "log10piE"]

    posterior_samples = np.vstack(
        [logtE_posterior_samples, logpiE_posterior_samples]
    ).swapaxes(0, 1)
    posterior = Posterior(samples=posterior_samples, parameter_labels=parameters)
    inference_data = posterior.to_inference_data(prior_density)

    for model_name in AVAILABLE_MODELS:
        popsycle = PopulationModel.from_library(model_name)

        classification = classify(
            population_model=popsycle,
            inference_data=inference_data,
            parameters=parameters,
        )

        assert abs(sum(classification.values()) - 1.0) < 0.00001
