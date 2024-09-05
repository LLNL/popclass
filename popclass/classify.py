"""
Main function and usage case for ``popclass``.
Will take an ``InferenceData`` and ``PopulationModel`` object and return
object class probabilities for classes in ``PopulationModel.classes()``.

"""
import numpy as np


def classify(inference_data, population_model, parameters):
    """
    ``popclass`` classification function.
    Takes in ``popclass.InferenceData`` and ``popclass.PopulationModel`` objects,
    then returns class probabilities.

    Args:
        inference_data (popclass.InferenceData):
            popclass InferenceData object
        population_model (popclass.PopulationModel):
            popclass PopulationModel object
        parameters (list):
            Parameters to use for classification.

    Returns:
        Dictionary of classes in ``PopulationModel.classes()`` and associated
        probability.
    """
    class_names = population_model.classes
    posterior = inference_data.posterior.marginal(parameters)
    posterior_samples = posterior.samples

    unnormalized_prob = {}
    for class_name in class_names:
        class_kde = population_model.evaluate_density(
            class_name=class_name,
            parameters=posterior.parameter_labels,
            points=posterior_samples,
        )
        integrated_posterior = np.mean(class_kde / inference_data.prior_density)
        weighted_integrated_posterior = (
            integrated_posterior * population_model.class_weight(class_name)
        )
        unnormalized_prob[class_name] = weighted_integrated_posterior

    normalization = sum(unnormalized_prob.values())
    class_prob = {
        class_name: float(value / normalization)
        for class_name, value in unnormalized_prob.items()
    }
    return class_prob
