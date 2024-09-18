"""
The classification framework is susceptible to systematic error through a variety of sources, including model assumptions (e.g. incomplete populations) or simulation noise in the tails of the distribution. The None class is constructed to have non-zero support in regions of low to no simulation support to reflect the epistemic uncertainty of the classifier.
"""
import numpy as np
from scipy.stats import gaussian_kde


class additiveUQ:
    def __init__(self):
        return

    def apply_uq(self, unnormalized_prob, inference_data, population_model, parameters):
        return unnormalized_prob


class NoneClassUQ(additiveUQ):
    # def __init__(self,bounds, grid_size=int(1e3), kde=gaussian_kde, kde_kwargs={"bandwidth":0.4}, population_model =None, parameters=None,none_class_weight = .01):
    def __init__(
        self,
        bounds,
        grid_size=int(1e3),
        kde=gaussian_kde,
        kde_kwargs={"bw_method": 0.4},
        population_model=None,
        parameters=None,
        none_class_weight=0.01,
    ):
        self.bounds = bounds
        self.grid_size = grid_size
        self.kde = kde
        self.none_class_weight = none_class_weight
        self.kde_kwargs = kde_kwargs
        self._build_grids()
        if population_model and parameters:
            self.parameters = parameters
            self.base_model_kde = self._train_base_model_kde(population_model)
        else:
            self.base_model_kde = None
            self.parameters = None

        return

    def _build_grids(self):
        """
            Calculate the square grid (corners and centers) bounded by bounds.
            Populates the quantities:

            1. self.grid  (Dictionary containing the grid edges in each dimension. Format: {parameter_key : np.array(size=grid_size)})

            2. self.grid_mesh (Numpy containing the meshed grid, shape [dimensions, grid_size, grid_size])
            3. self.grid_corners (Numpy array containing the raveled grid corner coordinates, shape [grid_size**dimensions, dimensions])
            4. self.grid _centers (Dictionary containing the grid centers in each dimension. Format: {parameter_key : np.array(size=grid_size-1)})
            5. self.grid_mesh_centers (umpy containing the meshed grid centers, shape [dimensions, grid_size-1, grid_size-1])
            6. self.grid_centers (Numpy array containing the raveled grid center coordinates, shape [(grid_size-1)**dimensions, dimensions])
            7. self.grid_volumes ( Numpy array volumes of every cell, shape [(grid_size-1)**dimensions])

        Args:
            None
        Returns:
            None
        """

        # Calculate 1000x1000 grid in parameter space
        # should be grid_size**d elements
        (
            self.grid,
            self.grid_mesh,
            self.grid_corners,
        ) = calculate_square_grid_coordinates(self.grid_size, self.bounds)

        # Calculate bin centers
        # should be (grid_size-1)**d elements
        (
            self.grid_centers,
            self.grid_mesh_centers,
            self.grid_centers_raveled,
        ) = calculate_square_grid_centers(self.grid)

        # Calculate grid volumes - Assume fixed grid
        # should be (grid_size-1)**d elements
        self.grid_volumnes = np.prod(
            np.array([self.grid[p][1] - self.grid[p][0] for p in self.grid.keys()])
        ) * np.ones(self.grid_centers_raveled.shape)
        return

    def _train_base_model_kde(self, population_model):
        pop_model_samples = np.vstack(
            [
                population_model.samples(class_name, self.parameters)
                for class_name in population_model.classes
            ]
        )
        base_model_kde = self.kde(pop_model_samples.T, **self.kde_kwargs)

        return base_model_kde

    def apply_uq(self, unnormalized_prob, inference_data, population_model, parameters):
        """
        Applies ``None'' class uncertainty quantification to the classification results.
        The method transforms the initial classification result, using the base population model.
        Works by defining an additional class to the set of classes, defined as the areas of parameter
        space poorly supported by the base population model.

        Args:
            unnormalized_prob (dictionary):
                Dictionary containing initial classification results, performed with the base population model.
            inference_data (popclass.InferenceData):
                popclass InferenceData object
            population_model (popclass.PopulationModel):
                popclass PopulationModel object
            parameters (list):
                Parameters to use for classification.
            bounds (dictionary):
                Dictionary containing the lower and upper bounds of the parameter space, with keys
                matching the supplied ``parameter'' list. Format: {key : [lower_bound, upper_bound]}

        Returns:
            Dictionary of classes in ``PopulationModel.classes()`` and associated
            probability, unnormalized, with the appended ``None'' class and associated probability.

        """
        # Train kde with tophat kernel and bandwidth of .4 on galactic model data
        if self.base_model_kde is None:
            self._train_base_model_kde(population_model)
        pop_model_eval_centers = self.base_model_kde(self.grid_centers_raveled)
        max_pop_model_eval_centers = np.amax(pop_model_eval_centers)

        # Assign p(phi|NONE) to bin centers

        none_class_pdf_centers_unnormed = (
            1.0 - pop_model_eval_centers / max_pop_model_eval_centers
        )
        none_class_pdf_normalization = np.sum(
            none_class_pdf_centers_unnormed * self.grid_volumes
        )
        none_class_pdf_centers = (
            none_class_pdf_centers_unnormed / none_class_pdf_normalization
        )

        # Undo prior weighting on unnormalized probability
        for class_name, value in unnormalized_prob.items():
            unnormalized_prob[class_name] = value * (1 - self.none_class_weight)

        # Calculate likelihood of event in None class (integrated posterior, unweighted)
        # evaluate map (where map_binned[param1][param2][...][param_N] are coords for the parameter order)
        # todo: reconcile the grid format with map_binned and bins. check parameter order. get posterior and prior from InferenceData object.

        def evaluate(posterior, parameters, map_binned, bins):
            grid_bins = {}
            for parameter in parameters:
                grid_bins[parameter] = (
                    np.clip(
                        np.digitize(x=posterior[parameter], bins=bins[parameter]),
                        1,
                        len(bins[parameter]),
                    )
                    - 1
                )
            bin_idx = tuple(tuple(grid_bins[parameter].T) for parameter in parameters)
            eval_ = map_binned[bin_idx]

            return eval_

        none_evaluated = (
            np.mean(evaluate(posterior, parameters, map_binned, bins) / prior_pdf)
            if map_binned is not None
            else 0.0
        )

        # Append to dictionary
        unnormalized_prob["None"] = self.none_class_weight * none_evaluated

        return unnormalized_prob


