===============
Getting Started
===============

To demostrate basic usage of popclass we will mock some input microlensing
event data and use a pre-loaded population model to classify the lens of the
event. For a primer on microlensing see the microlensing source
`website <https://www.microlensing-source.org/>`_ .

The inputs to popclass are samples from a single event posterior distribution
and their associated prior density. Let's assume the posterior distribution is
10,000 samples from an uncorrelated gaussian in :math:`\log t_{E}- \log\pi_{E}` centered on 2, and -1, with
standard deviations of 0.1 and 0.5, respectively.

For simplicity, let's also assume that an independent uniform prior with range [-3,3]
in each parameter was used in the modeling so the prior density of each
posterior sample is identical and equal to :math:`1/6 \times 1/6 \approx 0.028`.

.. code-block:: python

    import numpy as np
    from popclass.posterior import Posterior
    from popclass.model import PopulationModel

    NUM_POSTERIOR_SAMPLES = 10000

    logtE_posterior_samples = np.random.normal(loc=2,scale=0.1, size=NUM_POSTERIOR_SAMPLES)
    logpiE_posterior_samples = np.random.normal(loc=-1,scale=0.5, size=NUM_POSTERIOR_SAMPLES)
    posterior_samples = np.dstack((logtE_posterior_samples,logpiE_posterior_samples))

    prior_density = 0.028 * np.ones(NUM_POSTERIOR_SAMPLES)

Now let's load this data into a format popclass understands.

.. code-block:: python

    posterior = Posterior(samples=posterior_samples, parameter_labels=['log10tE', 'log10piE'])
    inference_data = posterior.to_inference_data(prior_density)

Now we will load in a readily-available (or named) population model. We will choose the
`PopSyCLE <https://github.com/jluastro/PopSyCLE>`_ :cite:p:`Lam2020` population model
with the sukhbold :cite:p:`Sukhbold2016` initial final mass relation.

.. code-block:: python

    popsycle = PopulationModel.from_libaray('popsycle_singles_sukhboldn20')

We will now combine all of this information to classify the lens,
given the popsycle model and the event :math:`\log t_{E}-\log\pi_{E}` posterior.

.. code-block:: python

    classification = pc.classify(population_model=popsycle, inference_data=inference_data,
        parameters =['log10tE', 'log10piE'])
    print(classification)

classification is a dictionary of len class probabilities.

.. code-block:: console

    {"star": 0.4, "white dwarf": 0.3, "neutron star": 0.1, "black hole": 0.2}

For more advanced usage and a deeper dive into the details, please see
the documentation tutorials.
