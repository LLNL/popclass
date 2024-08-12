"""
Main classification utilities.
"""
import numpy as np


def classify(inference_data, population_model, parameters):
    """
    main function, takes in a posterior, population model, prior density 
    of posterior samples and returns class probabilities.

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

        print(class_kde.shape)
        print(inference_data.prior_density.shape)

        raise ValueError

        class_prob = np.mean(class_kde/inference_data.prior_density)
        class_prob *= population_model.class_weight(class_name)
        prob_dict[class_name] = class_prob

    return prob_dict
