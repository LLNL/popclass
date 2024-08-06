"""
Reading, saving, and  handling population models 
"""
import asdf
import numpy as np


class PopulationModel:
    """
    Holds population model data
    """

    def __init__(self, population_samples, weights, density_estimator):
        self._weights = weights
        self._population_samples = population_samples
        self._density_estimator = density_estimator

    @classmethod
    def from_asdf(cls, path, class_names):
        
        pass

    def samples(self, class_name):
        return self._population_samples[class_name]

    @property
    def classes():
        return self._population_samples.keys()


    def weight(self, class_name):
        return self._weights


    def evaluate_denisty(class_name, point):
        pass