def calculate_square_grid_coordinates(grid_size, bounds):
    """
        Calculates the coordinates of the corners for a grid bounded in some domain in arbitrary dimension.

    Args:
        grid_size (int):
            number of bin edges per dimension

        bounds (dictionary):
            Dictionary containing the lower and upper bounds of the parameter space, with keys
            matching the supplied ``parameter'' list. Format: {key : [lower_bound, upper_bound]}
    Returns:
        grid (dictionary):
            Dictionary containing the grid edges in each dimension. Format: {parameter_key : np.array(size=grid_size)}

        grid_mesh (numpy.array):
            Numpy containing the meshed grid, shape [dimensions, grid_size, ...] with a total of dimensions + 1 along the first axis

        grid_corners (numpy.array):
            Numpy array containing the raveled grid corner coordinates, shape [grid_size**dimensions, dimensions]
    """
    grid = {
        p: np.linspace(bounds[p][0], bounds[p][1], grid_size) for p in bounds.keys()
    }
    grid_mesh = np.array(np.meshgrid(*list(grid.values())))
    grid_corners = np.array([a.ravel() for a in grid_mesh]).transpose()
    return grid, grid_mesh, grid_corners


def calculate_square_grid_centers(grid):
    """
        Calculates the coordinates of the corners for a grid bounded in some domain in arbitrary dimension.

    Args:
        grid (dictionary):
            dictionary containing the bin edges for each dimension, keyed by the parameter name

    Returns:
        grid_centers (dictionary):
            Dictionary containing the grid edges in each dimension. Format: {parameter_key : np.array(size=grid_size-1)}

        grid_mesh_centers (numpy.array):
            Numpy containing the meshed grid, shape [dimensions, grid_size-1, ...] with a total of dimensions + 1 along the first axis

        grid_centers_raveled (numpy.array):
            Numpy array containing the raveled grid corner coordinates, shape [(grid_size-1)***dimensions, dimensions]
    """
    grid_centers = {p: (grid[p][1:] + grid[p][:-1]) / 2 for p in grid.keys()}
    grid_mesh_centers = np.array(np.meshgrid(*list(grid_centers.values())))
    grid_centers_raveled = np.array([a.ravel() for a in grid_mesh_centers]).transpose()
    return grid_centers, grid_mesh_centers, grid_centers_raveled
