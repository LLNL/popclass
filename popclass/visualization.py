"""
Light visualization library.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

color_cycler = [
    "#009988",
    "#EE3377",
    "#EE7733",
    "#33BBEE",
    "#CC3311",
    "#0077BB",
]

cmap_cycler = ["Greens", "RdPu", "Oranges", "Blues", "Reds", "Purples"]

marker_cycler = ["o", "^", "*", "s", "H"]


def get_bounds(PopulationModel, parameters):
    """
    Creates bounds on the basis of a PopulationModel and given parameters, if they are not specified by the user. Bounds are automatically constructed to be 10% of the extent in samples beyond the minimum and maximum value found in samples for each parameter.

    Args:
        PopulationModel (class) - as defined in model.py, class containing the population samples and parameters

        parameters (list of str) - a subset of parameters for visualization (must be found in PopulationModel.parameters)

    Returns
    -------
        bounds (numpy.ndarray) - pairs of upper and lower bounds for each parameter. Shape (N_dim, 2), where N_dim is equal to the number of parameters and has the same order.
    """

    ndim = len(parameters)
    classes = PopulationModel.classes
    bounds = np.array([[0.0, 0.0] for i in range(ndim)])

    samples_all = np.concatenate(
        (
            [
                PopulationModel.samples(class_name=class_name, parameters=parameters)
                for class_name in classes
            ]
        )
    )
    for counter, param in enumerate(parameters):
        param_min, param_max = np.min(samples_all[:, counter]), np.max(
            samples_all[:, counter]
        )
        param_lower, param_upper = (
            param_min - (param_max - param_min) / 10,
            param_max + (param_max - param_min) / 10,
        )
        bounds[counter] = param_lower, param_upper

    return bounds


def plot_population_model(
    PopulationModel,
    parameters=None,
    plot_samples=False,
    plot_kdes=True,
    bounds=None,
    N_bins=200,
    N_hist=40,
    levels=5,
    legend=False,
):
    """
     Represent the population samples and/or their KDEs in the defined parameter space for each individual class in a figure.

    Args:
        PopulationModel (class) - as defined in model.py, class containing the population samples, parameters, and a method for evaluating density

        parameters (list of str) - a subset of parameters of the population model to create a subspace for visualization (must be found in PopulationModel.parameters)

        plot_samples (bool, optional) - flag for plotting all simulated samples in a scatter plot. Default: False.

        plot_kdes (bool, optional) - flag for plotting the simulated population KDEs (according to the evaluate_density method specified in PopulationModel) constructed from samples. Default: True.

        bounds (array-like or None, optional) - pairs of upper and lower bounds for each parameter or None. If provided, should have a shape (N_dim, 2) where N_dim is equal to the number of parameters and has the same order. If bounds are not provided, they are automatically constructed to be 10% of the extent in samples beyond the minimum and maximum value found in samples for each parameter. Default: None.

        N_bins (int, optional) - Resolution of the grid to evaluate the KDEs on (if plot_kdes=True). Default: 200.

        N_hist (int, optional) - Resolution of the 1D histogram of samples (if plot_samples=True). Default: 40.

        levels (int or array-like, optional) - Number and/or positions of contour lines (for >1D KDE plotting). Corresponds to the 'levels' argument in plt.contour. Default: 5.

        legend (bool) - flag for including plot legend. Default: False.

    Returns
    -------
        fig, ax (matplotlib objects) - figure visualising population distributions in the specified parameter space
    """

    classes = PopulationModel.classes

    ndim = len(parameters)

    fig, ax = plt.subplots()

    if bounds is None:
        bounds = get_bounds(PopulationModel, parameters)

    bins = np.linspace(bounds.T[:][0], bounds.T[:][1], N_bins + 1).T
    bin_centers = (bins[:, 1:] + bins[:, :-1]) / 2

    if ndim == 1:
        coords_eval = bin_centers
    elif ndim == 2:
        X, Y = np.meshgrid(bin_centers[0], bin_centers[1])
        coords_eval = np.vstack((X.ravel(), Y.ravel()))
    else:
        raise ValueError(
            "Only plotting 1D and 2D distributions is currently supported."
        )

    for counter, class_name in enumerate(classes):
        samples = PopulationModel.samples(class_name=class_name, parameters=parameters)

        if plot_samples:
            if ndim == 1:
                ax.hist(
                    samples[:, 0],
                    color=color_cycler[counter % 6],
                    bins=np.linspace(bounds.T[:][0], bounds.T[:][1], N_hist + 1).T[0],
                    alpha=0.5,
                    density=True,
                    label=f"{class_name} samples",
                )
            else:
                ax.scatter(
                    samples[:, 0],
                    samples[:, 1],
                    color=color_cycler[counter % 6],
                    marker=marker_cycler[counter % 5],
                    edgecolor="black",
                    s=20,
                    label=f"{class_name} samples",
                )

        if plot_kdes:
            if ndim == 1:
                eval_ = PopulationModel.evaluate_density(
                    class_name=class_name,
                    parameters=parameters,
                    points=coords_eval.swapaxes(0, 1),
                )
                ax.plot(
                    coords_eval[0],
                    eval_,
                    color=color_cycler[counter % 6],
                    label=f"{class_name} density estimate",
                )
            else:
                eval_ = PopulationModel.evaluate_density(
                    class_name=class_name,
                    parameters=parameters,
                    points=coords_eval.swapaxes(0, 1),
                )
                ax.contour(
                    X,
                    Y,
                    eval_.reshape(np.shape(X)),
                    colors=color_cycler[counter % 6],
                    linewidths=2,
                    levels=levels,
                )
                legend_proxy = ax.plot(
                    bounds[0] - 1000,
                    bounds[1] - 1000,
                    color=color_cycler[counter % 6],
                    lw=2,
                    label=f"{class_name} density estimate",
                )

    ax.set_xlabel(f"{parameters[0]}")
    ax.set_xlim(bounds[0])
    if ndim == 1:
        ax.set_ylabel("density")
    else:
        ax.set_ylabel(f"{parameters[1]}")
        ax.set_ylim(bounds[1])

    if legend:
        ax.legend(loc="best", fontsize=10)

    return fig, ax


def plot_rel_prob_surfaces(
    PopulationModel,
    parameters=None,
    plot_samples=False,
    bounds=None,
    N_bins=1000,
    create_none_class=None,
    none_kde=None,
    none_kde_kwargs={},
):
    """
    Plots 2D relative probability surfaces (p(class | parameters, model)). A visualisation of probability the classifier would return, for points with exactly known parameters, of belonging to the given class, taking into account distributions and weights of all classes.

    Args:
        PopulationModel (class) - as defined in model.py, class containing the population samples, parameters, and a method for evaluating density

        parameters (list of str) - a subset of parameters of the population model to create a subspace for visualization (must be found in PopulationModel.parameters)

        plot_samples (bool, optional) - flag for overplotting all simulated samples belonging to a given class. Default: False.

        bounds (array-like or None, optional) - pairs of upper and lower bounds for each parameter or None. If provided, should have a shape (N_dim, 2) where N_dim is equal to the number of parameters and has the same order. If bounds are not provided, they are automatically constructed to be 10% of the extent in samples beyond the minimum and maximum value found in samples for each parameter. Default: None.

        N_bins (int, optional) - Resolution of the grid to evaluate the KDEs on. Default: 1000.

        create_none_class (popclass.NoneClassUQ-like or None, optional) - method to build the 2D None class probability distribution using the grid defined with bounds and N_bins. If None, only classes from PopulationModel are included in visualization. Default: None.

        none_kde (scipy.stats.gaussian_kde-like, optional) - method to evaluate the overall sample density in the process of building the None class. Passed as the ``kde'' argument when initializing the None class object. Default: None.

        none_kde_kwargs (dictionary) - extra arguments for evaluating the overall sample density in the process of building the None class. Passed as the ``kde_kwargs'' argument when initializing the None class object. Default: {}.


    Returns
    -------
        figs, axes (lists of matplotlib objects) - figures visualising relative probability surfaces in the specified parameter space (one for each class)

    """

    classes = PopulationModel.classes

    ndim = len(parameters)
    if ndim != 2:
        raise ValueError(
            "Only 2-parameter input is currently supported for plotting relative probability surfaces."
        )
    else:
        if bounds is None:
            bounds = get_bounds(PopulationModel, parameters)

        bins = np.linspace(bounds.T[:][0], bounds.T[:][1], N_bins + 1).T
        bin_centers = (bins[:, 1:] + bins[:, :-1]) / 2

        X, Y = np.meshgrid(bin_centers[0], bin_centers[1])
        coords_eval = np.vstack((X.ravel(), Y.ravel()))

        maps_2d = []
        weights = []

        for class_name in classes:
            density_eval = PopulationModel.evaluate_density(
                class_name=class_name,
                parameters=parameters,
                points=coords_eval.swapaxes(0, 1),
            )
            map_2d = np.reshape(density_eval, X.shape)

            weight = PopulationModel.class_weight(class_name)

            maps_2d.append(map_2d)
            weights.append(weight)

        if create_none_class:
            bounds_dict = {}
            for counter, parameter in enumerate(parameters):
                bounds_dict[parameter] = bounds[counter]

            none_class = create_none_class(
                bounds=bounds_dict,
                grid_size=N_bins + 1,
                population_model=PopulationModel,
                parameters=parameters,
                kde=none_kde,
                kde_kwargs=none_kde_kwargs,
            )

            classes.append("None")
            map_none = none_class.none_pdf_binned

            maps_2d.append(map_none)
            weights.append(
                none_class.none_class_weight / (1 - none_class.none_class_weight)
            )

        maps_2d, weights = np.array(maps_2d), np.array(weights)

        weighted_cmaps = (maps_2d.T * weights).T
        colormaps_normed = weighted_cmaps / np.sum(weighted_cmaps, axis=0)

        figs, axes = [], []
        for counter, class_name in enumerate(classes):
            fig, ax = plt.subplots()

            if class_name != "None":
                cmap = cmap_cycler[counter % 6]

                if plot_samples:
                    samples = PopulationModel.samples(
                        class_name=class_name, parameters=parameters
                    )
                    ax.scatter(
                        samples[:, 0],
                        samples[:, 1],
                        color=color_cycler[counter % 6],
                        marker=marker_cycler[counter % 5],
                        edgecolor="black",
                        s=20,
                        label=f"{class_name} samples",
                    )
                    ax.legend()
            else:
                cmap = "Greys"

            im = ax.imshow(
                colormaps_normed[counter],
                origin="lower",
                extent=[bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]],
                cmap=cmap,
                vmin=0.0,
                vmax=1.0,
            )

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cb = fig.colorbar(im, cax=cax, orientation="vertical")

            ax.set_xlabel(f"{parameters[0]}")
            ax.set_xlim(bounds[0])
            ax.set_ylabel(f"{parameters[1]}")
            ax.set_ylim(bounds[1])
            cb.set_label(f"p({class_name} | " + r"$\phi, \mathcal{G} )$")

            figs.append(fig)
            axes.append(ax)

        return figs, axes
