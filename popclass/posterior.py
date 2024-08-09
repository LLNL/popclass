"""
Utils for converting and handling posterior distributions.
"""
import numpy as np
import copy

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
    function should covert dynesty posterior object to our definition of Posterior.
    """
    # samples = dynesty_posterior_object.results('samples')
    # weights = dynesty_posterior_object.results('logwt')
    samples = dynesty_posterior_object.sample_equal()

    return Posterior(samples, parameter_labels)

def convert_pymulitnest(pymultinest_posterior_object, parameter_labels) -> Posterior:
    """
    function should covert pymulitnest posterior object to our definition of Posterior.
    """
    samples = pymultinest_posterior_object['samples']

    return Posterior(samples, parameter_labels)