from popclass.posterior import Posterior
import numpy as np 

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
    assert(post.samples == test_samples)

def test_marginal():
    """
    Test that a marginal distribution can be constructed.
    """

    test_samples = np.random.rand(3,1000)
    test_params = ['A', 'B', 'C']
    post = Posterior(samples=test_samples, parameter_labels=test_params)

    assert(post.marginal(['A']).samples == test_samples[0,:])
    assert(post.marginal(['B']).samples == test_samples[1,:])
    assert(post.marginal(['C']).samples == test_samples[2,:])


    assert(post.marginal(['A','B']).samples == test_samples[:1,:])