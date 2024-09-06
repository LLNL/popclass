"""
Utilities for creating the posterior and inference data objects for interfacing
with ``popclass``' classification function.
"""
import copy

import numpy as np


class InferenceData:
    """
    ``popclass`` verion of an object containing the inference
    data for classification.

    Similar to ``popclass.Posterior``, but is intended to include prior infrmation
    to be passed to the classifier.
    """

    def __init__(self, posterior, prior_density):
        """
        Initialize the InferenceData object

        Args:
            posterior (popclass.Posterior):
                A posterior object in popclass formatting convention
            prior_density (array-like):

        """
        self.posterior = posterior
        self.prior_density = prior_density


class Posterior:
    """
    ``popclass`` object containing the user's posterior information.
    This can be either from data arrays or an allowable format.

    **Supported Formats**:

    * ArViz
    * BAGLE (Microlensing specific, see below)
    """

    def __init__(self, samples, parameter_labels):
        """
        Initialize posterior object.

        Args:
            samples (array-like):
                Posterior samples
            parameter_labels (list[str]):
                Labels of the paramater labels corresponding to
                posterior samples.

        """
        testnan = np.isnan(samples)
        if True in testnan:
            raise ValueError("Posterior samples cannot be NaN")

        self.parameter_labels = parameter_labels
        self.samples = samples

    def marginal(self, parameter_list):
        """
        Get marginal distribution for some ordered subset of parameters in ``Posterior``

        Args:
            parameter_list (list[str]):
                List of parameters for generating marginal.
                Should be a subset of ``Posterior.parameter_labels()``

        Returns:
            New instance of ``Posterior`` object containing samples
            determined and ordered by `parameter_list`.
        """

        _1, id_arr_labels, id_arr_list = np.intersect1d(
            self.parameter_labels, parameter_list, return_indices=True
        )
        marginal = copy.deepcopy(self)
        marginal.parameter_labels = list([parameter_list[i] for i in id_arr_list])
        marginal.samples = self.samples[:, id_arr_labels]

        return marginal

    @property
    def parameters(self):
        """
        Returns:
            paramaters (list [str]):
                Ordered list of parameters in ``Posterior`` object.
        """
        return self.parameter_labels

    def to_inference_data(self, prior_density):
        """
        Go from ``Posterior`` object to a new ``InferenceData`` object.

        Args:
            posterior_object (popclass.Posterior)
                Either a popclass ``Posterior`` or ``Posterior.marginal()``
            prior_density (array-like)
                Prior density corresponding to samples in posterior_object

        Returns:
            An ``InferenceData`` object that contains all information needed
            to pass to classifier
        """
        return InferenceData(posterior=self, prior_density=prior_density)

    @classmethod
    def from_arviz(cls, arviz_posterior_object):
        """
        Utility to convert an ArViz posterior object directly to popclass posterior object

        Args:
            arviz_posterior_object (arviz.InferenceData):
                InferenceData from an ArViz run

        Returns:
            ``popclass.Posterior`` object
        """
        labels = list(arviz_posterior_object.posterior.data_vars.keys())
        samples = list(arviz_posterior_object.posterior.to_dataarray().to_numpy())
        return cls(np.array(samples).swapaxes(0, 1), labels)

    @classmethod
    def from_pymultinest(cls, pymultinest_analyzer_object, parameter_labels):
        """
        Utility to convert a PyMultiNest posterior to a popclass posterior

        Args:
            pymultinest_analyzer_object:
                Analyzer object from PyMultiNest
            parameter_labels:
                ordered list of parameters. Should correspond to the order of
                parameterss in ``pymultinest_analyzer_object``

        Returns:
            ``popclass.Posterior`` object
        """
        samples = pymultinest_analyzer_object.get_equal_weighted_posterior()

        return Posterior(samples, parameter_labels)


# def convert_dynesty(dynesty_posterior_object, parameter_labels) -> Posterior:
#    """
#    function should convert dynesty posterior object to our definition of Posterior.
#    """
#    # samples = dynesty_posterior_object.results('samples')
#    # weights = dynesty_posterior_object.results('logwt')
#    samples = dynesty_posterior_object.sample_equal()
#
#    return Posterior(samples, parameter_labels)
