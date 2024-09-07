# popclass

[![Documentation Status](https://readthedocs.org/projects/popclass/badge/?version=latest)](https://popclass.readthedocs.io/en/latest/?badge=latest) ![Tests](https://github.com/LLNL/popclass/actions/workflows/test.yml/badge.svg) [![codecov](https://codecov.io/gh/LLNL/popclass/graph/badge.svg?token=A4DAAGSE2V)](https://codecov.io/gh/LLNL/popclass) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/LLNL/popclass/main.svg)](https://results.pre-commit.ci/latest/github/LLNL/popclass/main)

popclass is a lightweight python package that allows fast, probabilistic classification of the lens of a microlensing event given the event's posterior distribution and a model of the Galaxy. popclass provides the bridge between Galactic simulation and lens classification, an interface to common Bayesian inference libraries, and the ability for users to flexibly specify their own Galactic model and classification parameters.

For more details on the project please see the documentation.

![image info](./docs/images/lens_class.gif)

Example of popclass classifying a microlensing event with a range of different posterior distributions. Left panel shows a population simulation used to classify the event. Right panel shows the output lens classification from popclass which is calculated by combining the event posterior information with the simulation.

## License

popclass is distributed under the terms of the MIT license. All new contributions must be made under the MIT license.

See Link to [license](https://github.com/LLNL/popclass/blob/main/LICENSE) and [NOTICE](https://github.com/LLNL/popclass/blob/main/NOTICE) for details.

SPDX-License-Identifier: MIT

LLNL-CODE-2000456
