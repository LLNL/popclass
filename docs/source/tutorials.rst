=========
Tutorials
=========

Converting and creating posterior objects
-----------------------------------------

``popclass`` includes convenience functions for ingesting common inference
data objects.
While an array of samples and associated parameter labels can be passed
directly to ``popclass.Posterior``, we currently support conversion from
the following output formats:

* ArviZ

To create a ``popclass.Posterior`` object from ArviZ:

.. code-block:: python

    from popclass.posterior import Posterior

    post = Posterior.from_arviz(arviz_inference_data)


Alternatively, ``Posterior`` can be initialized with an array of samples and
a list of parameter labels.

.. code-block:: python

    samples = np.random.randn(1000, 2)
    labels = ['log10tE', 'log10piE']

    post = Posterior(samples, labels)

Population model data format
----------------------------

In this section we will cover how simulation data from a population model
is saved. You might find this useful if you are planning on creating your
own population model and contributing it to popclass.

popclass models can be saved in the ASDF (Advanced Scientific Data Format).
This Python implementation of the ASDF Standard can be found
`here <https://asdf.readthedocs.io/en/latest/>`_ and more information
on the ASDF Standard itself can be found in :cite:`Greenfield2015`.

Here is an example schema of a popclass population model file
:code:`popsycle_singles_raithel18.asdf`.

.. code-block:: python

    import asdf

    f = asdf.open('popsycle_singles_sukhboldn20.asdf')
>>> f.info(max_rows=None)
root (AsdfObject)
├─asdf_library (Software)
│ ├─author (str): The ASDF Developers
│ ├─homepage (str): http://github.com/asdf-format/asdf
│ ├─name (str): asdf
│ └─version (str): 3.3.0
├─history (dict)
│ └─extensions (list)
│   └─[0] (ExtensionMetadata)
│     ├─extension_class (str): asdf.extension._manifest.ManifestExtension
│     ├─extension_uri (str): asdf://asdf-format.org/core/extensions/core-1.5.0
│     ├─manifest_software (Software)
│     │ ├─name (str): asdf_standard
│     │ └─version (str): 1.1.1
│     └─software (Software)
│       ├─name (str): asdf
│       └─version (str): 3.3.0
├─class_data (dict)
│ ├─black_hole (NDArrayType): shape=(17, 4), dtype=float64
│ ├─neutron_star (NDArrayType): shape=(21, 4), dtype=float64
│ ├─star (NDArrayType): shape=(1255, 4), dtype=float64
│ └─white_dwarf (NDArrayType): shape=(178, 4), dtype=float64
├─class_weights (dict)
│ ├─black_hole (float): 0.011556764106050306
│ ├─neutron_star (float): 0.014276002719238613
│ ├─star (float): 0.8531611148878314
│ └─white_dwarf (float): 0.12100611828687967
├─model_name (str): popsycle_singles_sukhboldn20
└─parameters (list)
  ├─[0] (str): log10tE
  ├─[1] (str): log10piE
  ├─[2] (str): log10thetaE
  └─[3] (str): f_blend_I

Here is an example of how to create a popclass population model file
from a nested python dictionary with the same structure but with random
mock class data.

.. code-block:: python

    import asdf
    import numpy as np


    parameters = ['log10tE', 'log10PiE', 'log10thetaE', 'f_blend_I']
    class_data = {"black_hole": np.random.randn(17, 4),
                  "neutron_star": np.random.randn(21,4),
                  "star": np.random.randn(1255,4),
                  "white dwarf": np.random.randn(178,4)}

    model_name = 'popsycle_singles_sukhboldn20'
    class_weights = {
                    "black_hole": 0.011556764106050306,
                    "neutron_star": 0.014276002719238613,
                    "star": 0.8531611148878314,
                    "white_dwarf": 0.12100611828687967
                     }

    tree = {
        "class_data": class_data,
        "parameters": parameters,
        "class_weights": class_weights,
        "model_name": "popsycle_singles_imfr_sukhboldn20"
    }

    af = asdf.AsdfFile(tree)
    af.write_to("example.asdf")

To read-in a user-generated population model:

.. code-block:: python

    from popclass.model import PopulationModel

    file = 'path/to/file.asdf'
    user_population_model = PopulationModel.from_asdf(file)

Additionally, to contribute a population model to the library,
the file may be placed in ``popclass/data`` and then added to the list of
``AVAILABLE_MODELS`` in ``model.py``.
The data can then be read using ``from_library().``
The format of the data in the asdf file must match the existing schema for
the included models as described above.
The model can then be read in directly from the library via

.. code-block:: python

    # use the above example
    model_name = 'popsycle_singles_raithel18'
    population_model = PopulationModel.from_library(model_name)

Using the classifier
--------------------
In order to perform object classification, the user must specify *both* a
``PopulationModel`` and an ``InferenceData`` object.
The creation of the ``PopulationModel`` is as described above and the
``InferenceData`` object can be created from an existing ``Posterior`` object
by passing a prior density to the ``Posterior.to_InferenceData`` method:

.. code-block:: python

    from popclass.posterior import Posterior, InferenceData

    # set a uniform prior for demonstration
    num_samples = (1000)
    prior = np.ones(num_samples)

    # for the above posterior object
    inference_data = post.to_InferenceData(prior)

The ``InferenceData`` object can also be formed using the marginal distribution
formed by ``popclass.Posterior.marginal()``.

To run the classifier, the user must also pass the ``classify()`` function the
parameters to use for classification.
The models supplied by ``popclass`` include the following parameters:

* 'log10tE'
* 'log10PiE'
* 'log10thetaE'
* 'f_blend_I'

.. code-block:: python

    from popclass.classify import classify

    classification = (population_model, inference_data, parameters=['log10tE', 'log10piE'])

This will return a dictionary of object clases with their associated probabilities.
