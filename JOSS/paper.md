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
   ror: 00hx57361
 - name: Zentrum f{\"u}r Astronomie der Universit{\"a}t Heidelberg, Astronomisches Rechen-Institut, M{\"o}nchhofstr. 12-14, 69120 Heidelberg, Germany
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
$$ p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) \text{ for } \text{class}_L\in\text{classes}$$
the probability that an event belongs to class L given microlensing event light curve data $\boldsymbol{d}$ and a galactic model $\mathcal{G}$.

The library includes several models containing information on several key parameters which may be useful for lens classification ($\log_{10}t_E$, $\log_{10}\pi_E$, $\log_{10}\theta_E$, and $f_{\rm{blend}}$), but allows the user to provide their own model file so long as it is consistent with the supplied posterior at each step of analysis.
`popclass` also supplies tools for visualizing population models (in multi-dimensional parameter space) alongside the supplied posterior samples (FIGURE?).

# Statement of need
In the current climate of observational astronomy, with the Vera C. Rubin Observatory (CITE) and the Nancy Grace Roman Space Telescope (CITE) soon to see first light, selection of interesting targets becomes key to maximizing science output.
In the realm of time-domain astronomy and transients, it is important to be able to qiuckly identify targets for follow-up imaging with confidence that the selected object is an appropriate use of resources.
Use of the classifier is not computationally intensive; the code creates kernel density estimates via `scipy` (CITE?), but otherwise relies on galactic model simulations and event parameter fitting to have been run prior.

*Talk about DarkLens code and PyLIMAS and things that are related*

# Method
While lens classification in microlensing is the primary use case for `popclass`, it relies on a completely general Bayesian framework.
Extending on the framework introduced above, we can use Bayes' Theorem
$$p(\text{class}_L| \boldsymbol{d}, \mathcal{G}) = \frac{p(\text{class}_L| \mathcal{G})p(\boldsymbol{d}| \text{class}_L, \mathcal{G})}{p(\boldsymbol{d}| \mathcal{G})},$$

*include the rest of the math from the background*



# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

# Figures

# Acknowledgements

This work was performed under the auspices of the U.S.
Department of Energy by Lawrence Livermore National
Laboratory (LLNL) under Contract DE-AC52-07NA27344.
The theoretical foundation of this work was established
under support from Lawrence Livermore National Laboratory’s
Laboratory Directed Research and Development Program
under project [22-ERD-037](https://ldrd-annual.llnl.gov/ldrd-annual-2023/project-highlights/space-security/new-dark-matter-and-early-universe-grand-science-campaign). The software implementation
for this project was funded under the LLNL
[Space Science Institute's](https://space-science.llnl.gov/) Institutional Scientific
Capability Portfolio funds in partnership with LLNL’s
[Academic Engagement Office](https://st.llnl.gov/about-us/AEO).
This work was prepared as an account of work sponsored by an agency of the United States
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
