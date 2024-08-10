==========
Background
==========

Here we will briefly cover the mathematics underpinning popclass. For a detailed theoretical 
background on the methods please see :cite:t:`Perkins2024`. 

Consider the data from a single microlensing event light curve :math:`\boldsymbol{d}`,
using a model of the Galaxy :math:`\mathcal{G}`, popclass calculates the probability
that the lens of the events belongs to each lens class, :math:`\text{class}_L`, where
:math:`\text{class}_L\in\text{classes}` and 
:math:`\text{classes} = \{\text{Star, Neutron Star, White Dwarf, Black Hole}\}`. Namely,
popclass calulates,

.. math::

    p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) \text{ for } \text{class}_L\in\text{classes}.

Using Bayes' theorem we can write,

.. math::

    p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})p(\boldsymbol{d}| \text{class}_L, \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}.

Assuming that our set of considered lens classes is complete, the evidence of a single lens
(the denominator of the above equation) is,

.. math::

    p(\boldsymbol{d} | \mathcal{G}) = \sum_{\text{class}_L\in\text{classes}} p(\text{class}_L|\mathcal{G}) p(\boldsymbol{d}|\text{class}_L, \mathcal{G}).

We can now write the equations in a form that can be computed by introducing parameters of 
the microlensing light curve :math:`\theta=[t_{E}, \pi_{E}, \text{...}]`,

..  math::

    p(\text{class}_L | \boldsymbol{d}, \mathcal{G}) &= \frac{p(\text{class}_L| \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})} \\
    &\times \int p(\boldsymbol{d}| \theta ) p(\theta |\text{class}_L, \mathcal{G})d\theta.

We can compute the integral on the right hand side by importance sampling if we have :math:`S` 
independent posterior samples :math:`\theta_{c}\sim p(\theta|\boldsymbol{d})`
drawn under some prior, :math:`\pi(\theta)`, with wide support :cite:p:`Hogg2010`,

.. math::

    \begin{align}\label{eq:finalPosteriorclassIS}\nonumber
    \int p(\boldsymbol{d} | \theta ) &p(\theta |\text{class}_L, \mathcal{G})d\theta \approx  \\
    &\frac{1}{S} \sum_{c=0}^{S} \frac{ p(\theta_{c} |\text{class}_L, \mathcal{G})}{\pi(\theta_{c})}\,.
    \end{align}

This allows us to we leverage previously calculated posterior samples to perform
lens classification for a single event in the context of a Galactic model. The term,
:math:`p(\theta_{c} |\text{class}_L, \mathcal{G})` can be calculated by using kernel
density estimation over the single event observable space (e.g., :math:`t_{E}-\pi_{E}`) 
using a simulated catalog of microlensing events from :math:`\mathcal{G}`. 
:math:`p(\text{class}_L | \mathcal{G})` is the prior probability that a event belongs
to each class before any data is seen, which is just set by relative number of expected
events predicted by the Galactic model :math:`\mathcal{G}`.
