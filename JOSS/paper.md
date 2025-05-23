---
title: 'popclass: A Python Package for Classifying Microlensing Events'
tags:
  - Python
  - astronomy
  - Milky Way
  - black hole
authors:
  - name: Greg Sallaberry
    orcid: 0009-0001-4859-5205
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
  - name: William A. Dawson
    orcid: 0000-0003-0248-6123
    affiliation: 1
    equal-contrib: false
  - name: Caitlin G. Begbie
    orcid: 0009-0006-8866-4224
    affiliation: 3

affiliations:
 - name: Space Science Institute, Lawrence Livermore National Laboratory, 7000 East Ave., Livermore, CA 94550, USA
   index: 1
 - name: Astronomisches Rechen-Institut, Zentrum für Astronomie der Universität Heidelberg, Mönchhofstr. 12-14, 69120 Heidelberg, Germany
   index: 2
 - name: Department of Astronomy, University of California, Berkeley, 501 Campbell Hall, Berkeley, CA 94720, USA
   index: 3

date: 17 October 2024
bibliography: paper.bib

---

# Summary

`popclass` is a Python package that provides a flexible, probabilistic framework for classifying
the lens of a gravitational microlensing event. Gravitational microlensing occurs when a massive
foreground object (e.g., a star, white dwarf or black hole) passes in front of and
lenses the light from a distant background source. This causes an apparent brightening, and shift
in position, of the background source. In most cases, characteristics of the microlensing signal
do not contain enough information to definitively identify the lens type. Different lens
types lie in different but overlapping regions of the characteristics
of the microlensing signal. For example, black holes tend to be more massive than stars and
therefore cause microlensing signals that are longer. Current Galactic simulations enable us to predict
where different lens types lie in the observational space and can therefore be
used to classify events [e.g., @Lam2020].

`popclass` allows the user to match the characteristics of a microlensing signal with a simulation of the
Galaxy to calculate lens type probabilities for the event (see \autoref{lensclass}). Constraints on
any microlensing signal properties and any Galactic model can be used. `popclass`
comes with an interface to ArviZ [@arviz_2019] and PyMultiNest [@Buchner2014] for microlensing
signal constraints, as well as pre-loaded Galactic models, plotting functionality, and methods to quantify the classification uncertainty.
The probabilistic framework for popclass was developed in @Perkins2024,
used in @Fardeen2024 and has been applied to classifying events in @Kaczmarek2024.

# Statement of need

The advent of the Vera C. Rubin Observatory [@Ivezic2019] and the _Nancy Grace Roman Space Telescope_ [@Spergel2015]
will provide tens of thousands of microlensing events per year [e.g., @Abrams2023;@Penny2019]. To maximize the scientific output from this event stream, it is critical to identify events that have a high probability of being caused
by a certain lens type such as a black hole [@Sahu2022; @Lam2022], before we allocate expensive
follow-up observations such as space-based astrometry [e.g., @Sahu2022] or ground-based adaptive optics imaging [e.g., @Terry2022] to confirm their nature.

![Left: posterior distribution of an event in log10(timescale)-log10(parallax) space, overlaid on 'star', 'white dwarf', 'neutron star' and 'black hole' contours. Right: bars showing probabilities of that event belonging to each of the lens populations.\label{lensclass}](lens_class.png)

Current microlensing software packages such as DarkLensCode [@Howil2024] or pyLIMASS [@Bachelet2024] estimate
lens mass and distance constraints using the light curves of microlensing events and auxiliary information
(e.g., source proper motions, distances, color, or finite source effects). Using auxiliary information makes these
current methods powerful but limits their application to only be effective for events with the available auxiliary data. Moreover,
no current software tools explicitly predict the lens type, and they always assume a fixed Galactic model. `popclass` fills the
need for a flexible microlensing classification software package that can be broadly applied to classify all events
from the Vera C. Rubin Observatory and  _Nancy Grace Roman Space Telescope_ and can be used with any Galactic model
in the form of a simulation.

# Method

`popclass` is based on the Bayesian classification framework in @Perkins2024. Consider the data from a
single microlensing event $\boldsymbol{d}$, and a model of the Galaxy $\mathcal{G}$. `popclass`
calculates the probability that the lens of the event belongs to each lens class, $\text{class}_L$, where
$\text{class}_L\in\text{classes}$ and, for example,
$\text{classes} = \{\text{star, neutron star, white dwarf, black hole}\}$. Namely, `popclass` calculates

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) \text{ for } \text{class}_L\in\text{classes}.$$

Using Bayes' theorem,

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})p(\boldsymbol{d}| \text{class}_L, \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}.$$

Assuming that the set of considered lens classes is complete, $p(\boldsymbol{d}| \mathcal{G})$ is a normalization factor such that all lens class probabilities sum to unity. Using importance sampling [e.g., @Hogg2010] with $S$ independent posterior samples $\theta_{c}\sim p(\theta|\boldsymbol{d})$
drawn under some prior, $\pi(\theta)$, obtained from fitting some set of microlensing signal parameters, $\theta$,

$$p(\text{class}_L | \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}
    \times \frac{1}{S} \sum _{c=0}^{S} \frac{p(\theta _c | \text{class}_L, \mathcal{G})}{\pi(\theta _{c})}.$$

This allows the use of previously calculated posterior samples to perform lens classification for a single event in
the context of a Galactic model. The term $p(\theta_c | \text{class}_ L, \mathcal{G})$ is calculated using kernel
density estimation in `popclass` over $\theta$ with a simulated catalog of microlensing events
from $\mathcal{G}$. $p(\text{class}_L | \mathcal{G})$ is the prior probability that an event belongs to each class before
any data is seen, which is simply set by the relative number of expected events predicted by the Galactic model $\mathcal{G}$.

# Acknowledgements

`popclass` depends on NumPy [@Harris2020], SciPy [@Virtanen2020], ASDF [@Greenfield2015], Matplotlib [@Hunter2007], and scikit-learn [@sklearn_api].
This work was performed under the auspices of the U.S.
Department of Energy by Lawrence Livermore National
Laboratory (LLNL) under Contract DE-AC52-07NA27344. The document number is LLNL-JRNL-870290 and the code number is LLNL-CODE-2000456.
The theoretical foundation of this work was established
under support from LLNL’s
Laboratory Directed Research and Development Program
under project 22-ERD-037. The software implementation
for this project was funded under the LLNL
Space Science Institute's Institutional Scientific
Capability Portfolio funds in partnership with LLNL’s
Academic Engagement Office. ZK acknowledges support from the
2024 LLNL Data Science Summer Institute and is a Fellow of
the International Max Planck Research School for Astronomy
and Cosmic Physics at the University of Heidelberg (IMPRS-HD).

# References
