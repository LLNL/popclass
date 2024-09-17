---
title: 'popclass: a python package for classifying microlensing events'
tags:
  - Python
  - astronomy
  - milky way
  - black hole
authors:
  - name: Greg Sallaberry
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 1
  - name: Zofia Kaczmarek
    orcid: 0009-0007-4089-5012
    equal-contrib: true
    affiliation: "1, 2"
  - name: Peter McGill
    orcid: 0000-0002-1052-6749
    corresponding: true
    affiliation: 1
    equal-contrib: true
  - name: Scott E. Perkins
    orcid: 0000-0002-5910-3114
    affiliation: 1
    equal-contrib: true

affiliations:
 - name: Space Science Institute, Lawrence Livermore National Laboratory, 7000 East Ave., Livermore, CA 94550, USA
   index: 1
 - name: Zentrum fur Astronomie der Universitat Heidelberg, Astronomisches Rechen-Institut, Monchhofstr. 12-14, 69120 Heidelberg, Germany
   index: 2

date: 13 August 2017
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi:
aas-journal:
---

# Summary
`popclass` is a lightweight Python library that provides a flexible, probabilistic framework for classification based on a model.
The primary and first intended use case is in classifying microlensing events based on the event posterior and subject to a pre-specified galactic model.
At base level, the library solves the following:

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) \text{ for } \text{class}_L\in\text{classes}$$

\- the probability that an event belongs to class L given microlensing event light curve data $\boldsymbol{d}$ and a galactic model $\mathcal{G}$.

The library includes several models containing information on several key parameters which may be useful for lens classification ($\log_{10}t_E$, $\log_{10}\pi_E$, $\log_{10}\theta_E$, and $f_{\rm{blend}}$), but allows the user to provide their own model file so long as it is consistent with the supplied posterior at each step of analysis.
`popclass` also supplies tools for visualizing population models (in multi-dimensional parameter space) alongside the supplied posterior samples (FIGURE?).

# Statement of need
In the current climate of observational astronomy, with the _Vera C. Rubin Observatory_ [@Ivezic2019] and the _Nancy Grace Roman Space Telescope_ [@Spergel2015] soon to see first light, selection of interesting targets becomes key to maximizing science output.
In the realm of time-domain astronomy and transients, it is important to be able to quickly identify targets for follow-up imaging with confidence that the selected object is an appropriate use of resources.
Use of the classifier is not computationally intensive; the code creates kernel density estimates via `scipy` [@Virtanen2020], but otherwise relies on Galactic model simulations and event parameter fitting to have been run prior.

With the recent discovery of the first confirmed isolated stellar-origin black hole [@Sahu2022; @Lam2022], the search for microlensing dark remnants is a timely topic. While other codes for inferring lens properties - such as `DarkLensCode` [@Howil2024] or `PyLiMASS` [@Bachelet2024] - have recently been made public and have yielded successful mass determinations and dark remnant candidates, their strengths lie in incorporating additional follow-up information (e.g. source proper motions and distances, multiband photometry or spectroscopy, finite source effect). We provide a complimentary method that is flexible, lightweight and does not require any information beyond that easily obtainable from the event light curve (e.g. $\log_{10} t_{\rm E} - \log_{10}\pi_{\rm E}$ posterior distributions). Our method also assesses the inherent uncertainty of its classifications, which is crucial in cases of low information content or missing populations [@Kaczmarek2024]. Those qualities make our classifier a perfect tool to apply to wide databases and filter promising events for follow-up, which is specifically desirable in the era of microlensing databases containing $\sim 10^4$ events. Furthermore, we provide tools to quantify and visualize intrinsic uncertainty over a parameter space given a Galactic model, which will also aid in making follow-up decisions - e.g. to free up resources for other events rather than further constraining an event posterior, if tighter constraints cannot decrease its classification uncertainty.

