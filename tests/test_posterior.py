from popclass.posterior import Posterior
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
    assert(post.parameter_labels == test_params)

def test_posterior_init_samples():
    """
    Test that posterior parameter samples are initialized correctly.
    """

    test_samples = np.random.rand(3,1000)
    test_params = ['A', 'B', 'C']
    post = Posterior(samples=test_samples, parameter_labels=test_params)
    assert(np.array_equal(post.samples, test_samples))

def test_marginal():
    """
    Test that a marginal distribution can be constructed.
    """

    test_samples = np.random.rand(3,1000)
    test_params = ['A', 'B', 'C']
    post = Posterior(samples=test_samples, parameter_labels=test_params)

    #print(post.marginal(['A']).samples, test_samples[0,:])

    assert(np.allclose(post.marginal(['A']).samples, test_samples[0,:]))
    assert(np.allclose(post.marginal(['B']).samples, test_samples[1,:]))
    assert(np.allclose(post.marginal(['C']).samples, test_samples[2,:]))

    assert(np.allclose(post.marginal(['A','B']).samples, test_samples[:2,:]))

def test_nan_in_samples_exception():
    """
    Test that there is a check for NaNs in posterior samples when Posterior is constructed
    """

    with pytest.raises(ValueError):
        test_samples = np.random.rand(3,1000)
        test_samples[0,1] = np.nan
        test_params = ['A', 'B', 'C']
        post = Posterior(samples=test_samples, parameter_labels=test_params)
