"""
Utilities for creating the posterior and inference data objects for interfacing
with ``popclass``' classification function.
"""
import copy

import numpy as np


class InferenceData:
    """
    ``popclass`` version of an object containing the inference
    data for classification, including posterior samples and prior density.

    Similar to ``popclass.Posterior``, but is intended to include prior information
    to be passed to the classifier.
    """

    def __init__(self, posterior, prior_density):
        """
        Initialize the InferenceData object.

        Args:
            posterior (popclass.Posterior):
                A posterior object in popclass formatting convention, containing posterior
                samples of the shape (number of samples, number of parameters)
            prior_density (array-like):
                1D array representing the prior density with an expected shape of (number of samples,)
        """
        self.posterior = posterior
        self.prior_density = prior_density


class Posterior:
    """
    ``popclass`` object containing the user's posterior information.
    This object can either be initialized from data arrays, or come from outside libraries in a
    compatible format. Acceptable formats from outside sources are listed below.

    **Supported Formats**:

    * ArViz
    * BAGLE (Microlensing specific, see below)
    """

    def __init__(self, samples, parameter_labels):
        """
        Initialize posterior object.

        Args:
            samples (array-like):
                Posterior samples with a shape of (number of samples, number of parameters).
                Rows correspond to individual samples drawn from the posterior distribution,
                and columns correspond to specific parameters.
            parameter_labels (list[str]):
                List of strings representing the labels of the parameters.
                There should be an equal number of labels to columns in samples representing
                individual parameters (i.e. the number of parameters).

        Raises:
            ValueError: if the number of parameters is not less than the number of samples.
        """
        testnan = np.isnan(samples)
        if True in testnan:
            raise ValueError("Posterior samples cannot be NaN")

        # Check that number of samples > number of parameters
        if samples.shape[0] <= samples.shape[1]:
            raise ValueError(
                "Number of samples must be greater than number of parameters!"
            )

        self.parameter_labels = parameter_labels
        self.samples = samples

    def marginal(self, parameter_list):
        """
        Get marginal distribution for some ordered subset of parameters in ``Posterior``

        Args:
            parameter_list (list[str]):
                List of parameters for generating a marginal distribution.
                Should be a subset of ``Posterior.parameter_labels()``.

        Returns:
            New instance of the ``Posterior`` object only containing
            samples determined and ordered by `parameter_list`.

        Raises:
            ValueError: if the number of parameters is not less than the number of samples.
        """

        _1, id_arr_labels, id_arr_list = np.intersect1d(
            self.parameter_labels, parameter_list, return_indices=True
        )
        marginal = copy.deepcopy(self)
        marginal.parameter_labels = list([parameter_list[i] for i in id_arr_list])
        marginal.samples = self.samples[:, id_arr_labels]

        # Shape check
        if marginal.samples.shape[0] <= marginal.samples.shape[1]:
            raise ValueError(
                "Number of samples in marginal array must be greater than number of parameters!"
            )

        return marginal

    @property
    def parameters(self):
        """
        Defines an ordered list of parameters for the ``Posterior`` object.

        Returns:
            parameters (list [str]):
                Ordered list of parameters in the ``Posterior`` object.
        """
        return self.parameter_labels

    def to_inference_data(self, prior_density):
        """
        Go from the ``Posterior`` object to a new ``InferenceData`` object.

        Args:
            posterior_object (popclass.Posterior):
                Either a popclass ``Posterior`` or ``Posterior.marginal() `` object.
            prior_density (array-like):
                1D array representing the prior density with an expected shape of (number of samples,).
                Prior density corresponds to samples in posterior_object, as the number of entries must
                match the number of rows in the posterior samples array.

        Returns:
            popclass.InferenceData:
                An ``InferenceData`` object that contains all the information needed
                to pass to a classifier.
        """
        return InferenceData(posterior=self, prior_density=prior_density)

    @classmethod
    def from_arviz(cls, arviz_posterior_object):
        """
        Utility to convert an ArViz posterior object directly to popclass posterior object.

        Args:
            arviz_posterior_object (arviz.InferenceData):
                InferenceData from an ArViz run.

        Returns:
            popclass.Posterior:
                A ``popclass.Posterior`` object generated from the ArViz posterior.

        Raises:
            ValueError: if the number of parameters is not less than the number of samples.
        """
        labels = list(arviz_posterior_object.posterior.data_vars.keys())
        samples = arviz_posterior_object.posterior.to_dataarray().to_numpy().squeeze()

        samples_array = np.array(samples).swapaxes(0, 1)
        # Shape check
        if samples_array.shape[0] <= samples_array.shape[1]:
            raise ValueError(
                "Number of samples in arviz array must be greater than number of parameters!"
            )

        return cls(samples_array, labels)

    @classmethod
    def from_pymultinest(cls, pymultinest_analyzer_object, parameter_labels):
        """
        Utility to convert a PyMultiNest posterior to a popclass posterior object.

        Args:
            pymultinest_analyzer_object:
                Analyzer object from PyMultiNest
            parameter_labels (list[str]):
                Ordered list of parameters. Should correspond to the order of
                parameters in ``pymultinest_analyzer_object``.

        Returns:
            popclass.Posterior:
                A ``Posterior`` object with samples from the PyMultiNest analysis.

        Raises:
            ValueError: if the number of parameters is not less than the number of samples.
        """
        samples = pymultinest_analyzer_object.get_equal_weighted_posterior()

        # Shape check
        if samples.shape[0] <= samples.shape[1]:
            raise ValueError(
                "Number of samples in pymultinest array must be greater than number of parameters!"
            )

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
