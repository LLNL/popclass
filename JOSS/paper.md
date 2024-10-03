---
title: 'popclass: a python package for classifying microlensing events'
tags:
  - Python
  - astronomy
  - milky way
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
    orcid: 0000-0000-0000-0000
    affiliation: 3

affiliations:
 - name: Space Science Institute, Lawrence Livermore National Laboratory, 7000 East Ave., Livermore, CA 94550, USA
   index: 1
 - name: Zentrum fur Astronomie der Universitat Heidelberg, Astronomisches Rechen-Institut, Monchhofstr. 12-14, 69120 Heidelberg, Germany
   index: 2
 - name: University of California, Berkeley, Astronomy Department, Berkeley, CA 94720, USA
   index: 3

date: 13 August 2017
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi:
aas-journal:
---

# Summary

`popclass` is a Python library that provides a flexible, probabilistic framework for classifying
the lens of a gravitational microlensing event. Gravitational microlensing occurs when a massive
foreground object - the lens (e.g., a star, white dwarf or a black hole) passes infront of and
deflects the light from a distant background star. This causes an apparant brightening, and shift
in position, of the background source. In most cases, characteristics of the microlensing
signal do not contain enough information to definitively identity the lens type. However, different
lens types (e,g., Stars vs black holes) can lie in different but overlapping regions of
the characteristics of the microlensing signal. For examples, black holes tend to be more massive than
stars and therefore cause microlensing signals that are longer. Current Galactic models allow the simulation
of where differnt lens types lie in the observational space and can therefore be leveraged to classify
an event [@Lam2020].

`popclass` allows a user to match characteristics of a microlensing signal to a simulation of the
Galaxy to calculate lens class probabilities for an event. The user can flexibly use constraints
on any microlensing signal characteristics and specific their own Galactic simulation.
`popclass` also comes with an interface to `ArviZ` [@arviz_2019] and `pymultinest` [@Buchner2016]
for microlesning signal constraints, pre-loaded Galactic simulations, plotting fuctionality,
and uncertainty quantification methods that can be included in the classification calculation.

# Statement of need

The advent of the _Vera C. Rubin Observatory_ [@Ivezic2019] and the _Nancy Grace Roman Space Telescope_ [@Spergel2015]
will trigger a deludge of tens-of-thousands of microlensing events per year [@Abrams2023;@Penny2019].
To miximize the science output of this event stream it is critical to identify events that have a high proablity of being
caused by interesting lens types such as an isolated black hole [@Sahu2022; @Lam2022], and then to allocate expensive follow-up
observations such as space based astrometry [@Sahu2022] or ground based adaptic optics imaging [@Terry2022] to confirm their nature. 

Current microlensing software packages such as `DarkLensCode` [@Howil2024] or `PyLiMASS` [@Bachelet2024] estimate lens 
mass-distance constraints using microlensing event lightcurve and additional auxillary information 
(e.g. source proper motions,distances, color, or finite source effect). Using axillary information makes these current
methods powerful but limits them to only be effective for events with the available auxillary data. 
Moreoever, no current software tools explicitly predict lens type and always assumes a fixed Galactic model.
`popclass` fills the need for a flexiable microlensing classification software package that can be broadly 
applied to classify all events from the Vera C. Rubin Observatory and  _Nancy Grace Roman Space Telescope_
and can be used with any Galactic model in the form of a simuation.

# Method

`popclass` relies on the general Bayesian classification framework detailed in [@Perkins2024]. Consider the data from a
single microlensing event light curve $\boldsymbol{d}$, using a model of the Galaxy $\mathcal{G}$, `popclass`
calculates the probability that the lens of the events belongs to each lens class, $\text{class}_L$, where
$\text{class}_L\in\text{classes}$ and for exmaple,
$\text{classes} = \{\text{Star, Neutron Star, White Dwarf, Black Hole}\}$. Namely, `popclass` calculates

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) \text{ for } \text{class}_L\in\text{classes}.$$

Using Bayes' theorem we can write,

$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})p(\boldsymbol{d}| \text{class}_L, \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}.$$

Assuming that our set of considered lens classes is complete, and using importance sampling [@Hogg2010] with $S$ independent posterior samples $\theta_{c}\sim p(\theta|\boldsymbol{d})$
drawn under some prior, $\pi(\theta)$, obtained from fittings some parameters $\theta=[t_{E}, \pi_{E}, \text{...}]$ of the microlensing signal,

$$p(\text{class}_L | \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})}
    \times \frac{1}{S} \sum _{c=0}^{S} \frac{p(\theta _c | \text{class}_L, \mathcal{G})}{\pi(\theta _{c})}$$.

This allows us to we leverage previously calculated posterior samples to perform lens classification for a single event in
the context of a Galactic model. The term $p(\theta_c | \text{class}_ L, \mathcal{G})$ can be calculated by using kernel
density estimation in `popclass` over the single event observable space using a simulated catalog of microlensing events
from $\mathcal{G}$. $p(\text{class}_L | \mathcal{G})$ is the prior probability that a event belongs to each class before
any data is seen, which is just set by relative number of expected events predicted by the Galactic model $\mathcal{G}$.

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
Government. Neither the United States Government nor Lawrence Livermore
National Security,
LLC, nor any of their employees makes any warranty,
expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any
information, apparatus, product, or process disclosed, or represents that its use would
not infringe privately owned rights. Reference herein to any specific commercial product,
process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United States
Government or Lawrence Livermore National Security, LLC. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the United States Government
or Lawrence Livermore National Security, LLC, and shall not be used for advertising or
product endorsement purposes.

# References
