"""
Main classification utilities.
"""
from popclass.model import PopulationModel
import numpy as np


def classify(posterior, model_name, prior_density, parameters=['log10tE', 'log10piE']):
    """
    main function, takes in a posterior, population model, prior density 
    of posterior samples and returns class probabilities.
    """
    # just going to take a crack at this and get code written

    # first load in the population model
    # right now just make it from library
    population_model = PopulationModel.from_model_library(model_name=model_name)

    class_names = population_model.classes()

    prob_dict = {}

    for class_name in class_names:
        class_kde = population_model.evaluate_denisty(class_name=class_name, parameters=parameters, points=posterior)
        class_prob = np.mean(class_kde/prior_density)
        class_prob *= population_model.class_weight[class_name]
        prob_dict[class_name] = class_prob

    return prob_dict
