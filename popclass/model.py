"""
In order to make object classification probabilities,
we must define a galactic model.
``popclass`` allows the user to either specify one of the models included with
the library or supply their own, given that it is in ASDF file format.
"""
import asdf
import numpy as np
import pkg_resources
from scipy.stats import gaussian_kde
from scipy.stats import multivariate_normal
from sklearn.neighbors import KernelDensity

AVAILABLE_MODELS = [
    "popsycle_singles_raithel18",
    "popsycle_singles_spera15",
    "popsycle_singles_sukhboldn20",
]


class PopulationModel:
    """
    Used to store information on simulation data necessary for classification.
    """

    def __init__(
        self,
        population_samples,
        class_weights,
        parameters,
        citation=None,
        density_estimator=gaussian_kde,
        density_kwargs={},
    ):
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
            citation (list):
                list of DOI entries for citing the model.
            density_estimator: (scipy.stats.gaussian_kde like):
                Kernel density estimator used to compute density from
                population data.
        """

        self._class_weights = class_weights
        self._population_samples = population_samples
        self._density_estimator = density_estimator
        self._density_kwargs = density_kwargs
        self._parameters = parameters
        self._citation = citation

    @classmethod
    def from_asdf(cls, path):
        """
        Build population model from data in an asdf file.
        This file can be user-generated, but must adhere to the schema
        of the files included in the library.

        Args:
            path (str): path to the asdf file

        Returns:
            PopulationModel populated with the data from the asdf file.
        """

        with asdf.open(path, lazy_load=False) as tree:
            population_samples = tree["class_data"]
            parameters = tree["parameters"]
            class_weights = tree["class_weights"]
            citation = tree["citation"]

        return cls(
            population_samples=population_samples,
            parameters=parameters,
            class_weights=class_weights,
            citation=citation,
        )

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
            PopulationModel from library of avaible models.t
        """

        if model_name not in AVAILABLE_MODELS:
            raise ValueError(
                f"{model_name} not available. Available models are: {AVAILABLE_MODELS}"
            )

        stream = pkg_resources.resource_stream(__name__, f"data/{model_name}.asdf")
        path = stream if library_path is None else f"{library_path}{model_name}.asdf"

        return cls.from_asdf(path)

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
        params_sorted, indices, _ = np.intersect1d(
            self.parameters, parameters, return_indices=True
        )
        samples_sorted = self._population_samples[class_name][:, indices]
        order = np.array(parameters).argsort().argsort()
        return samples_sorted[:, order]

    @property
    def parameters(self):
        """
        Return all parameters available in the population model.

        Returns:
            List of all parameters.
        """
        return self._parameters

    @property
    def citation(self):
        """
        Return the citation of the population model.

        Returns:
            List of DOI entries corresponding to cite the model.
        """
        return self._citation

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

    def evaluate_density(self, class_name, parameters, points):
        """
        Evaluate the kernel density estimate of a point
        for a class.

        Args:
            class_name (str):
                name of class to evaluate density.
            parameters (list[str]):
                parameters to evaluate
                population model density over. Order sets the order
                of the second dimension of points.
            points (np.ndarray):
                data to evalute density on. Has shape
                (num_data_points, len(parameters)).
        Returns:
            density_evaluation (np.ndarray)
        """
        class_samples = self.samples(class_name, parameters).swapaxes(0, 1)
        kernel = self._density_estimator(class_samples, **self._density_kwargs)
        return kernel.evaluate(points.swapaxes(0, 1))

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
            "citation": self._citation,
        }
        af = asdf.AsdfFile(tree)
        af.write_to(path)


class MultivariateGaussianKernel:
    """An example of defining a custom kernel for a PopulationModel. Wraps scipy.stats.multivariate_normal to conform to the template needed by PopulationModel and classify."""

    def __init__(self, data):
        """Initialization.

        Args:
            data (numpy.array): shape [# dims, # samples]. Same as scipy.stats.gaussian_kde
        Returns:
            None
        """
        self.mean = np.mean(data, axis=1)
        self.cov = np.cov(data)

    def evaluate(self, pts):
        """Evaluation method for calculating the pdf of the kernel at a set of points.

        Args:
            pts (numpy.array): array of points to evaluate the density on. Shape: [# dimensions, # of points].
        Returns:
            evaluated_density (numpy.array): the probability density values at each of the corresponding points.
        """
        return multivariate_normal.pdf(pts.T, mean=self.mean, cov=self.cov)


def validate_asdf_population_model(asdf_object):
    """
    Check if PopulationModel asdf file is valid.

    Args:
        asdf_object (asdf): asdf file to validate against a
            Population model required format.

    Returns:
        True if asdf is valid. False otherwise.
    """
    valid_key_set = [
        "model_name",
        "class_weights",
        "parameters",
        "class_data",
        "citation",
    ]
    keys_present = [name in asdf_object for name in valid_key_set]

    if all(keys_present):
        number_of_classes = len(asdf_object["class_data"])
        number_of_parameters = len(asdf_object["parameters"])
        # valid_class_data = [isinstance(data, np.ndarray) for data in asdf_object['class_data'].values()]
        valid_class_data_dim = [
            data.shape[1] == number_of_parameters
            for data in asdf_object["class_data"].values()
        ]

        # Validating the citation field
        citation = asdf_object["citation"]
        valid_citation = isinstance(citation, list) and all(
            isinstance(doi, str) for doi in citation
        )

        valid = all(valid_class_data_dim) and valid_citation
    else:
        valid = False
    return valid


class CustomKernelDensity:
    """An example of defining a custom kernel for a PopulationModel. Wraps sklearn.neighbors.KernelDensity to conform to the template needed by PopulationModel and classify."""

    def __init__(self, data, **kwargs):
        """Initialization.
        Args:
            data (numpy.array): shape [# dims, # samples]. Same as scipy.stats.gaussian_kde
            kernel_type (str): matches 'kernel' argument of KernelDensity. Default: "tophat".
            bandwidth (float): matches 'bandwidth' argument of KernelDensity. Default: 0.4.
        Returns:
            None
        """
        self.data = data
        self.density_kwargs = kwargs

    def evaluate(self, pts):
        """Evaluation method for calculating the pdf of the kernel at a set of points.

        Args:
            pts (numpy.array): array of points to evaluate the density on. Shape: [# dimensions, # of points].
        Returns:
            evaluated_density (numpy.array): the probability density values at each of the corresponding points.
        """
        kernel = KernelDensity(**self.density_kwargs).fit(self.data.T)
        return np.exp(kernel.score_samples(pts.T))
