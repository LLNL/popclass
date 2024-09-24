import numpy as np
import pytest
from pytest import approx
from scipy.stats import multivariate_normal
from scipy.stats import norm

from popclass.model import PopulationModel
from popclass.posterior import Posterior
from popclass.uq import additiveUQ
from popclass.uq import NoneClassUQ


def test_additiveUQ():
    """Test the template class for additive UQ.
    Ensure it does nothing by default.
    """
    classes = ["A", "B"]
    parameters = ["p1", "p2"]
    samples = {
        cname: norm.rvs(size=200, loc=1, scale=1).reshape((100, 2)) for cname in classes
    }
    class_weights = {"A": 0.3, "B": 0.7}
    population_model = PopulationModel(
        population_samples=samples, class_weights=class_weights, parameters=parameters
    )

    posterior_samples = norm.rvs(size=200, loc=5, scale=1).reshape((100, 2))
    posterior_data = Posterior(posterior_samples, parameters)
    prior = np.ones((100))
    inference_data = posterior_data.to_inference_data(prior)

    unnormalized_prob = {"A": 80, "B": 20}

    additive_uq = additiveUQ()
    new_probs = additive_uq.apply_uq(
        unnormalized_prob=unnormalized_prob,
        inference_data=inference_data,
        population_model=population_model,
        parameters=parameters,
    )
    for key, item in unnormalized_prob.items():
        assert item == new_probs[key]


def test_none_class_kde_build():
    """Test to make sure the total kde built for None class is accurate"""
    np.random.seed(seed=1)
    bounds = {"p1": [-10, 10], "p2": [-10, 10], "p3": [-10, 10]}
    grid_size = int(1e1)

    classes = ["A", "B", "C"]
    nclasses = len(classes)
    parameters = ["p1", "p2", "p3"]
    ndim = len(parameters)

    means = {"A": 1 * np.ones(ndim), "B": -1 * np.ones(ndim), "C": 0 * np.ones(ndim)}
    covs = {"A": 1 * np.eye(ndim), "B": 1 * np.eye(ndim), "C": 1 * np.eye(ndim)}

    nsamples = 100000
    samples = {
        cname: multivariate_normal.rvs(
            size=nsamples, mean=means[cname], cov=covs[cname]
        )
        for cname in classes
    }
    class_weights = {
        "A": float(nsamples) / (nclasses * nsamples),
        "B": float(nsamples) / (nclasses * nsamples),
        "C": float(nsamples) / (nclasses * nsamples),
    }

    population_model = PopulationModel(
        population_samples=samples, class_weights=class_weights, parameters=parameters
    )

    none_class = NoneClassUQ(
        bounds=bounds,
        grid_size=grid_size,
        population_model=population_model,
        parameters=parameters,
        kde_kwargs={"bw_method": "scott"},
    )

    test_point = np.array([0, 0, 0])
    true_value = np.sum(
        [
            class_weights[cname]
            * multivariate_normal.pdf(test_point, mean=means[cname], cov=covs[cname])
            for cname in classes
        ]
    )

    # Assert the answer matches the truth to within 5%.
    assert none_class.base_model_kde(test_point) == approx(true_value, rel=0.05)


def test_none_class_build_grids():
    """Test the construction of the grids for evaluating none class"""
    bounds = {"A": [0, 1], "B": [1, 2], "C": [2, 3]}
    ndim = len(bounds.keys())
    grid_size = int(1e2)

    # Define grid by corners
    grid = {
        p: np.linspace(bounds[p][0], bounds[p][1], grid_size) for p in bounds.keys()
    }
    grid_mesh = np.array(np.meshgrid(*list(grid.values())))
    grid_corners = np.array([a.ravel() for a in grid_mesh]).transpose()

    # Define grid by centers
    grid_centers = {p: (grid[p][1:] + grid[p][:-1]) / 2 for p in grid.keys()}
    grid_mesh_centers = np.array(np.meshgrid(*list(grid_centers.values())))
    grid_centers_raveled = np.array([a.ravel() for a in grid_mesh_centers]).transpose()

    classes = ["A", "B"]
    parameters = ["p1", "p2", "p3"]
    samples = {
        cname: norm.rvs(size=300, loc=1, scale=1).reshape((100, 3)) for cname in classes
    }
    class_weights = {"A": 0.3, "B": 0.7}
    population_model = PopulationModel(
        population_samples=samples, class_weights=class_weights, parameters=parameters
    )

    none_class = NoneClassUQ(
        population_model=population_model,
        parameters=parameters,
        bounds=bounds,
        grid_size=grid_size,
    )

    # Check Shapes
    for key, bds in none_class.grid.items():
        assert bds.shape[0] == grid_size
    shape_template = [ndim]
    for i in np.arange(shape_template[0]):
        shape_template.append(grid_size)
    assert np.all(np.array(none_class.grid_mesh.shape) == shape_template)
    shape_template = [grid_size, ndim]
    for i in np.arange(shape_template[1] - 1):
        shape_template[0] *= grid_size
    assert np.all(np.array(none_class.grid_corners.shape) == shape_template)

    # Check values
    for key, boundary in grid.items():
        assert np.all(boundary == none_class.grid[key])
    assert np.all(grid_mesh == none_class.grid_mesh)
    assert np.all(grid_corners == none_class.grid_corners)
    for key, bds in none_class.grid.items():
        assert bds.shape[0] == grid_size

    # Check Shapes
    for key, bds in none_class.grid_centers.items():
        assert bds.shape[0] == grid_size - 1
    shape_template = [ndim]
    for i in np.arange(shape_template[0]):
        shape_template.append(grid_size - 1)
    assert np.all(np.array(none_class.grid_mesh_centers.shape) == shape_template)
    shape_template = [grid_size - 1, ndim]
    for i in np.arange(shape_template[1] - 1):
        shape_template[0] *= grid_size - 1
    assert np.all(np.array(none_class.grid_centers_raveled.shape) == shape_template)

    # Check values
    for key, boundary in grid_centers.items():
        assert np.all(boundary == none_class.grid_centers[key])
    assert np.all(grid_mesh_centers == none_class.grid_mesh_centers)
    assert np.all(grid_centers_raveled == none_class.grid_centers_raveled)


def test_uq_input_errors():
    """
    Test errors are returned if insufficient input for creating the None class is provided.
    """
    bounds = {"A": [0, 1], "B": [1, 2], "C": [2, 3]}

    classes = ["A", "B"]
    parameters = ["p1", "p2", "p3"]
    grid_size = int(1e1)
    samples = {
        cname: norm.rvs(size=300, loc=1, scale=1).reshape((100, 3)) for cname in classes
    }
    class_weights = {"A": 0.3, "B": 0.7}

    population_model = PopulationModel(
        population_samples=samples, class_weights=class_weights, parameters=parameters
    )

    # provide no base kde or popmodel
    with pytest.raises(ValueError):
        none_class = NoneClassUQ(
            parameters=parameters, bounds=bounds, grid_size=grid_size
        )
    # provide no parameters
    with pytest.raises(ValueError):
        none_class = NoneClassUQ(
            population_model=population_model, bounds=bounds, grid_size=grid_size
        )

    # provide no kde object or method
    with pytest.raises(ValueError):
        none_class = NoneClassUQ(
            population_model=population_model,
            parameters=parameters,
            bounds=bounds,
            grid_size=grid_size,
            kde=None,
        )
