"""
Light visualization library.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

color_cycler = ['#EE7733', '#33BBEE', '#EE3377', '#009988', '#CC3311', '#0077BB', "BBBBBB"]
marker_cycler = ['o', 's', '^', 'v', '*']

def plot_population_model(PopulationModel, samples=False, kdes=True, bounds=None, N_bins=200, legend=False):

	"""
	 Represent the population samples and/or their KDEs in the defined parameter space for each individual class in a figure.

        Args:
            PopulationModel (class) - as defined in model.py, class containing the population samples, parameters, and a method for evaluating density

            samples (bool, optional) - flag for plotting all simulated samples in a scatter plot. Default: False.

            kdes (bool, optional) - flag for plotting the simulated population KDEs (according to the evaluate_density method specified in PopulationModel) constructed from samples. Default: True.

            bounds (array-like or None, optional) - pairs of upper and lower bounds for each parameter or None. If provided, should have a shape (N_dim, 2) where N_dim is equal to the number of parameters and has the same order. If bounds are not provided, they are automatically constructed to be 10% of the extent in samples beyond the minimum and maximum value found in samples for each parameter. Default: None.

            N_bins (int, optional) - Resolution of the grid to evaluate the KDEs on (if kdes=True). Default: 200.

            levels (int or array-like, optional) - Number and/or positions of contour lines. Corresponds to the 'levels' argument in plt.contour. Default: 5.

            legend (bool) - flag for including plot legend. Default: False.

        Returns
        -------
            fig, ax (matplotlib objects) - figure visualising population distributions in the specified parameter space
	"""

	parameters = PopulationModel.parameters()
	classes = PopulationModel.classes()
	ndim = len(parameters)

	fig, ax = plt.subplots()

	if bounds is None:
		bounds = np.array([[0,0] for i in range(ndim)])
		for counter, param in enumerate(samples[parameters]):
			param_min, param_max = np.min(samples[param]), np.max(samples[param])
			param_lower, param_upper = param_min - (param_max - param_min)/10, param_max + (param_max - param_min)/10
			bounds[counter] = [param_lower, param_upper]

	bins = np.linspace(bounds.T[:][0], bounds.T[:][1], N_bins+1).T
	bin_centers = (bins[:,1:]+bins[:,:-1])/2

	if(ndim==1):
		coords_eval = bin_centers
	elif(ndim==2):
		X, Y = np.meshgrid(bin_centers[0], bin_centers[1])
		coords_eval = np.vstack((X.ravel(),Y.ravel()))
	else:
		raise ValueError('Only plotting 1D and 2D distributions is currently supported.')

	for counter, class_name in enumerate(classes):

		samples = PopulationModel.samples(class_name=class_name, parameters=parameters)

		if samples:
			if(ndim==1): ax.hist(samples[parameters[0]], color=color_cycler[counter%7], alpha=0.5, density=True, label=f'{class_name} samples')
			else: ax.scatter(samples[parameters[0]], samples[parameters[1]], color=color_cycler[counter%7], marker=marker_cycler[counter%5], edgecolor='black', label=f'{class_name} samples')

		if kde:
			if(ndim==1):
				eval_ = PopulationModel.evaluate_density(class_name=class_name, parameters=parameters, points=coords_eval)
				ax.plot(coords_eval, eval_, color=color_cycler[counter%7], lw=2, label=f'{class_name} density estimate')
			else:
				eval_ = PopulationModel.evaluate_density(class_name=class_name, parameters=parameters, points=coords_eval)
				ax.contour(X, Y, eval_.reshape(np.shape(X)), colors=color_cycler[counter%7], lw=2, levels=levels, label=f'{class_name} density estimate')


	ax.set_xlim(bounds[0][0], bounds[0][1])
	ax.set_xlabel(f'{parameters[0]}')

	if(ndim==1):
		ax.set_ylabel('density')
	else:
		ax.set_ylim(bounds[1][0], bounds[1][1])
		ax.set_ylabel(f'{parameters[1]}')

	if(legend):
		ax.legend(loc='best', fontsize=20)

	return fig, ax

