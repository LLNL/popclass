from popclass.posterior import Posterior
from dynesty.results import Results
import numpy as np 
import pytest
import arviz as az


def test_posterior_init_parameters():
    """
    Test that posterior parameter labels are initialized correctly.
    """

    test_samples = np.random.rand(3,1000)
    test_params = ['A', 'B', 'C']
    post = Posterior(samples=test_samples, parameter_labels=test_params)
    assert(post.parameters == test_params)

def test_posterior_init_samples():
    """
    Test that posterior parameter samples are initialized correctly.
    """

    test_samples = np.random.rand(1000,3)
    test_params = ['A', 'B', 'C']
    post = Posterior(samples=test_samples, parameter_labels=test_params)
    assert(np.array_equal(post.samples, test_samples))

def test_marginal():
    """
    Test that a marginal distribution can be constructed.
    """

    test_samples = np.random.rand(1000,3)
    test_params = ['A', 'B', 'C']
    post = Posterior(samples=test_samples, parameter_labels=test_params)

    assert(np.allclose(post.marginal(['A']).samples, test_samples[:,0].reshape(1000,1)))
    assert(np.allclose(post.marginal(['B']).samples, test_samples[:,1].reshape(1000,1)))
    assert(np.allclose(post.marginal(['C']).samples, test_samples[:,2].reshape(1000,1)))
    assert(np.allclose(post.marginal(['A','B']).samples, test_samples[:,[0,1]]))

def test_nan_in_samples_exception():
    """
    Test that there is a check for NaNs in posterior samples when Posterior is constructed
    """

    with pytest.raises(ValueError):
        test_samples = np.random.rand(3,1000)
        test_samples[0,1] = np.nan
        test_params = ['A', 'B', 'C']
        post = Posterior(samples=test_samples, parameter_labels=test_params)

def test_convert_arviz():
    """
    Test that conversion from Arviz works.
    """
    test_samples = np.random.rand(3,1000)
    test_params = ['A', 'B', 'C']

    post =  {
        test_params[0]: test_samples[0, :],
        test_params[1]: test_samples[1, :],
        test_params[2]: test_samples[2, :]
    }

    az_post = az.convert_to_inference_data(post)
    popclass_from_az_post = Posterior.from_arviz(az_post)

    assert(np.allclose(test_samples, popclass_from_az_post.samples))

def test_to_InferenceData():
    """
    Test that creating an InferenceData object from Posterior works
    """
    test_samples = np.random.rand(1000,3)
    test_params = ['A', 'B', 'C']
    test_prior = np.ones(len(test_samples[0]))
    post = Posterior(samples=test_samples, parameter_labels=test_params)

    inference_data = post.to_inference_data(test_prior)

    assert(np.array_equal(inference_data.posterior.samples, test_samples))
    assert(np.array_equal(inference_data.posterior.parameter_labels, test_params))
    assert(np.array_equal(inference_data.prior_density, test_prior))


#def test_convert_dynesty():
#    """
#    Test that conversion from dynesty works
#    """
#    test_samples = np.random.rand(3,1000)
#    test_params_dict = {'A': 1, 'B': 2, 'C': 3}

#    dynesty_post = Results([('samples_id', list(test_params_dict.values())), ('samples',test_samples)])
    
#    popclass_from_dynesty_post = convert_dynesty(dynesty_post, test_params_dict)

#    assert(np.allclose(popclass_from_dynesty_post.samples, test_samples))