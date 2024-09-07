"""
The classification framework is susceptible to systematic error through a variety of sources, including mismodeling in the population model or simulation noise in the 
"""
import numpy as np
from scipy.stats import gaussian_kde

def apply_none_class_uq(unnormalized_prob,inference_data, population_model, parameters, bounds, kde=gaussian_kde):
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
    # Tunable Hyperparameters: kde method, kde kernel (maybe), kde bandwidth, prior weight
    grid_size = int(1e3)
    kde = gaussian_kde
    kde_kwargs = {}


    # Calculate 1000x1000 grid in parameter space
    # should be grid_size**d elements
    grid, grid_mesh, grid_corners = calculate_square_grid_coordinates(gridsize, bounds)

    # Calculate bin centers
    # should be (grid_size-1)**d elements
    grid_centers, grid_mesh_centers, grid_centers = calculate_square_grid_centers(grid)
    #grid_centers = {p : (grid[p][1:] + grid[p][:-1])/2 for p in grid.keys()}
    #grid_mesh_centers = np.array(np.meshgrid(*list(grid_centers.values())))
    #grid_centers = np.array([ a.ravel() for a in grid_mesh_centers]).transpose()

    # Calculate grid volumes - Assume fixed grid
    # should be (grid_size-1)**d elements
    grid_volumnes = np.product(np.array([grid[p][1]-grid[p][0] for p in grid.keys()])) * np.ones(grid_centers.shape)

    # Train kde with tophat kernel and bandwidth of .4 on galactic model data
    pop_model_samples = np.vstack([ population_model.get_samples(class_name, parameters) for class_name in population_model.classes])
    pop_model_kde = kde(pop_model_samples,**kde_kwargs)
    pop_model_eval_centers = pop_model_kde(grid_centers)
    max_pop_model_eval_centers = np.amax(pop_model_eval_centers)

    # Assign p(phi|NONE) to bin centers
    
    none_class_pdf_centers_unnormed = (1. - pop_model_eval_centers/max_pop_model_eval_centers)
    none_class_pdf_normalization = np.sum(none_class_pdf_centers_unnormed * grid_volumes)
    none_class_pdf_centers = none_class_pdf_centers_unnormed / none_class_pdf_normalization

    # Calculate A such that it's normalized

    # Assign prior probability of 0.01

    # Undo prior weighting on unnormalized probability

    # Calculate new prior

    # Calculate likelihood of event in None class

    # Append to dictionary

    # reweight by new priors
    
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
            Numpy containing the meshed grid, shape [dimensions, grid_size, grid_size]
        
        grid_corners (numpy.array): 
            Numpy array containing the raveled grid corner coordinates, shape [grid_size*grid_size, dimensions]
    """
    grid = {p: np.linspace(bounds[p][0],bounds[p][1], grid_size) for p in bounds.keys()}
    grid_mesh = np.array(np.meshgrid(*list(grid.values())))
    grid_corners = np.array([ a.ravel() for a in grid_mesh]).transpose()
    return grid, grid_mesh, grid_corners

def calculate_square_grid_centers(grid):
    """
        Calculates the coordinates of the corners for a grid bounded in some domain in arbitrary dimension.

    Args:
        grid (dictionary): 
            dictionary containing the bin edges for each dimension, keyed by the parameter name
        
    Returns:
        grid (dictionary):
            Dictionary containing the grid edges in each dimension. Format: {parameter_key : np.array(size=grid_size)}

        grid_mesh (numpy.array):
            Numpy containing the meshed grid, shape [dimensions, grid_size, grid_size]
        
        grid_corners (numpy.array): 
            Numpy array containing the raveled grid corner coordinates, shape [grid_size*grid_size, dimensions]
    """
    grid_centers = {p : (grid[p][1:] + grid[p][:-1])/2 for p in grid.keys()}
    grid_mesh_centers = np.array(np.meshgrid(*list(grid_centers.values())))
    grid_centers = np.array([ a.ravel() for a in grid_mesh_centers]).transpose()
    return grid_centers, grid_mesh_centers, grid_centers
