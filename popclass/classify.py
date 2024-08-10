"""
Main classification utilities.
"""
import numpy as np



def classify(inference_data, population_model, parameters=['log10tE', 'log10piE']):
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
    # just going to take a crack at this and get code written

    # first load in the population model
    # right now just make it from library
    class_names = population_model.classes()

    prob_dict = {}

    for class_name in class_names:
        class_kde = population_model.evaluate_denisty(
            class_name=class_name, 
            parameters=parameters, 
            points=inference_data.posterior
        )
        class_prob = np.mean(class_kde/inference_data.prior_density)
        class_prob *= population_model.class_weight[class_name]
        prob_dict[class_name] = class_prob

    return prob_dict
