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

------------------------------------
Event parameter prior considerations
------------------------------------

To properly use importance sampling, as outline above, one must reweight the posterior samples by the original prior on the event parameters :math:`\pi(\theta_{c})`.
This yields a classification probability invariant under the original choice of prior for the event parameters (disregarding numerical error in the re-sampling and assuming the prior is smooth and continuous), a very attractive feature in this framework due to the fully Bayesian nature of the calculation.
However, for this to be done properly, the prior density must be evaluated in the exact same parameter space as the population model density :math:`p(\theta_{c} |\text{class}_L, \mathcal{G})`.
It is up to the user to ensure the prior being density values supplied with the posterior samples are the correct density, matching the parameter space used in the population model.

A common example of this issue that might arise in this context is the transformation from linear to logrimthic spaces.
If an event's posterior was sampled in linear :math:`t_E-\pi_E` space, but the population model is evaulated in the :math:`\log_{10} t_E - \log_{10} \pi_E` space, one must use the proper Jacobian to transform the probability densities to a consistent space.
E.g.,

.. math::

        \pi(\log_{10} t_E, \log_{10} \pi_E) = |\mathbf{J}| \pi(t_E, \pi_E) \,,

where :math:`|\mathbf{J}|` is the determinant of the Jacobian of the transformation from :math:`t_E-\pi_E` to :math:`\log_{10} t_E - \log_{10} \pi_E`.
Explicitly, in this example, that comes out to

.. math::

        |\mathbf{J}| = (\ln 10)^2  (t_E   \pi_E) \,,

giving a final form of the prior

.. math::

        \pi(\log_{10} t_E, \log_{10} \pi_E) = (\ln 10)^2   (t_E   \pi_E) \pi(t_E, \pi_E) \,.

Even in the case that a uniform prior was used for :math:`t_E` and :math:`\pi_E`, the resulting prior needed in this framework will not be uniform :math:`\log_{10} t_E` and :math:`\log_{10} \pi_E`, giving biased results if this transformation is not taken into account.

------------------------------------------------------
Uncertainty Quantification - :math:`\text{None}` Class
------------------------------------------------------

Quantifying the uncertainty in classifying events into subpopulations is not a uniquely solvable problem, but some specific instances can be diagnosed.
One example of a systematic effect that we would like to mitigate comes about when an event posterior extends well beyond the domain of the simulation data for all the classes.
This could be a shift of the mean of the posterior outside the domain of support or an inflation of the posterior well beyond said domain.
In this case, one might apply our classifier to the event posterior, obtaining a strong probability of this event belonging to a specific class.
However, this could be a deceptive conclusion if taken at face value, as there is a real possibility that the classifier is simply picking the best of many bad explanations of the data and the result is driven by the noisy tails of the class distributions.
This situation illustrates a case where information is lost about the completeness of the simulation and the overall ability of the population model to explain a specific event when we assumed the set of classes was complete.

We implement in this package one method to handle this uncertainty, by appending an additional population on top of the existing simulation data.
This additional population, which we will denote as the :math:`\text{None}` class following the notation of :cite:t:`Kaczmarek2024`, will be designed to be the complement to the modeled populations in the simulation (defined more precisely below).
By injecting a non-physical "class" into the population model which fills up the parameter space not occupied by the physical population model, we now have a metric to quantify the lack of our population model to explain an events posterior.
If an event has a substantial probability to belong to the :math:`\text{None}` class, we know that the population model struggled to confidently identify it as belonging to the physical classes, even if one of those physical classes dominates over the other physical classes.
Therefore, this event should receive more careful consideration, as it might be an outlier of the population model.

The way in which this :math:`\text{None}` class is defined is somewhat subjective, and several methods might need to be employed to marginalize over this choice.
For now, we following :cite:t:`Kaczmarek2024` and define this class as

.. math::
    p(\theta | \text{None},\mathcal{G}) = A \left( 1 - \frac{p(\theta | \mathcal{G})}{\max_{\hat{\phi}} (p(\hat{\phi} | \mathcal{G}))} \right)\,,

where, as above, :math:`\theta` represents a vector of event parameters, and :math:`\mathcal{G}` generally represents all other assumptions about the modeling (such as the galactic model, in the microlensing context).
The quantity :math:`p(\theta | \mathcal{G})` represents the prediction for :math:`\theta` marginalized over class, i.e., for the entire population model as a whole (excluding the :math:`\text{None}` class).
The quantity :math:`A` is the normalization constant that ensures :math:`p(\theta | \text{None},\mathcal{G})` is properly normalized over the entire, supported parameter space.
With this definition, the :math:`\text{None}` class is appended onto the list of possible classes that events are classified into, and it is subsequently treated identically as the physical classes.
