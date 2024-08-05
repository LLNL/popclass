"""
Utils for converting and handling posterior distributions.
"""
import numpy as np
import copy
import arviz as az

class Posterior:

    """
    Our set internal posterior object.
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
        We probably only want to classify using a slice of the full posterior in a couple of paramters

        target usage.

        marginal = Posterior.marginal(['tE', 'PiE']) should return the tE, Pi marginal posterior distribution object. 

        we also want support to take the log transform of the posterior (common use case, this might be hard to do 
        genreally.)

        """

        _, idx, _ = np.intersect1d(self.parameter_labels, parameter_list, return_indices=True)
        
        marginal = copy.deepcopy(self)
        marginal.parameter_labels = parameter_list
        marginal.samples = self.samples[idx, :]
        print(marginal.samples.shape)
        return marginal



    def paramters(self):
        """
        return ordered list of parameters
        """
        return self.parameter_labels


def convert_arviz(arviz_posterior_object) -> Posterior:
    """
    function should covert arviz posterior object to our definition of Posterior.
    """
    labels = list(arviz_posterior_object.posterior.data_vars.keys())
    samples = list(arviz_posterior_object.posterior.to_dataarray().to_numpy())
    
    return Posterior(np.array(samples).swapaxes(0,1), labels)

def convert_dynesty(dynesty_posterior_object, parameter_labels_dict) -> Posterior:
    """
    function should covert dynesty posterior object to our definition of Posterior.
    """
    labels = list(parameter_labels_dict.keys())
    samples = dynesty_posterior_object.results('samples')
    #call the function to weight the samples also (importance_weights) resample equal

    return Posterior(samples, labels)

def convert_pymulitnest(pymultinest_posterior_object) -> Posterior:
    """
    function should covert pymulitnest posterior object to our definition of Posterior.
    """
    pass