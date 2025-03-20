popclass
========

popclass is a python package that allows flexible, probabilistic classification of
the lens of a microlensing event given the event's posterior distribution and a model of
the Galaxy. popclass provides the bridge between Galactic simulation and lens classification,
an interface to common Bayesian inference libraries, and the ability for users to flexibly
specify their own Galactic model and classification parameters.

popclass is being actively
developed on `GitHub <https://github.com/LLNL/popclass>`_.

.. figure:: ../images/lens_class.gif

   Example of popclass classifying a microlensing event
   with a range of different posterior distributions.
   Left panel shows a population simulation used to classify
   the event. Right panel shows the output lens classification
   from popclass which is calculated by combining the event posterior
   information with the simulation.

.. note:: Finding your way around

   A good place to get started is with the installation guide, getting started page and
   the the tutorial examples.

   If you are here to develop on popclass, please head over to the contributing guide.

   If you have issues with the software or need support please open a `github issue <https://github.com/LLNL/popclass/issues>`_.


Contents
--------

.. toctree::
   :titlesonly:
   :maxdepth: 1

   installation
   getting_started.ipynb
   background
   tutorials
   library
   acknowledgements
   contributing
   developer
   changelog
   references
   api
