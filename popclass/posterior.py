"""
Utils for converting and handling posterior distributions.
"""
import numpy as np
import copy

class InferenceData:
    """
    popclass verion of an object containing the inference
    data for classification.
    """

    def __init__(self, posterior, prior_density, parameter_labels):
        """
        Initialize the InferenceData object

        Args:
            posterior (popclass.Posterior): 
                A posterior object in popclass formatting convention
            prior_density (array-like):
                
        """
        self.posterior=posterior
        self.prior_density=prior_density
        self.parameter_labels=parameter_labels


class Posterior:

    """
    popclass internal posterior object.
    """

    def __init__(self, samples, parameter_labels):
        """
        Target usage.

        post = Posterior(posterior_samples=np.array(ndim,nsamples), parameter_labels=['tE','piE', 'uO'])

        """
        testnan = np.isnan(samples)
        if True in testnan:
            raise ValueError("Posterior samples cannot be NaN")
        

        self.parameter_labels=parameter_labels
        self.samples=samples


    def marginal(self, parameter_list):
        """
        Get marginal distribution for some ordered subset of parameters in `Posterior()`

        Parameters
        ----------
        parameter_list : list
            List of parameters for generating marginal.
            Should be a subset of `Posterior.parameter_labels()`

        Returns
        -------
            New instance of `Posterior` object containing samples
            determined and ordered by `parameter_list`.
        """

        _, idx, _ = np.intersect1d(self.parameter_labels, parameter_list, return_indices=True)
        
        marginal = copy.deepcopy(self)
        marginal.parameter_labels = parameter_list
        marginal.samples = self.samples[idx, :]
        print(marginal.samples.shape)
        return marginal


    def paramters(self):
        """
        Returns
        -------
            Ordered list of parameters in `Posterior` object.
        """
        return self.parameter_labels
    
    def to_InferenceData(self, posterior_object, prior_density):
        """
        Go from Posterior object to a new InferenceData object.

        Args:
            posterior_object (popclass.Posterior)
                Either a popclass Posterior or Posterior.marginal
            prior_density (array-like)
                Prior density corresponding to samples in posterior_object

        Returns:
            An InferenceData object that contains all information needed
            to pass to classifier
        """
        inference_data = InferenceData(
            posterior=posterior_object.posterior,
            prior_density=prior_density,
            parameter_labels=posterior_object.parameter_labels
        )

        return inference_data

def convert_arviz(arviz_posterior_object) -> Posterior:
    """
    Utility to convert an ArViz posterior object directly to popclass posterior object

    Parameters
    ----------
    arviz_posterior_object : arviz.InferenceData
        InferenceData from an ArViz

    Returns
    -------
        popclass `Posterior object`
    """
    labels = list(arviz_posterior_object.posterior.data_vars.keys())
    samples = list(arviz_posterior_object.posterior.to_dataarray().to_numpy())
    
    return Posterior(np.array(samples).swapaxes(0,1), labels)

"""
The following have not been tested. May fail
"""

def convert_dynesty(dynesty_posterior_object, parameter_labels) -> Posterior:
    """
    function should convert dynesty posterior object to our definition of Posterior.
    """
    # samples = dynesty_posterior_object.results('samples')
    # weights = dynesty_posterior_object.results('logwt')
    samples = dynesty_posterior_object.sample_equal()

    return Posterior(samples, parameter_labels)

def convert_pymulitnest(pymultinest_posterior_object, parameter_labels) -> Posterior:
    """
    function should convert pymultinest posterior object to our definition of Posterior.
    """
    samples = pymultinest_posterior_object['samples']

    return Posterior(samples, parameter_labels)