We aim to make `popclass` maximally flexible and user-friendly. All astrophysical assumptions come from the Galactic model, which can be freely modified by the user either by injecting additional populations or by providing a new set of population samples altogether. We use the Advanced Scientific Data Format (ASDF) [@Greenfield2015], which is set to become a new standard for astronomical data, as a default solution for storing population models. In case of posteriors, we provide a convenient interface to commonly used Bayesian inference libraries, such as `dynesty` [@Speagle2020], `pymultinest` [@Buchner2016] or `ArviZ` [@arviz_2019], as well as microlensing-specific libraries such as BAGLE[^1], so that their output can be directly read by `popclass`. The parameter set is also modifiable to adjust to the science case, both within and outside of microlensing. A natural example is a straightforward extension to astrometry by incorporating the event's angular scale $\theta_{\rm E}$, which is particularly important for the upcoming _Roman Space Telescope_ data. Generally, `popclass` can be applied to any problem where a posterior distribution is to be classified given simulated samples of target classes in a given parameter space.

(current and expected use cases: please fill!)

[^1]:[https://github.com/MovingUniverseLab/BAGLE_Microlensing](https://github.com/MovingUniverseLab/BAGLE_Microlensing)

# Method

While lens classification in microlensing is the primary use case for
`popclass`, it relies on a completely general Bayesian framework from
[@Perkins2024]. Consider the data from a single microlensing
event light curve $\boldsymbol{d}$, using a model of the Galaxy
$\mathcal{G}$, popclass calculates the probability that the lens of the
events belongs to each lens class, $\text{class}_L$, where
$\text{class}_L\in\text{classes}$ and $\text{classes} = \{\text{Star, Neutron Star, White Dwarf, Black Hole}\}$. Namely, popclass calculates

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) \text{ for } \text{class}_L\in\text{classes}.$$

Using Bayes' theorem we can write,

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})p(\boldsymbol{d}| \text{class}_L, \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}.$$

Assuming that our set of considered lens classes is complete, the evidence of a single lens
(the denominator of the above equation) is,

$$p(\boldsymbol{d} | \mathcal{G}) = \sum_{\text{class}_L\in\text{classes}} p(\text{class}_L|\mathcal{G}) p(\boldsymbol{d}|\text{class}_L, \mathcal{G}).$$

We can now write the equations in a form that can be computed by introducing parameters of
the microlensing light curve $\theta=[t_{E}, \pi_{E}, \text{...}]$,

$$p(\text{class}_L | \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}
    \times \int p(\boldsymbol{d}| \theta ) p(\theta |\text{class}_L, \mathcal{G})d\theta.$$

We can compute the integral on the right hand side by importance sampling if we have $S$ independent posterior samples $\theta_{c}\sim p(\theta|\boldsymbol{d})$
drawn under some prior, $\pi(\theta)$, with wide support [@Hogg2010],

$$ \int p(d | \theta) p(\theta | \text{class}_L, \mathcal{G}) d\theta \approx \frac{1}{S} \sum _{c=0}^{S} \frac{p(\theta _c | \text{class}_L, \mathcal{G})}{\pi(\theta _{c})} $$

This allows us to we leverage previously calculated posterior samples to perform
lens classification for a single event in the context of a Galactic model. The term
$p(\theta_c | \text{class}_ L, \mathcal{G})$ can be calculated by using kernel density estimation over the single event observable space (e.g., $t_{E}-\pi_{E}$) using a simulated catalog of microlensing events from $\mathcal{G}$.
$p(\text{class}_L | \mathcal{G})$ is the prior probability that a event belongs
to each class before any data is seen, which is just set by relative number of expected
events predicted by the Galactic model $\mathcal{G}$.

# Figures

# Acknowledgements

This work was performed under the auspices of the U.S.
Department of Energy by Lawrence Livermore National
Laboratory (LLNL) under Contract DE-AC52-07NA27344.
The theoretical foundation of this work was established
under support from Lawrence Livermore National Laboratory’s
Laboratory Directed Research and Development Program
under project 22-ERD-037. The software implementation
for this project was funded under the LLNL
Space Science Institute's Institutional Scientific
Capability Portfolio funds in partnership with LLNL’s
Academic Engagement Office. This work was prepared as an account of
work sponsored by an agency of the United States
Government. Neither the United States Government nor Lawrence Livermore National Security,
LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any
legal liability or responsibility for the accuracy, completeness, or usefulness of any
information, apparatus, product, or process disclosed, or represents that its use would
not infringe privately owned rights. Reference herein to any specific commercial product,
process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United States
Government or Lawrence Livermore National Security, LLC. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the United States Government
or Lawrence Livermore National Security, LLC, and shall not be used for advertising or
product endorsement purposes.

# References
