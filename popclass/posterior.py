"""
Utils for converting and handling posterior distributions.
"""


class Posterior:

    """
    Our set internal posterior object.
    """

    def __init__(self, samples, parameter_labels):
        """
        Target usage.

        post = Posterior(posterior_samples=np.array(ndim,nsamples), parameter_labels=['tE','piE', 'uO'])

        """
        pass


    def marginal(self, parameter_list):
        """
        We probably only want to classify using a slice of the full posterior in a couple of paramters

        target usage.

        marginal = Posterior.marginal(['tE', 'PiE']) should return the tE, Pi marginal posterior distribution object. 

        we also want support to take the log transform of the posterior (common use case, this might be hard to do 
        genreally.)

        """
        pass


    def paramters():
        """
        return ordered list of parameters
        """
        pass


def convert_arviz(arviz_posterior_object) -> Posterior:
    """
    function should covert arviz posterior object to our definition of Posterior.
    """
    pass

def convert_emcee(emcee_posterior_object) -> Posterior:
    """
    function should covert emcee posterior object to our definition of Posterior.
    """
    pass


def convert_dynesty(dynesty_posterior_object) -> Posterior:
    """
    function should covert dynesty posterior object to our definition of Posterior.
    """
    pass


def convert_pymulitnest(pymultinest_posterior_object) -> Posterior:
    """
    function should covert pymulitnest posterior object to our definition of Posterior.
    """
    pass