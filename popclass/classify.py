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
    """
    class_names = population_model.classes
    posterior = inference_data.posterior.marginal(parameters)
    posterior_samples = posterior.samples

    prob_dict = {}

    for class_name in class_names:
        class_kde = population_model.evaluate_denisty(
            class_name=class_name, 
            parameters=parameters, 
            points=posterior_samples
        )
        class_prob = np.mean(class_kde/inference_data.prior_density)
        class_prob *= population_model.class_weight(class_name)
        prob_dict[class_name] = class_prob

    return prob_dict
