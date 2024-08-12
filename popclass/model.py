"""
In order to make object classification probabilities, 
we must define a galactic model.
``popclass`` allows the user to either specify one of the models included with
the library or supply their own, given that it is in ASDF file format.
"""
import asdf
import numpy as np
from scipy.stats import gaussian_kde

AVAILABLE_MODELS = [
    "popsycle_singles_raithel18", 
    "popsycle_singles_spera15",
    "popsycle_singles_sukhboldn20"
    ]

class PopulationModel:
    """
    Used to store information on simulation data necessary for classification.
    """

    def __init__(self, population_samples, class_weights, parameters, density_estimator=gaussian_kde):
        """
        Initialize PopulationModel.

        Args:
            population_samples (dict):
                key is a class name and value is numpy array of parameter
                samples with shape (n_samples, n_parameters).
            class_weights (dict):
                key is a class name and value is a number between [0,1].
            parameters (list(str)):
                list of parameter names sets the order for the second dimension
                in population_samples.
            density_estimator: (scipy.stats.gaussian_kde like):
                Kernel density estimator used to compute density from
                population data. 
        """

        self._class_weights = class_weights
        self._population_samples = population_samples
        self._density_estimator = density_estimator
        self._parameters = parameters

    @classmethod
    def from_asdf(cls, path):
        """
        Build population model from data in an asdf file

        Args:
            path (str): path to the asdf file

        Returns:
            PopulationModel populated with the data from the asdf file.
        """

        with asdf.open(path, lazy_load=False, copy_arrays=True) as tree:
            population_samples=tree['class_data'] 
            parameters=tree['parameters']
            class_weights=tree['class_weights']
    
        return cls(population_samples=population_samples, 
                    parameters=parameters,
                    class_weights=class_weights)

    @classmethod
    def from_library(cls, model_name, library_path=None):
        """
        Build population model from available models.

        Available models include

        * ``popsycle_singles_raithel18``
        * ``popsycle_singles_spera15``
        * ``popsycle_singles_sukhboldn20``

        Args:
            model_name (str): Name of the model.
            library_path (str): Path to library of models.
        
        Returns:
            PopulationModel from library of avaible models.
        """

        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"{model_name} not available. Available models are: {AVAILABLE_MODELS}")
        path = "popclass/data/" if library_path is None else library_path

        return cls.from_asdf(f'{path}{model_name}.asdf')
    
    def samples(self, class_name, parameters):
        """
        Return simulation samples for a given class and given list of parameters.

        Args:
            class_name: (str): 
                name of class to get population samples for.
            parameters: (list[str]): 
                List of parameters to get samples for.
        
        Returns:
            samples of shape (`num_samples, len(parameters)`) with
            the order of the second dimension being set by the order of parameters.
        """
        _, indicies, _ = np.intersect1d(self.parameters, parameters, return_indices=True)
        return self._population_samples[class_name][:, indicies]

    @property
    def parameters(self):
        """
        Return all parameters available in the population model.

        Returns:
            List of all parameters.
        """
        return self._parameters

    @property
    def classes(self):
        """
        Return all classes available in the population model.

        Returns:
            List of all classes available.
        """

        return list(self._population_samples.keys())


    def class_weight(self, class_name):
        """
        Return the class weight for a given class.

        Returns:
            Class Weight for the specified class.
        """
        return self._class_weights[class_name]


    def evaluate_denisty(self, class_name, parameters, points):
        """
        Evaulate the kernal density estimate of a point
        for a class.

        Args:
            class_name (str): 
                name of class to evaluate density.
            parameters (list[str]): 
                parameters to evaluate
                population model density over. Order sets the order
                of the second dimension of points.
            points (np.ndarray): 
                data to evalute desnity on has shape
                (num_data_points, len(parameters)).
        Returns:
            density_evaluation (np.ndarray)
        """
        class_samples = self.samples(class_name, parameters)
        kernal = self._density_estimator(class_samples.T)
        return kernal.evaluate(points[0,:,:].T.shape)


    def to_asdf(self, path, model_name):
        """
        Save population model to asdf file.

        Args:
            path (str): path to save the asdf file
            model_name (str): Name of the model to be saving in the asdf file. 
        """
        tree = {
            "class_data": self._population_samples,
            "parameters": self._parameters,
            "class_weights": self._class_weights,
            "model_name": model_name,
        }
        af = asdf.AsdfFile(tree)
        af.write_to(path)


def validate_asdf_population_model(asdf_object):
    """
    Chack if PopulationModel asdf file is valid.

    Args:
        asdf_object (asdf): asdf file to validate against a
            Population model required format.
    
    Returns:
        True if asdf is valid. False otherwise.
    """
    valid_key_set = ['model_name', 'class_weights', 'parameters', 'class_data']
    keys_present = [name in asdf_object for name in valid_key_set]
    return all(keys_present)
    
    



