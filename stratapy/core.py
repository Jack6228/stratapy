"""
This module contains the main functions or classes within stratapy. It includes the LogObject class, which is used to create and manipulate stratigraphic logs, as well as methods for loading files, complex plotting, and customising assets. 

The module is imported through ``__init__.py``, so users can access its functionality via ``import stratapy as sp``.
"""

from .setup import formatting, config
from numpy import sort, ndarray, asarray
from os import path, listdir

def list_examples(return_list : bool = False):
    """
    Returns a list of all the .csv example files built into stratapy. 

    These files can be use by calling ``sp.load('examples.XXX.csv')``.

    Parameters
    ----------
    return_list : bool, optional
        If True, the list of example files will be returned as a list of strings. If False, the list will be printed to the console. Default is False.

    Returns
    ----------
    list
        A list of the example files available in stratapy, if ``return_list`` is True. Otherwise, the list is printed to the console and None is returned.

    Examples
    ----------
    >>> # To use the `tutorial.csv` example file, call:
    >>> log = sp.load('examples.tutorial.csv')
    """
    files = [f for f in listdir(path.join(config.direc, 'assets/examples')) if f.endswith('.csv')]
    if return_list:
        return files
    print("Example files:")
    for f in files:
        print(f" - {f}")

class LogObject:
    """
    This class represents a stratigraphic log and contains methods for plotting and customising the log. It is created from the ``sp.load()`` function, which loads data from a CSV file and returns an instance of the LogObject class.
    
    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The axes object on which the log is plotted. Created only after the ``plot()`` method is called.
    fig : matplotlib.figure.Figure
        The figure object on which the log is plotted. Created only after the ``plot()`` method is called.
    leg : matplotlib.legend.Legend
        The legend object for the log. Created only after the ``plot()`` method is called.

    Methods
    -------
    plot()
        Creates a stratigraphic plot based on the loaded data and specified parameters.
    save()
        Saves the current figure to a file with the specified filename and format.
    add_chronostratigraphy()
        Adds chronostrarigraphy to the log if the y-axis is set to 'age'. Available once ``plot()`` has been called.
    add_samples()
        Plots scatter points on the left side of the log, representing sample positions. Available once ``plot()`` has been called.
    add_twin_axis()
        Adds a secondary y-axis to the figure, for example, to compare relative distance to ground level, or sea level. Available once ``plot()`` has been called.
    add_labels()
        User can provide a list of strings which will be displayed to the right of each unit - the length of the list must match the number of units otherwise nothing will happen. Available once ``plot()`` has been called.
    add_trends()
        Draws a triangle in the between two y-axis bounds on the log. By default, it will add space between the log and any elements in the features column, but can alternatively be passed an x-coordinate to place the triangle at. Available once ``plot()`` has been called.
    """
        
    def __init__(self, **kwargs):
        """
        init function to set up the LogObject with the provided data and parameters. This is called by the ``sp.load()`` function when creating a new LogObject instance.
        """
        # Store copies of original data which are not to be modified by class methods  - marking them as the immutable source
        self.df = kwargs.get('df')
        self.original_df = self.df.copy()
        
        # Keep non-data attributes as they are
        self.y_mode = kwargs.get('y_mode')
        self.lithologies = kwargs.get('lithologies')
        self.minerals_list = kwargs.get('minerals_list')
        self.features = kwargs.get('features')
        self.contact_types = kwargs.get('contact_types')
        self.direc = kwargs.get('direc')
        self.user_direc = kwargs.get('user_direc')
        self.x_ticks_dict = kwargs.get('x_ticks_dict')
        self.grain_brackets = kwargs.get('grain_brackets')

    def plot(self, fig=None, ax=None, display_mode='default', feature_mode=None, unit_borders=True, legend_loc='right', legend_columns=1, legend_border=True, figsize=None, dpi=150, ppi=400, x_label='', x_axis=True, y_label=None, y_axis_unit='', spines=False, mineral_size=1, feature_size=1, xmax=None, legend_titles=['Lithologies', 'Minerals', 'Sedimentary Structures', 'Palaeontological Features', 'Tectonic Structures', 'Bed Contacts', 'Sample Indicators'], legend=True, legend_kwargs={}) -> tuple:
        """
        Creates a stratigraphic plot based on the loaded data and specified parameters. 
        
        No arguments are required to run this function, but has many optional parameters for customisation including figure size, resolution, legend location, and more - see the documentation for more details.

        Parameters
        ----------
        fig : matplotlib.figure.Figure, optional
            The figure object to plot on. If None, a new figure will be created. (Both a fig and ax must be provided to use a pre-existing figure and axes.)
        ax : matplotlib.axes.Axes, optional
            The axes object to plot on. If None, a new axes will be created. (Both a fig and ax must be provided to use a pre-existing figure and axes.)
        display_mode : str, optional
            The display mode for the plot. Options are 'default', 'grainsize', 'log'. 'default' fills in each unit with the pattern or fill, 'column' creates a column of filled rectangles, with the rest of each unit only having its outline shown, 'log' only shows a rectangle for each unit, ignoring grain sizes completely. Default is 'default'.
        feature_mode : str, optional
            How features, minerals and lenses are displayed on the plot. Options are 'deafult', 'semi-merge', 'merge' or 'off'. 'default' displays all features, minerals, and lenses in a column on the right of the log, while 'semi-merge' displays features in that column, but minerals and lenses are shown within a units lithology. 'merge' displays all features, minerals, and lenses within the units lithology. Default is 'default'. 'off' can be used when no features, minerals, or lenses are to be displayed in the log itself, but they are wanted in the legend. Note: if display_mode is set to 'log', feature_mode changes to 'merge' unless 'default' or another mode is explicitly provided.
        unit_borders : bool, optional
            If True, borders will be drawn around each unit in the log. Default is True.
        legend_loc : str, optional
            The location of the legend in the plot: 'top', 'bottom', 'right', 'left'. Default is 'right'.
        legend_columns : int, optional
            The number of columns in the legend. Default is 1.
        legend_border : bool, optional
            If True, a border will be drawn around the legend. Default is False.
        figsize : tuple, optional
            The size of the figure in inches (width, height). Default is (10, 10). Does not include the legend. Ignored if ``fig`` is provided.
        dpi : int, optional 
            The resolution of the figure in dots per inch. Default is 150. Higher dpi values produce higher quality images but increase file size and rendering time. You may wish to use lower values (e.g. 100) when creating or fine-tuning figures, and increase this (e.g. 300-500) when saving the final figure for publication or other use.
        ppi : int, optional 
            The resolution of the image-based lithological patterns in units, in pixels per inch. Default is 400. A larger ppi will cause patterns to appear more zoomed out, and will increase the rendering time of the plot.
        x_label : str, optional
            The label for the x-axis. Default is an empty string.
        x_axis : bool, optional
            If False, the x-axis (ticks, labels, spine, grainsize brackets) will not be displayed. Default is True.
        y_label : str, optional
            The label for the y-axis. Defaults to 'Age', 'Depth', or 'Height' depending on the input data. If set to an empty string (''), it will not display a label.
        y_axis_unit : str, optional
            The unit for the y-axis. Default is an empty string which uses 'Ma' for age inputs and 'm' for height/depth inputs. If ``y_label`` is set to an empty string, this will not display a unit label.
        spines : bool, optional 
            If True, upper and right spines will be shown on the plot. Default is False.
        mineral_size : float, optional
            Scaling factor for the size of mineral symbols in the plot. Default is 1.
        feature_size : float, optional
            Scaling factor for the size of features in the plot. Default is 1.
        legend_titles : list, optional
            The titles for the legend sections. Default is ['Lithologies', 'Minerals', 'Structures', 'Fossils', 'Bed Contacts']. Note: the order of display of the legend is fixed (lithologies, then minerals, etc.), only names can be changed.
        legend_kwargs : dict, optional
            Additional keyword arguments to pass to the legend function, such as ``frameon``, etc. Default is an empty dictionary. Note: this will be overriden by the ``legend_loc``, ``legend_columns``, and ``legend_border`` parameters, if they are provided.
        legend : bool, optional
            If False, no legend will be displayed. Default is True. Note: the ``sp.standalone_legend()`` function can be used to create a separate legend figure if no legend is wanted on the main plot.

        Returns
        ----------
        None

        Examples
        ----------
        >>> import stratapy as sp
        >>> # Load data from a CSV file
        >>> log = sp.load('path/to/your/data.csv')
        >>> # Create the figure
        >>> log.plot()
        """ 
        from .utils import parse_params
        # Create copy to allow repeated use of methods
        self.df = self.original_df.copy()
        
        # Verify local parameters, excluding parse_params
        local_vars = {k: v for k, v in locals().items() if k != 'parse_params'}
        params = parse_params(local_vars)

        # Load the PlottingHelp class and initialise parameters to pass to it
        from .plotting_help import PlottingHelp
        x_ticks, x_tick_labels = list(self.x_ticks_dict.values()), list(self.x_ticks_dict.keys())
        # For the labels, remove any punctuation in [*, ^, &, _, £, $] to allow non-unique labels
        x_tick_labels = [label.replace('*', '').replace('^', '').replace('&', '').replace('_', '').replace('£', '').replace('$', '') for label in x_tick_labels]

        # In case of replotting, reset chrono_ax and twin_ax
        self.chrono_ax = None
        self.twin_ax = None

        # If override_ylims is a variable of self (set in multi-figure methods), use it, otherwise use None
        override_ylims = getattr(self, 'override_ylims', None)
        if params['legend'] == False:
            share_legend = True
        else:
            share_legend = getattr(self, 'share_legend', None)

        # Initialise the helper class
        helper = PlottingHelp(
            self,
            params['display_mode'],
            params['feature_mode'],
            params['unit_borders'], 
            params['legend_loc'],
            params['legend_columns'],
            params['legend_border'],
            formatting.fontsizes,
            params['figsize'],
            params['dpi'],
            params['ppi'],
            max(150, int(params['dpi']/3)),
            params['x_label'],
            params['x_axis'],
            params['y_label'],
            params['y_axis_unit'],
            params['spines'],
            params['mineral_size'],
            params['feature_size']/2, # scales so default value is 1
            params['xmax'],
            x_ticks,
            x_tick_labels,
            params['legend_titles'],
            params['legend_kwargs'],
            self.grain_brackets
        )

        from .plot import create_log
        # Call the function to create the log and save useful attributes for user access
        self.fig, self.ax, self.leg, self.helper = create_log(helper, params['fig'], params['ax'], override_ylims, share_legend)

    def add_chronostratigraphy(self, ranks_to_display : list = [0,1,2,3,4,5], width_ratio : float = 0.2, spacing : float = 0.02) -> None:
        """
        Creates a new axis to the left of the log, showing the chronostratigraphy of the stratigraphic column. Only works if the y-axis is set to 'age'.

        If a more customised chronostratigraphy is desired (for example on more complex subplot layouts, or on a depth/age-based log), you can manually call the `sp.chronostratigraphy()` function to add chronostratigraphy to a pre-existing axis. More information and examples of this can be found in the `documentation <https://stratapy.readthedocs.io/en/latest/customisation/additional_elements/chronostratigraphy.html>`_.

        Parameters
        ----------
        ranks_to_display : array-like, optional
            A list of the ranks to display in the chronostratigraphy axis. Default is [0, 1, 2, 3, 4, 5], which corresponds to the six main ranks (e.g., Super-eonothem, Eonothem, Erathem, System, Series, Stage).
        width_ratio : float, optional
            The width ratio between the chronostratigraphy axis and the main log axis. Default is 0.2.
        spacing : float, optional
            The spacing between the chronostratigraphy axis and the main log axis, as a fraction of the main axis width. Default is 0.02 (2% of the main axis width).

        Returns
        ----------
        None

        Notes
        ----------
        This method can only be called after the ``plot()`` method has been called, and only on logs with the y-axis set to 'age'.
        """
        if self.y_mode != 'age':
            print("Chronostratigraphy can only be plotted on a log directly if the y-axis is age. Alternatively, you can manually call ``sp.chronostratigraphy()`` to add chronostratigraphy to any axis.")
            return

        # Use add_axes to add chronostratigraphy axis 
        box = self.ax.get_position()
        width = box.width
        height = box.height
        left = box.x0 - (width * (width_ratio + spacing))
        bottom = box.y0
        chrono_ax = self.fig.add_axes([left, bottom, width * width_ratio, height])
        
        # Copy the y-axis label and ticks to the new axis
        chrono_ax.set_ylabel(self.ax.get_ylabel(), fontsize=formatting.fontsizes['y_axis_label'])
        yticks, yticklabels = self.ax.get_yticks().copy(), self.ax.get_yticklabels().copy()
        chrono_ax.set_yticks(yticks)
        chrono_ax.set_yticklabels(yticklabels, fontsize=formatting.fontsizes['y_tick_labels'])
        chrono_ax.set_xticks([])
        # Then remove them from the main axis
        if self.twin_ax is None:
            self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
            self.ax.set_ylabel('')

        age_lims = self.ax.get_ylim()
        # Sort smallest to largest
        age_lims = sorted(self.helper.y_limits)   
        chrono_ax = chronostratigraphy(age_lims[0], age_lims[1], self.fig, chrono_ax, ranks_to_display, unit=self.helper.y_axis_unit)
        chrono_ax.set_ylim(age_lims[1], age_lims[0])  # Reverse the y-axis to match the main axis

        self.chrono_ax = chrono_ax  # Store the axis for later use

    def add_samples(self, samples : list = [], label : str = None, x : float = -0.25, scatter_kwargs={}) -> None:
        """
        Plots scatter points on a log at the desired x position, deafulting to the left of the y-axis. 
        
        Keyword arguments can be passed to the scatter function to customise the appearance of the points, such as color, marker style, and size. 
        
        This function is designed such that it can be called multiple times to add many points to the log under one legend entry, and repeated for different points, or it can be called separately for each point with a unique label to be explicitly added to the legend.

        Parameters
        ----------
        samples : list
            A list of y-values (numeric) to plot on the log.
        label : str, optional
            The label for the sample points to be displayed in the legend. If None, the points will be plotted without a legend entry. Default is None.
        x : float, optional
            The x-coordinate on the log where the samples will be plotted. Default is -0.25, which places them just to the left of the y-axis.
        scatter_kwargs : dict, optional
            Additional keyword arguments to pass to ax.scatter, such as ``color``, ``marker``, ``s``, etc. Default is an empty dictionary. Warning: no validation is performed, so an error will be returned if any kwargs are not valid for ax.scatter; see `matplotlib.axes.Axes.scatter <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html>`_ or examples below.

        Returns
        ----------
        None

        Notes
        ----------
        Any scatter kwargs provided are passed directly to the ``ax.scatter()`` function without validation; ensure that the kwargs are valid for that function.

        Examples
        ----------
        >>> # Another example with default scatter kwargs   
        >>> log.add_samples(samples=[-20, -15, -10, -5, 0, 5, 10])

        This will plot black circles at the specified y-values on the left side of the log, using the default scatter appearance (black color, circle marker, size 5).

        >>> # Assuming ``log`` has already been created and plotted 
        >>> log.add_samples(samples=[50, 53, 57.5], label='Rock Samples', scatter_kwargs={'color': 'red', 'marker': 'x', 's': 50})

        This will plot red crosses at the specified y-values (50, 53, 57.5) on the left side of the log, with a size of 50, and add a similar marker to the 'Sample Indicators' section of the legend with the label 'Rock Samples'.
        """
        # Set default kwargs if not provided
        scatter_kwargs.setdefault('color', 'k')
        scatter_kwargs.setdefault('s', 50)
        scatter_kwargs.setdefault('marker', 'o')
        scatter_kwargs.setdefault('edgecolor', scatter_kwargs['color'])  # Default edgecolor to color if not provided

        helper = self.helper  # Access the helper for legend creation   
        helper.added_samples_list = {} if not hasattr(helper, 'added_samples_list') else helper.added_samples_list  # Initialise the added_samples_list if it doesn't exist

        # Plot each sample if it is within the plot limits and add legend entries if needed
        ylims = sort(self.ax.get_ylim())
        for k in samples:
            # Ensure value is valid and within axis extent
            if isinstance(k, (int, float)) and ylims[0] <= k <= ylims[1]:
                # Plot the point
                self.ax.scatter(x, k, clip_on=False, **scatter_kwargs)
                # Add legend entry
                if label is not None:
                    # Add this point to the legend with tuple of (fill, edge, shape)
                    helper.added_samples_list[label] = (scatter_kwargs['color'], scatter_kwargs['edgecolor'], scatter_kwargs['marker'])

        # Remove and recreate the legend only if one is currently attached
        if self.leg is not None:
            self.leg.remove()
            self.leg = helper.make_legend(self.fig, helper.lithology_legend)

    def add_twin_axis(self, offset : float = 0, limits = None, label='', spacing : float = 80) -> None:
        """
        Adds a secondary y-axis to the left of the existing axis with an offset applied or a custom axis range. 

        Parameters
        ----------
        offset : float, optional
            The offset to apply to the y-axis limits; new axis will be plotted with this offset applied to the existing y-axis limits. Default is 0, which will not add a new axis.
        limits : list, optional
            Instead of a fixed offset, the lower and upper limits of the new y-axis can be provided as a list of two numeric values [lower_limit, upper_limit]. Overrides the ``offset`` parameter, if both are provided.
        ylabel : str, optional
            The label for the new y-axis. Default is blank ('').
        spacing : float, optional
            The spacing between the new y-axis and the existing y-axis, in points. Default is 80. Enables more control over the positioning of the new twin axis.

        Returns
        ----------
        None 
        """
        # If a chronostratigraphy axis has been added, use that axis instead of the main axis
        if self.chrono_ax is not None:
            twin1 = self.chrono_ax.twinx()
        else:
            twin1 = self.ax.twinx()
        
        # Ensure offset is float
        if not isinstance(offset, (int, float)):
            print("Warning: Offset must be a numeric value (int or float). No twin axis will be added.")
            return
        # Ensure limits is array-like of two floats and use that instead of offset if provided
        if limits is not None:
            if isinstance(limits, (list, tuple, ndarray)) and len(limits) == 2 and all(isinstance(i, (int, float)) for i in limits):
                offset = None  # Disable offset
            else:
                print("Warning: Limits must be a list or array-like of two numeric values (int or float). Using offset instead.")
        # If both provided, use limits, else create limits from offset
        if offset is not None and limits is None:
            limits = [x + offset for x in self.ax.get_ylim()]

        # Move the new axis spine further left, outside the existing y-axis
        twin1.spines["left"].set_position(("outward", spacing))
        twin1.yaxis.set_label_position('left')
        twin1.yaxis.tick_left()
        # Hide the right spine of the twin axis
        twin1.spines["right"].set_visible(False)
        twin1.spines["top"].set_visible(False)
        # Set limits and label for the new axis
        twin1.set(ylim=limits, ylabel=label)
        # Set tick and axis label fontisze
        twin1.yaxis.label.set_size(formatting.fontsizes['y_axis_label'])
        twin1.tick_params(axis='y', labelsize=formatting.fontsizes['y_tick_labels'])
        self.twin_ax = twin1  # Store the axis for later use

    def add_labels(self, labels : list, fontsize : float = 12, padding : float = 5) -> None:
        """
        Enables the user to provide a list of strings which will be displayed to the right of each unit - the length of the list must match the number of units.

        Parameters
        ----------
        labels : list
            Strings to be displayed next to each unit in the log.
        fontsize : float, optional
            The font size of the labels. Default is 12.
        padding : float, optional
            The padding between the labels and the units, as a percentage of the x-axis range. Default is 5 (5% of the x-axis range). 
            
        Returns
        ----------
        None

        Notes
        ----------
        Labels are plotted to the right of each unit, at the middle of the unit's height. If the log is in 'log' display mode, labels are plotted to the right of the x-axis with padding applied.
        """
        # Ensure valid input
        if len(labels) != len(self.df):
            print(f"Warning: The number of labels ({len(labels)}) does not match the number of units ({len(self.df)}). No labels will be added.")
            return
        padding = 1 + padding / 100

        # Add labels for each unit
        for i, label in enumerate(labels):
            # Get the y position of the unit
            y_pos = self.df['height/age'].iloc[i] + self.df['thickness'].iloc[i] / 2
            if self.helper.display_mode == 'log':
                # Set the x position to right of the y-axis
                self.ax.text(self.ax.get_xlim()[1] * padding, y_pos, label, ha='left', va='center', fontsize=fontsize, color='black', clip_on=False)
            else:
                # Get the x position of the unit (middle of grain sizes + 0.5)
                x_pos = max(self.df['bottom_grain'].iloc[i], self.df['top_grain'].iloc[i]) + 0.3
                if self.helper.display_mode == 'grainsize':
                    x_pos = max(self.helper.lithology_column_thickness + 1, x_pos)
                else:
                    x_pos = max(1, x_pos)  # Ensure x_pos is at least 1
                # Add the text to the plot
                self.ax.text(x_pos, y_pos, label, ha='left', va='center', fontsize=fontsize, color='black', clip_on=True)

    def add_trends(self, bounds : list, x = None, triangle_type : str = 'isosceles', fill_color : str = 'black', edge_color : str = 'black', linewidth : float = 1.0) -> None:
        """
        Draws a triangle in the between two y-axis bounds on the log. By default, it will place the trend to the right of the log, but specifying an x-coordinate will place the triangle at that position instead (either a numeric value or an x-tick label).

        Multiple triangles can be added by calling this method multiple times with different bounds.

        Note, the ``xmax`` parameter in the ``plot()`` method can be used to add extra space between a log and the features column where trends can be fit in.

        Parameters
        ----------
        bounds : list
            A list of two numeric values representing the y-axis bounds between which the triangle will be drawn. The triangle will point from the first value to the second value.
        x : float or str, optional
            The x-coordinate where the triangle will be placed. If a string is provided, it should match one of the x-tick labels in the log. If None, the triangle will be placed to the right of the grain size axis. Default is None.
        triangle_type : str, optional
            The type of triangle to draw. Options are 'isosceles' or 'right-angled', or variations thereof. Default is 'isosceles'.
        fill_color : str, optional
            The fill color of the triangle. Default is 'black'.
        edge_color : str, optional
            The edge color of the triangle. Default is 'black'.
        linewidth : float, optional
            The line width of the triangle's edge. Default is 1.0.

        Returns
        ----------
        None

        Examples
        ----------
        >>> import stratapy as sp
        >>> log = sp.load('./examples.sedimentary.csv')
        >>> log.plot(xmax=7.5)
        >>> log.add_trends([3,2.3], x=7.3)
        """
        from matplotlib.patches import Polygon
        # from .utils import adjust_wspace
        if len(bounds) != 2:
            print("Warning: Please provide exactly two y-axis bounds to draw the triangle between.")
            return
        y_bottom, y_top = bounds[0], bounds[1]

        if x is not None:
            if isinstance(x, (str)):
                if x in self.x_ticks_dict:
                    x_mid = self.x_ticks_dict[x] + self.helper.lithology_column_thickness
                    print(f"Placing triangle at x-tick label '{x}' with value {x_mid}.")
            elif isinstance(x, (int, float)):
                x_mid = x
            else:
                print(f"Warning: x-tick label '{x}' not found in x_ticks_dict, use a numeric value or a valid label instead.")
                x_mid = self.helper.x_ticks[-1]
        else:
            x_mid = self.helper.xmax + 0.5*self.helper.spacing if self.helper.display_mode == 'log' else self.helper.xmax + .5
            # Add spacing to fit this between log and features - if log mode, use an adjust x-value of the xmax itself since padding is less than other display modes
            # if self.helper.display_mode == 'log':
            #     insrt, wspace = self.helper.xmax + 0.5*self.helper.spacing, self.helper.max_feature_width
            # else:
            #     insrt, wspace = self.helper.xmax + 2*self.helper.spacing, self.helper.max_feature_width
            # adjust_wspace(self.ax, insrt, wspace)
            # x_mid = insrt + wspace / 2
        x_left, x_right = x_mid - self.helper.max_feature_width / 2, x_mid + self.helper.max_feature_width / 2
            # x_left, x_right = self.helper.max_x_grain + 0.5, self.helper.max_x_grain + 0.5 + self.helper.max_feature_width
        
        triangles = ['isosceles', 'right-angled', 'ra', 'iso', 'isos', 'right', 'right angled', 'rightangled', 'right angle', 'rt', 'rightangle', 'r', 'i', 'is', 'r-a']
        if triangle_type.lower() not in triangles:
            print(f"Warning: Triangle type '{triangle_type}' not recognised, using 'isosceles' instead.")
            triangle_type = 'isosceles'
        if triangle_type.lower() in ['right-angled', 'ra', 'right', 'right angled', 'rightangled', 'right angle', 'rt', 'rightangle', 'r', 'r-a']:
            triangle_coords = [(x_left, y_bottom), (x_left, y_top), (x_right, y_bottom)]
        elif triangle_type.lower() in ['isosceles', 'iso', 'isos', 'i']:
            x_middle = (x_left + x_right) / 2
            triangle_coords = [(x_left, y_bottom), (x_right, y_bottom), (x_middle, y_top)]

        triangle = Polygon(triangle_coords, closed=True, facecolor=fill_color, edgecolor=edge_color, linewidth=linewidth)
        self.ax.add_patch(triangle)

    def save(self, filename='./stratapy_output', transparent=False) -> None:
        """
        Saves the current figure to a file. The filename should include the desired file extension (e.g., .png, .jpg, .pdf, .svg). If no extension is provided, it defaults to .png. 

        Parameters
        ----------
        filename : str, optional
            The name of the file to save the figure to. Default is './stratapy_output.png'. 
        transparent : bool, optional
            If True, the background of the saved figure will be transparent. Default is False.

        Returns
        ----------
        None

        Notes
        ----------
        Saving time increases with figure complexity and quality, so it is recommended to use a lower dpi (e.g., 100) during development and increase it (e.g., 300-500) for final figures. dpi is set when the ``plot()`` method of the individual logs is called.

        Other *matplotlib* backends like 'Cairo' or 'Agg' can be used to speed up saving figures. 
        
        >>> from matplotlib import use
        >>> use('Cairo')  # or use('Agg')

        These may require additional installation of matplotlib dependencies, but can significantly reduce saving time for complex figures.
        """
        from matplotlib.pyplot import savefig, close

        # Ensure the fig_filename has the correct extension
        valid_extensions = self.fig.canvas.get_supported_filetypes().keys()
        # Check if filename ends with any valid extension
        if not any(filename.endswith(f'.{ext}') for ext in valid_extensions):
            print(f"Extension '{filename.split('.')[-1]}' not supported, saving as PNG instead.")
            filename += '.png'
        
        # Save the figure
        savefig(filename, dpi=self.helper.dpi, transparent=transparent, bbox_inches='tight')
        print(f"Figure saved to {filename}")
        close()  # Close the figure to free up memory

class MultiLogObject:
    """
    A class to handle and provide methods for multiple logs plotted on the same figure, such as a shared legend or saving the figure. When ``correlated_logs()`` or ``multi_fig()``` are called, this class is return to provide figure saving functionality, and access to the figure and axes objects, as well as the individual logs and legend.
    
    Attributes
    ----------
    fig : matplotlib.figure.Figure
        The figure object containing the plotted logs.
    axes : list of matplotlib.axes.Axes
        A list of axes objects for each log plotted on the figure.
    logs : list of LogObject
        A list of LogObject instances representing each log plotted on the figure.
    leg : matplotlib.legend.Legend
        The legend object for the figure, which can be shared across multiple logs if desired.

    Methods
    ----------
    save(filename='./stratapy_output') -> None
        Saves the figure to a file.
    """

    def __init__(self, fig, axes, logs, leg):
        """
        Initialises with the provided variables
        """
        self.fig = fig
        self.axes = axes
        self.logs = logs
        self.leg = leg

    def save(self, filename='./stratapy_output', transparent=False) -> None:
        """
        Saves the current figure to a file. The filename should include the desired file extension (e.g., .png, .jpg, .pdf, .svg). If no extension is provided, it defaults to .png.

        Parameters
        ----------
        filename : str, optional
            The name of the file to save the figure to. Default is './stratapy_output.png'.
        transparent : bool, optional
            If True, the background of the saved figure will be transparent. Default is False. 

        Returns
        ----------
        None

        Notes
        ----------
        Saving time increases with figure complexity and quality, so it is recommended to use a lower dpi (e.g., 100) during development and increase it (e.g., 300-500) for final figures. dpi is set when the ``plot()`` method of the individual logs is called.
        
        Other *matplotlib* backends like 'Cairo' or 'Agg' can be used to speed up saving figures. 
        
        >>> from matplotlib import use
        >>> use('Cairo')  # or use('Agg')

        These may require additional installation of matplotlib dependencies, but can significantly reduce saving time for complex figures.
        """
        from matplotlib.pyplot import savefig, close
        
        # Ensure the fig_filename has the correct extension
        valid_extensions = self.fig.canvas.get_supported_filetypes().keys()
        # Check if filename ends with any valid extension
        if not any(filename.endswith(f'.{ext}') for ext in valid_extensions):
            print(f"Extension '{filename.split('.')[-1]}' not supported, saving as PNG instead.")
            filename += '.png'
        
        # Save the figure
        savefig(filename, dpi=self.logs[0].helper.dpi, transparent=transparent, bbox_inches='tight')
        print(f"Figure saved to {filename}")
        close()  # Close the figure to free up memory

def standalone_legend(files, dpi=300, transparent=True, filename='legend.png', legend_loc='right', legend_columns=1, legend_border=False, legend_kwargs={}):
    """
    This function will create only the legend of the logs provided in ``files``, which can be used when a legend is wanted without plotting the full log, or when a shared legend is wanted across multiple logs plotted separately, if not using the ``correlated_logs()`` or ``multi_fig()`` functions which automatically share legends.
    
    By passing custom input files, this function can also be used to create a legend for a non-stratapy plot, or to create a more customised legend.

    Parameters
    ----------
    files : list
        A list of file paths to the stratigraphic data files to be included in the legend. Must be files that can be read by the ``load()`` function.
    dpi : int, optional
        The resolution of the figure in dots per inch. Default is 300.
    transparent : bool, optional
        If True, the background of the saved legend will be transparent. Default is True.
    filename : str, optional
        The name of the file to save the legend to. Default is 'legend.png'. The file extension determines the format of the saved legend.
    legend_loc : str, optional
        The location of the legend on the figure. Default is 'right'. See ``matplotlib.legend.Legend`` documentation for more details on available options.
    legend_columns : int, optional
        The number of columns to use in the legend. Default is 1.
    legend_border : bool, optional
        If True, a border will be drawn around the legend. Default is False.
    legend_kwargs : dict, optional
        Additional keyword arguments to pass to the legend function, such as ``frameon``, etc. Default is an empty dictionary. Note: this will be overriden by the ``legend_loc``, ``legend_columns``, and ``legend_border`` parameters, if they are provided.

    Returns
    ----------
    None
    """
    # Ensure files is a list
    if isinstance(files, str):
        files = [files]
    
    from .utils import parse_params
    params = parse_params( {'legend_loc': legend_loc, 'legend_columns': legend_columns, 'legend_border': legend_border, 'dpi': dpi, 'legend_kwargs': legend_kwargs} )

    logs = [load(f) for f in files]

    # Load the PlottingHelp class and initialise for all logs
    from .plotting_help import PlottingHelp
    for log in logs:
        log.helper = PlottingHelp(
            log,
            params['display_mode'],
            params['feature_mode'],
            params['unit_borders'], 
            params['legend_loc'],
            params['legend_columns'],
            params['legend_border'],
            formatting.fontsizes,
            params['figsize'],
            params['dpi'],
            params['ppi'],
            max(150, int(params['dpi']/3)),
            params['x_label'],
            params['x_axis'],
            params['y_label'],
            params['y_axis_unit'],
            params['spines'],
            params['mineral_size'],
            params['feature_size']/2, # scales so default value is 1
            params['xmax'],
            {},
            {},
            params['legend_titles'],
            params['legend_kwargs'],
            log.grain_brackets
        )

    # Get the y_limits of each log to faciliate base-to-top legend order
    ylims = []
    for l in logs:
        if l.y_mode == 'age':
            y_limits = (l.df['height/age'].min(), l.df['height/age'].max() + l.df.iloc[-1]['thickness']) 
        elif l.y_mode == 'height':
            y_limits = (l.df['height/age'].min() - l.df.iloc[-1]['thickness'], l.df['height/age'].max()) 
        elif l.y_mode == 'depth':
            # l.df['height/age'] = l.df['height/age'] * -1
            y_limits = -l.df['height/age'].max(), (-l.df['height/age'].min() + l.df.iloc[-1]['thickness']) 
        ylims.append(y_limits)

    # Manually compute the legend order after the fact, for all logs base-to-top
    for i, l in enumerate(logs):
        leg = []
        for r, row in l.helper.df.iloc[::-1].iterrows():
            # Lithologies
            lithology_key = row.rock
            if lithology_key not in leg and lithology_key != 'no':
                leg.append(lithology_key)
            # Lenses
            for lr in row['lenses'].split(';'):
                if lr not in leg and lr != '':
                    leg.append(lr)
        # Invert if y-mode is height or depth
        if l.helper.y_mode in ['height', 'depth']:
            leg = leg[::-1]
        # Add not observed manually, if present
        if 'no' in l.helper.lithologies.keys():
            leg.append('no')
        l.helper.lithology_legend = leg
    # Features, minerals, etc. are accounted for in the merge_legends_and_create_legend function

    from matplotlib.pyplot import subplots, savefig, close
    from .utils import merge_legends_and_create_legend

    # Create figure and call function to create the legend
    fig, ax = subplots()
    leg = merge_legends_and_create_legend(logs, ylims, fig)
    
    # Ensure the fig_filename has the correct extension
    valid_extensions = fig.canvas.get_supported_filetypes().keys()
    # Check if filename ends with any valid extension
    if not any(filename.endswith(f'.{ext}') for ext in valid_extensions):
        print(f"Extension '{filename.split('.')[-1]}' not supported, saving as PNG instead.")
        filename += '.png'

    # Save only the legend region
    bbox = leg.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    ax.axis('off')
    savefig(filename, dpi=dpi, bbox_inches=bbox, transparent=transparent)
    print(f"Legend saved to {filename}")
    close()

def load(filepath : str, grain_preset : str = 'sedimentary', x_ticks_dict = None, grain_brackets = None) -> LogObject:
    """
    Reads in a file containing stratigraphic data and sets up the necessary variables for plotting. 
    
    Supported file formats: ``.csv``, ``.txt``, ``.xlsx``, ``.xls``. Desired column headers: ['height/age', 'rock', 'thickness', 'bottom_grain', 'top_grain', 'connection_type', 'erosion', 'lenses', 'minerals', 'features', 'contact']. 

    `See the documentation <https://stratapy.readthedocs.io/en/latest/getting_started/tutorial/file_format.html>`_ for more details on the expected format and structure of the input file.

    Parameters
    ----------
    filepath : str
        The path to the input file.
    grain_preset : str, optional
        Various default collections of grain sizes are available for different disciplines. Each one automatically passes a different ``x_ticks_dict`` and ``grain_brackets`` to the function. Options are 'sedimentary' (default), 'volcanic', and 'geological'. Alternatively, you can provide your own ``x_ticks_dict`` and ``grain_brackets`` directly, in which case this parameter is ignored.
        See `See the documentation <https://stratapy.readthedocs.io/en/latest/customisation/grain_size/index.html>`_ for details and examples of this functionality.
    x_ticks_dict : dict, optional
        A dictionary of x-tick labels and their corresponding values of grain size. Adjusting the labels and values will change where the x-ticks are placed on a log's x-axis. The labels should be unique strings; to have two separate labels for 'f' (e.g., 'f' for fine ash and 'f' for fine lapilli), suffix the string with any of [*, ^, &, _, £, $] to make it unique (these characters will be removed when displayed on the axis).
    grain_brackets : dict, optional
        A dictionary defining ranges of grain sizes where labelled brackets will be drawn. Each key of the dict is the label of a bracket, and the value is a list of consecutive grain sizes that will be included in the bracket. Grain sizes must match those in the ``x_ticks_dict``.

    Returns
    ----------
    LogObject : object
        An instance of the LogObject class containing the loaded data and set up variables.

    Raises
    ----------
    FileNotFoundError
        If the file is not found.
    ValueError
        If the file is not a valid CSV or does not contain the required columns.

    Examples
    ----------
    >>> import stratapy as sp
    >>> log = sp.load('path/to/your/data.csv')   # Initialise a visualisation
    >>> log.plot()                               # Create the figure

    Alternatively, you can change the grain size presets:

    >>> log = sp.load('path/to/your/data.csv', grain_preset='volcanic')
    >>> log.plot()  

    Or provide your own grain size ticks and brackets:

    >>> x_ticks = {'ash': 0.5, 'lapilli': 2, 'bomb': 64, 'block': 256}
    >>> grain_brackets = {'coarse': ['lapilli', 'bomb', 'block']}
    >>> log = sp.load('path/to/your/data.csv', x_ticks_dict=x_ticks, grain_brackets=grain_brackets)
    """
    from .utils import parse_params, read_strata_file
    
    # Validate parameters
    params = parse_params({'grain_preset': grain_preset, 'x_ticks_dict': x_ticks_dict, 'grain_brackets': grain_brackets})

    # Load example file, if requested
    if path.basename(filepath).lower().startswith('examples.'):
        filepath = path.join(config.direc, 'assets/examples', filepath.replace('examples.', ''))
        if path.exists(filepath):
            print(f"Using stratapy example log: {path.basename(filepath)}")
        else:
            print(f"'{path.basename(filepath).replace('examples.', '')}' is not a valid example file. Run `sp.list_examples()` to list the available example files, or provide a valid file path to load your own data.")
            return None

    # Read in csv
    df, y_mode = read_strata_file(filepath, formatting, params['x_ticks_dict'])

    # Collate data into dict
    log_data = {
        'df': df,
        'y_mode': y_mode,
        'lithologies': formatting.lithologies,
        'minerals_list': formatting.minerals_list,
        'features': formatting.features,
        'contact_types': formatting.contact_types,
        'direc': config.direc,
        'user_direc': config.user_direc,
        'x_ticks_dict': params['x_ticks_dict'],
        'grain_brackets': params['grain_brackets']
    }
    
    # Create a LogObject instance with the loaded data
    return LogObject(**log_data)

def correlated_logs(files, left_y_axis : bool = True, offsets : 'array-like' = None, spine_distance : float = 30, fig_kwargs : dict = {}, **kwargs) -> MultiLogObject:
    """
    The ``correlated_logs()`` function is designed for side-by-side log plots, allowing for easy visual correlation between multiple stratigraphic logs. Unlike ``multi_fig()``, logs have no axes of their own, and instead share a common y-axis, which can be styled as desired.
    
    The function accepts any of the parameters available in the ``LogObject.plot()`` method, allowing for extensive customisation of the appearance and layout of the logs, though it is optimised for logs displayed in 'log' mode, without grain size axes. Similarly, since the y-axis is shared, it is recommended to ensure that all logs have compatible y-axes (e.g., all in age, or all in depth/height).

    In addition, this function accept other parameters to control the style and layout of the figure; see below.

    Parameters
    ----------
    files : array-like
        A list, numpy array, or iterable of file paths to the stratigraphic data files to be plotted. Each file will be loaded and plotted as a separate log.
    left_y_axis : bool, optional
        If True, a single y-axis will be created on the left side of the first log, shared by all logs. Default is False, meaning each log will have its own y-axis on the left side.
    offsets : array-like, optional
        An iterable of numeric offsets to apply to the y-axis of each log. The length of the list must match the number of files provided. Offsets are applied as follows: for 'depth' or 'age' y-modes, the offset is subtracted from the y-values; for 'height' y-mode, the offset is added to the y-values. Default is None, meaning no offsets are applied.
    fig_kwargs : dict, optional
        A dictionary of keyword arguments to be passed to the ``matplotlib.pyplot.subplots()`` function when creating the figure and axes.
    **kwargs
        Additional keyword arguments to be passed to the ``LogObject.plot()`` method for each log.

    Returns
    ----------
    MultiLogObject : object
        An instance of the MultiLogObject class containing the figure, axes, logs, and legend.

    Notes
    ----------
    - use the ``y_label`` parameter to set a shared y-axis label for all logs, if desired.
    """
    from .utils import parse_params, merge_legends_and_create_legend
    from matplotlib.pyplot import subplots

    # Set some defaults unique to this function
    unique_defaults = {
        'display_mode': 'log',
        'feature_mode': 'merge',
        'spines': False,
    }
    for k, v in unique_defaults.items():
        kwargs[k] = v if k not in kwargs else kwargs[k]
    
    # Validate kwargs (do it once now to prevent repeating warnings in each log)
    kwargs = parse_params(kwargs)

    # Extract load() parameters from kwargs
    load_keys = ['grain_preset', 'x_ticks_dict', 'grain_brackets']
    load_kwargs = {k: kwargs.pop(k, None) for k in load_keys}

    # Ignore fig and ax if provided, as new ones will be created
    kwargs.pop('fig', None)
    kwargs.pop('ax', None)

    # Create a figure 
    nrows, ncols = 1, int(len(files))
    figsize = kwargs.get('figsize', (ncols * 5, nrows * 5))
    fig, axes = subplots(nrows=nrows, ncols=ncols, figsize=figsize, sharey=True, dpi=kwargs.get('dpi', 150), **fig_kwargs)

    # If only one axis, convert to a list for consistency
    if not isinstance(axes, (list, ndarray)):
        axes = [axes]

    # Ensure that files and axes are flattened, and are the same length
    files = [f for sublist in files for f in sublist] if isinstance(files[0], list) else files
    axes = [a for sublist in axes for a in sublist] if isinstance(axes[0], list) else axes
    if len(files) != len(axes):
        raise ValueError(f"The number of files ({len(files)}) must match the number of axes ({len(axes)}). Please provide the same number of files and axes.")

    # Ensure offsets is a list of the same length as files
    if offsets is None:
        offsets = [0] * len(files)
    elif len(offsets) != len(files):
        raise ValueError(f"The number of offsets ({len(offsets)}) must match the number of files ({len(files)}). Please provide the same number of offsets as files.")

    # Load each log
    logs = [load(f, **{k: v for k, v in load_kwargs.items() if v is not None}) for f in files]

    # If all logs do not share the same y_mode, throw a warning
    y_modes = [l.y_mode for l in logs]
    if len(set(y_modes)) > 1:
        print("Warning: Not all logs share the same y_mode. Ensure that the y-axes are compatible for correlation.")
    else:
        y_mode = y_modes[0]

    # For each log, apply the offset to the height/age column
    for i, l in enumerate(logs):
        if offsets[i] != 0:
            if y_mode in ['depth', 'age']:
                l.df['height/age'] = l.df['height/age'] - offsets[i]
                l.original_df['height/age'] = l.original_df['height/age'] - offsets[i]
            else:
                l.df['height/age'] = l.df['height/age'] + offsets[i]
                l.original_df['height/age'] = l.original_df['height/age'] + offsets[i]

    # Get the y_limits of each log
    ylims = []
    for l in logs:
        if l.y_mode == 'age':
            y_limits = (l.df['height/age'].min(), l.df['height/age'].max() + l.df.iloc[-1]['thickness']) 
        elif l.y_mode == 'height':
            y_limits = (l.df['height/age'].min() - l.df.iloc[-1]['thickness'], l.df['height/age'].max()) 
        elif l.y_mode == 'depth':
            y_limits = -l.df['height/age'].max(), (-l.df['height/age'].min() + l.df.iloc[-1]['thickness']) 
        ylims.append(y_limits)

    # Find the global y-limits and set for each log (shared y-axes)
    yminn = min([y[0] for y in ylims])
    ymaxx = max([y[1] for y in ylims])
    # Override the y limits for each log then plot logs
    for i, l in enumerate(logs):
        l.override_ylims = (yminn, ymaxx)  # Set the y limits for each log
        l.share_legend = True
        l.plot(fig, axes[i], **kwargs)

    if kwargs['legend']:
        leg = merge_legends_and_create_legend(logs, ylims, fig)
    else:
        leg = None

    # Formatting & style depending on layout
    if left_y_axis:
        # If single twin y-axis desired, remove all y-ticks from all axes and add new twin y-axis to the left of axes[0]
        [a.set_yticks([]) for a in axes[:]]
        # Add new twin y spine to the left of axes[0]
        twin1 = axes[0].twinx()
        # Move the new axis spine further left, outside the existing y-axis
        twin1.spines["left"].set_position(("outward", spine_distance))
        twin1.set_ylim(axes[0].get_ylim())
        twin1.yaxis.set_label_position('left')
        twin1.yaxis.tick_left()
        # Hide the right spine of the twin axis
        twin1.spines["right"].set_visible(False)
        twin1.spines["top"].set_visible(False)
        twin1.spines["bottom"].set_visible(False)
        # Set the label for the new axis
        if logs[0].helper.y_label is not None:
            twin1.set_ylabel(f"{logs[0].helper.y_label} ({logs[0].helper.y_axis_unit})", fontsize=formatting.fontsizes['y_axis_label'])
        # And remove labels from other axes
        [a.set_ylabel('') for a in axes[:]]
    else:
        # Otherwise, add ensure y_label is only on the first axis, and add in the left spine for it
        for a in axes[1:]:
            a.tick_params(axis='y', left=False, right=False, labelleft=False)
            a.set_ylabel('')
        axes[0].spines['left'].set_visible(True)

    # Return the figure, axes, logs, and legend in a MultiLogObject for easy access and saving
    return MultiLogObject(fig, axes, logs, leg)

def multi_fig(files, nrows : int = 1, ncols : int = -1, sharey : bool = False, sharex : bool = False, fig : 'plt.Figure' = None, axes : 'plt.Axes' = None, fig_kwargs : dict = {}, **kwargs) -> MultiLogObject:
    """
    This function enables the plotting of multiple logs in a single figure, critically, with a shared legend. Each log is plotted on its own axis, allowing for individual customisation while maintaining a cohesive overall appearance. All optional parameters available in the ``LogObject.plot()`` method can be passed to this function, but are shared across all logs for consistency. 

    Parameters
    ----------
    files : array-like
        An list, numpy array, or other iterable of file paths to stratigraphic data files. Each file should be in a supported format and contain the required columns.
    nrows : int, optional
        The number of rows in the figure. Default is 1.
    ncols : int, optional
        The number of columns in the figure. Default is -1, which will fit the number of columns to the number of files provided. 
    sharey : bool, optional
        If True, all logs will share the same y-axis limits. Default is False.
    sharex : bool, optional
        If True, all logs will share the same x-axis limits. Default is False.
    fig : matplotlib.figure.Figure, optional
        Matplotlib figure object to plot the logs on. If None, a new figure will be created. ``axes`` must also be provided if a custom ``fig`` is provided else a new figure will be created.
    axes : list of matplotlib.axes.Axes, optional
        List of matplotlib axes objects to plot the logs on. If None, new axes will be created. ``fig`` must also be provided if custom ``axes`` are provided else new axes will be created. 
    fig_kwargs : dict, optional
        A dictionary of keyword arguments to be passed to ``plt.subplots()`` when creating a new figure. 
    **kwargs : dict
        Additional keyword arguments to be passed to the ``LogObject.plot()`` method for each log
    
    Returns
    ----------
    MultiLogObject : object
        An instance of the MultiLogObject class containing the figure, axes, logs, and legend.

    Notes
    ----------
    If a custom ``fig`` and ``axes`` are provided, ``multi_fig``'s ``sharey`` and ``sharex`` should be used instead of the ``sharey`` and ``sharex`` parameters of ``plt.subplots()``. 
    Validation of custom ``fig`` and ``axes`` variables is minimal.
    """
    from .utils import parse_params, merge_legends_and_create_legend
    from matplotlib.pyplot import subplots

    # Set some defaults unique to this function
    unique_defaults = {
        'spines': False,
    }

    # If display_mode is 'log', and no feature_mode is provided, set to 'merge' for better appearance by default
    if 'display_mode' in kwargs and kwargs['display_mode'] == 'log' and 'feature_mode' not in kwargs:
        unique_defaults['feature_mode'] = 'merge'
    
    # Validate kwargs (do it once now to prevent repeating warnings in each log)
    for k, v in unique_defaults.items():
        kwargs[k] = v if k not in kwargs else kwargs[k]
    kwargs = parse_params(kwargs)
    
    # Extract load() parameters from kwargs
    load_keys = ['grain_preset', 'x_ticks_dict', 'grain_brackets']
    load_kwargs = {k: kwargs.pop(k, None) for k in load_keys}
    # Drop fig and ax from kwargs to avoid passing them to LogObject.plot() twice
    kwargs.pop('fig', None)
    kwargs.pop('ax', None)

    # Overwrite subplots() sharey and sharex
    fig_kwargs['sharey'] = False
    fig_kwargs['sharex'] = False

    # Create a figure with enough axes if not provided
    if fig is None or axes is None:
        if ncols == -1:
            ncols = len(files)
        # Ensure ncols x nrows is enough to plot all files
        if ncols * nrows < len(files):
            print(f"Warning: nrows x ncols ({nrows} x {ncols} = {nrows * ncols}) is less than the number of files ({len(files)}). Adjusting ncols to fit all logs.")
            ncols = (len(files) + nrows - 1) // nrows
        
        # Create subplots and pass all fig_kwargs 
        fig, axes = subplots(nrows=nrows, ncols=ncols, figsize=kwargs.get('figsize', (ncols * 4, nrows * 6)), dpi=kwargs.get('dpi', 150), **fig_kwargs)
        print(f"Created new figure with {nrows} rows and {ncols} columns for {len(files)} files.")

    # If only one axis is provided, convert to a list
    if not isinstance(axes, (list, ndarray)):
        axes = [axes]
    
    # Ensure that files and axes are flattened, and are the same length
    files = [f for sublist in files for f in sublist] if isinstance(files[0], list) else files
    axes = asarray(axes).flatten().tolist()
    if len(files) > len(axes):
        raise ValueError(f"The number of files ({len(files)}) must match the number of axes ({len(axes)}). Please provide the same number of files and axes.")
    elif len(files) < len(axes):
        # Hide unused axes
        for a in axes[len(files):]:
            a.set_visible(False)
        axes = axes[:len(files)]

    # Load each log
    logs = [load(f, **{k: v for k, v in load_kwargs.items() if v is not None}) for f in files]

    # Get the y_limits of each log
    ylims = []
    for l in logs:
        if l.y_mode == 'age':
            y_limits = (l.df['height/age'].min(), l.df['height/age'].max() + l.df.iloc[-1]['thickness']) 
        elif l.y_mode == 'height':
            y_limits = (l.df['height/age'].min() - l.df.iloc[-1]['thickness'], l.df['height/age'].max()) 
        elif l.y_mode == 'depth':
            # l.df['height/age'] = l.df['height/age'] * -1
            y_limits = -l.df['height/age'].max(), (-l.df['height/age'].min() + l.df.iloc[-1]['thickness']) 
        ylims.append(y_limits)
    yminn = min([y[0] for y in ylims])
    ymaxx = max([y[1] for y in ylims])

    # Also get the x_limits of each log for using sharex
    xlims = []
    for l in logs:
        x_limits = (min(l.df.bottom_grain.min(), l.df.top_grain.min()), max(l.df.bottom_grain.max(), l.df.top_grain.max()))
        xlims.append(x_limits)
    xmin = min([x[0] for x in xlims])
    xmax = max([x[1] for x in xlims])
    
    # If sharing x-axes, set xmax kwarg to be the global xmax
    if sharex:
        kwargs['xmax'] = xmax

    # Plot each lot
    for i, l in enumerate(logs):
        if sharey:
            # If sharing y-axes set global y-limits, then plot
            l.override_ylims = (yminn, ymaxx)
        l.share_legend = True # Flag to defer legend creation 
        l.plot(fig, axes[i], **kwargs)
        if sharey:
            # Tidy labels
            l.ax.set_ylabel("") if i > 0 else None

    # Compute legend
    if kwargs['legend']:
        leg = merge_legends_and_create_legend(logs, ylims, fig)
    else:
        leg = None

    # Return the figure, axes, logs, and legend in a MultiLogObject for easy access and saving
    return MultiLogObject(fig, axes, logs, leg)

def update_minerals(minerals : dict) -> None:
    """
    Enables the formatting of existing minerals to be updated, or new minerals to be added to the package.

    Parameters
    ----------
    minerals : dict
        A dictionary of the minerals to be added to the user's data in the format {key: (fillcolour, edgecolour, shape)}.
        The fillcolour and edgecolour can be RGB tuples, matplotlib color strings, or hex codes; the code will attempt to convert automatically.
        The key is the name of the mineral; it is case sensitive, with the title case version used in the legend.
        Shape is any of the `matplotlib markers <https://matplotlib.org/stable/api/markers_api.html>`_.

    Examples
    --------
    >>> import stratapy as sp
    >>> sp.update_minerals( {
    >>>     # Magenta diamond with black edge - overrides default garnet style
    >>>     'garnet': ('#FF00FF', 'k', 'd'),
    >>>     # Orange circle with brown edge - new mineral
    >>>     'honeystone': ('orange', 'brown', 'o'),
    >>> } )
    >>>
    >>> # 'garnet' is available by default, so this will update it
    >>> sp.update_minerals({'garnet': ((1, 0, 0), 'red', 'o')})
    >>> # 'granite' is not available by default, so this will add it
    >>> sp.update_minerals({'granite': ('#FF0000', 'r', 'o')})
    """
    import matplotlib.markers as mmarkers
    from .utils import colour_to_rgba

    # Ensure input is a dictionary
    if not isinstance(minerals, dict):
        print(f"Warning in 'update_minerals':  The input must be a dictionary of minerals, not {type(minerals).__name__}.  Please provide a dictionary in the format {{'mineral_name': (fillcolour, edgecolour, shape)}}.")
        return
    
    filled_markers = {'o', 's', 'D', '^', 'v', '<', '>', '8', 'p', 'h', 'H', '*', 'X'}

    added, updated, missing = [], [], {}
    for key, value in minerals.items():
        # Ensure input is in correct format
        if type(minerals[key]) != tuple or len(minerals[key]) != 3:
            missing.update({key: 'Mineral must be a tuple of length 3.'})
            continue
        
        # Use existing properties if blank and mineral already exists
        if key in formatting.minerals_list:
            new_fill = formatting.minerals_list[key][0] if value[0] == '' else value[0]
            new_edge = formatting.minerals_list[key][1] if value[1] == '' else value[1]
            new_shape = formatting.minerals_list[key][2] if value[2] == '' else value[2]
        else:
            new_fill, new_edge, new_shape = value

        # Validate fill and edge colours
        try:
            new_fill = colour_to_rgba(new_fill)
        except Exception:
            missing.update({key: f"Fill colour '{new_fill}' must be a valid colour string or RGB tuple."})
            continue
        try:
            new_edge = colour_to_rgba(new_edge)
        except Exception:
            missing.update({key: f"Edge colour '{new_edge}' must be a valid colour string or RGB tuple."})
            continue

        # Validate marker
        if new_shape not in mmarkers.MarkerStyle.markers:
            missing.update({key: f"Shape '{new_shape}' is not a valid matplotlib marker."})
            continue

        # If the marker can't take an edge colour, set it to None
        if new_shape not in filled_markers:
            new_edge = None

        if key not in formatting.minerals_list:
            added.append(key)
        else:
            updated.append(key)

        formatting.minerals_list[key] = (new_fill, new_edge, new_shape)

    # Print results
    if added:
        print("Minerals added for use: " + ", ".join([f"'{a}'" for a in added]))
    if updated:
        print("Minerals updated: " + ", ".join([f"'{u}'" for u in updated]))
    if missing:
        print("The following requested minerals are not in the correct format and will not be added or updated:\n" + "\n".join([f"\t'{k}': {v}" for k, v in missing.items()]))

def update_lithologies(patterns : dict) -> None:
    """
    In development : To update lithologies, the user can provide a dictionary of new keys, each with a tuple of length three as its value.
    Existing keys cannot be changed, but new keys can be added using the format (existing pattern or filepath, colour (optional), name), the only exception being the 'no observation' lithology, which can be changed to a new name (there is no fill colour so it takes the background of the figure). Lithology keys are all case insensitive.

    Parameters
    ----------
    patterns : dict
        A dictionary of the lithologies to be added to the user's data in the format {key: (pattern/existing key/filepath, colour, name)}. 
        The pattern can be an existing lithology key (e.g., 'sandstone'), or a filepath to a custom image (e.g., 'path/to/image.png').

        The colour can be a matplotlib colormap name, a colour string, or an RGB tuple; the code will attempt to convert automatically. If using a custom image, the colour is ignored.

        The name is the string that will be displayed in the legend for this lithology.
    
    Returns
    ----------
    None

    Examples
    --------
    >>> import stratapy as sp
    >>> sp.update_lithologies( {
    >>>     # A simple colour fill
    >>>     'clay': ('', '#A53535', 'Clay'),
    >>>     # A variation on an existing pattern with a new colour
    >>>     'new_sandstone': ('sandstone', 'tan', 'New sandstone'),
    >>>     # Naming a pattern lithology
    >>>     'soil': ('117', 'w', 'Soil'),
    >>>     # A custom image 
    >>>     'custom': ('path/to/image.png', '', 'Custom lithology'),
    >>> })

    Notes
    ----------
    - Supported formats for custom images are: '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'.
    """
    from difflib import get_close_matches
    from .utils import colour_to_rgba
    from matplotlib import colormaps
    import matplotlib.colors as mcolors

    # Ensure input is a dictionary
    if not isinstance(patterns, dict):
        print(f"Error in 'update_lithologies':  The input must be a dictionary, not '{type(patterns).__name__}'.  Please provide a dictionary in the format {{'lithology_key': (pattern/existing key/filepath, colour, name)}}.")
        return

    ignore, updated, added = {}, [], []

    # Loop over the requested additions
    for key, value in patterns.items():

        key = key.lower()  # Lithology keys are case insensitive

        # If the key contains an asterisk, throw warning about it cannot - and remove the asterisk
        if '*' in key or '^' in key:
            key = key.strip('*').strip('^')
            print(f"Warning: custom lithologies cannot contain asterisks (*) or carats (^). This lithology has been added with the key '{key}' instead.")

        # If key is 'no', special case for 'no observation' lithology
        if key == 'no':
            # Primarily expect a string or a 3-length tuple with a string in the last position. Accept any value which can be interpreted as a string, otherwise ignore
            if isinstance(value, str):
                name = value
            elif isinstance(value, tuple):
                # Get last value if it is a string
                if isinstance(value[-1], str):
                    name = value[-1]
                else:
                    # Otherwise get the first string in the tuple, or use default value
                    name = next((v for v in value if isinstance(v, str)), None)
                    if name is None:
                        name = 'Not observed'
                        ignore.update({key: 'The "no" pattern must be a string or a tuple with a string as the last value.'})
                        continue
            else:
                # If it is not a string or tuple, ignore
                ignore.update({key: 'The "no" pattern must be a string or a tuple with a string as the last value.'})
                continue
            formatting.lithologies[key] = ('fill', 'w', '', 'k', name)
            updated.append(key)

        # If the lithology exists in the default keys, throw ignore
        elif key in formatting.default_lithologies.keys():
            ignore.update({key: f"'{key}' is a default lithology and cannot be changed. You can create a new lithology using this pattern by using e.g.: 'new_{key}': ('{key}', 'colour/cmap', 'name')."})

        # If tuple of length 3 with an empty or None first value, this is a colour-filled lithology with no pattern
        elif isinstance(value, tuple) and (len(value) == 3 and (value[0] == '' or value[0] is None)):
            # If the first value is empty or None, it is a colour-filled lithology with no pattern
            try:
                cmap = colour_to_rgba(value[1]) if value[1] != '' else 'w' # Default to white if no colour provided
            except Exception:
                ignore.update({key: f"'{value[1]}' is not a valid colour. Please use a valid colour string or RGB tuple."})
                continue
            formatting.lithologies[key] = ('fill', cmap, '', cmap, str(value[-1]))
            added.append(key)

        # All other inputs should be tuples of length 3, else throw ignore
        elif not isinstance(value, tuple) or len(value) != 3:
            ignore.update({key: f"'{key}' must be a tuple of length 3; see the documentation for more information."})
        else:
            # Only 3-length tuples left. If the first value is a filepath (contains '.' and os.exists), it is a custom image, otherwise it is a variation of an existing pattern
            if isinstance(value[0], str) and '.' in value[0]:
                if not path.exists(value[0]):
                    ignore.update({key: f"Filepath '{value[0]}' does not exist. Please provide a valid filepath for the custom lithology image."})
                    continue
                # If it is a custom image, use a placeholder cmap 
                from matplotlib.colors import LinearSegmentedColormap
                cmap = LinearSegmentedColormap.from_list('custom_cmap_transparent', [(0,0,0,0), (0,0,0,1)], N=256)
                formatting.lithologies[key] = ('pattern', value[0], cmap, str(value[2]))
                added.append(key)
            else:
                rock_names = [f[-1].lower() for f in formatting.lithologies.values()]   
                # If a variation of an existing pattern, it must exist
                if value[0] not in formatting.lithologies and value[0].lower() not in rock_names: 
                    # Tell user of closest match if exists
                    closest_match = get_close_matches(value[0], rock_names, n=1, cutoff=0.6)
                    if closest_match:
                        ignore.update({key: f"'{value[0]}' is not a valid existing lithology key, check the pattern spelling\n{''.join([' ']*(len(key)+6))}> did you mean '{closest_match[0]}'?"})
                        continue
                    else:
                        ignore.update({key: f"'{value[0]}' is not a valid existing lithology key, check the pattern spelling."})
                        continue
                else:
                    # Assign key, depending on if it was a key or name
                    if value[0].lower() not in formatting.lithologies.keys():
                        existing_key = [key for key, val in formatting.lithologies.items() if val[-1].lower() == value[0].lower()][0]
                    else:
                        existing_key = value[0]

                # Extract and validate colour
                # If no cmap provided, assume white (default)
                cmap = value[1]
                if cmap == '':
                    cmap = 'w'
                # If the cmap is an actual cmap, use that, if not, assume a colour and create a cmap, else error
                if isinstance(cmap, str) and cmap in colormaps():
                    cmap = cmap
                else:
                    try:
                        cmap = colour_to_rgba(cmap)
                        # If it is, create a colormap from it
                        cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', [cmap, 'k'], N=256)
                    except Exception:
                        ignore.update({key: f"'{value[1]}' is not a valid colour or colourmap. Please use a valid colour string or RGB tuple, or a valid colourmap string."})
                        continue
                    
                # Format: (type, filepath, colour/map, name)
                formatting.lithologies[key] = ('lith', formatting.lithologies[existing_key][1], cmap, str(value[2]))
                added.append(key)
                
    # Print results
    if added:
        print("Lithologies added for use: " + ", ".join([f"'{a}'" for a in added])) 
    if updated:
        print("Lithologies updated: " + ", ".join([f"'{u}'" for u in updated]))
    if ignore:
        print("Warning: The following requested lithologies are not in the correct format and will not be added or updated:\n" + "\n".join([f"  > '{k}': {v}" for k, v in ignore.items()]))

def update_features(new_features : dict) -> None:
    """
    This function enables the addition or editing of features in stratapy. The user can provide a dictionary of new keys, each with a tuple of length three as its value. Existing keys cannot be changed, but new keys can be added using the format (type, filepath, name). The type can be 'fossil', 'structure', or 'tectonic' (or 'f', 's', 't' for short), and the filepath can be an existing feature key or a valid filepath to a custom image. Feature keys are case insensitive.

    Parameters
    ----------
    new_features : dict
        A dictionary of the features to be added to the user's data in the format {key: (type, filepath, name)}. 
        The type can be 'fossil', 'structure', or 'tectonic' (or 'f', 's', 't' for short).
        The filepath can be an existing feature key or a valid filepath to a custom image.
        The name is the string that will be displayed in the legend for this feature.
    
    Returns
    ----------
    None

    Examples
    --------
    >>> import stratapy as sp
    >>> sp.update_features( {
    >>>     # Renames the default 'normal grading' feature to 'Grading' in the legend
    >>>     'normal grading': ('', '', 'Grading'),          
    >>>     # Moves the default 'Mollusc' feature to the sedimentary structures group
    >>>     'mollusc': ('structure', '', 'Mollusc'),               
    >>>     # Moves the default 'Bioturbation (med.)' feature to the fossils group, and re-names to 'Bioturbation'
    >>>     'bioturbation medium': ('f', '', 'Bioturbation'),   
    >>>     # Creates a new 'Scaphopod' feature using the default trace fossil image and type
    >>>     'scaphopod': ('', 'trace fossil', 'Scaphopod'),     
    >>>     # Adds a new fossil feature with a custom image and name
    >>>     'my_fossil': ('fossil', 'my_fossil.png', 'My Fossil'),
    >>> } )
    """
    missing, updated, added = [], [], []
    for key, value in new_features.items():
        key = str(key)  # Ensure the key is case insensitive
        Ftype, Fpath, Fname = str(value[0]).lower(), str(value[1]), str(value[2])

        # Ensure input is in correct format
        if type(new_features[key]) != tuple or len(new_features[key]) != 3:
            missing.append(f"'{key}' must be a tuple of length 3 (type, filepath, name).")
            continue

        # Validations:
        # Key must be string
        if not isinstance(key, str):
            missing.append(f"'{key}' is not a valid string for a feature key.")
            continue
        # Ftype must be an available option
        if Ftype not in ['fossil', 'f', 'structure', 's', 'tectonic', 't', '']:
            missing.append(f"'{key}' : '{Ftype}' is not a valid feature type and has been ignored.")
        # Fpath must be a string (if not empty) 
        if not isinstance(Fpath, str):
            missing.append(f"'{key}' : '{Fpath}' must be a string")

        # If key exists, use existing values if new ones are blank
        if key in formatting.features.keys():
            Fpath = formatting.features[key][1] if Fpath == '' else Fpath
            Ftype = formatting.features[key][0] if Ftype == '' else Ftype
            Fname = formatting.features[key][2] if Fname == '' else Fname

        # If the filepath is an existing feature, use its filepath, else use the requested filepath (if it exists)
        if Fpath.lower() in formatting.features.keys():
            Ftype = formatting.features[Fpath.lower()][0] if Ftype == '' else Ftype
            Fpath = formatting.features[Fpath.lower()][1]
        from difflib import get_close_matches
        # Now assume it is a filepath
        if isinstance(Fpath, str) and path.exists(Fpath):
            Fpath = Fpath
        else:
            if Fpath == '':
                closest_match = get_close_matches(key, formatting.features.keys(), n=1, cutoff=0.6)
            else:                
                closest_match = get_close_matches(Fpath, formatting.features.keys(), n=1, cutoff=0.6)

            missing.append(f"'{key}' : '{Fpath}' is not a valid filepath or existing feature name, check the filepath or feature spelling.{'\n'+''.join([' ']*(len(key)+7)) if closest_match else ' '}" + (f"> did you mean '{closest_match[0]}'?" if closest_match else "."))
            continue

        # Assign a type if not provided
        if Ftype == '':
            Ftype = 'fossil'
            missing.append(f"'{key}' : No type provided. Defaulting to 'fossil'.")

        # If the filepath is a string but does not exist, throw warning and ignore
        if isinstance(Fpath, str) and not path.exists( path.join(config.user_direc, Fpath) ):
            missing.append(f"The filepath '{Fpath}' does not exist for '{key}'. Please provide a valid filepath for this feature.")
            continue

        # Ensure the name is a string
        if isinstance(Fname, str) and Fname == '' and key in formatting.features:
            Fname = formatting.features[key][2]
        elif not isinstance(Fname, str):
            missing.append(f"'{key}' : '{Fname}' is not a valid string for '{key}'. Please provide a valid name for this feature.")
            continue

        formatting.features[key] = (Ftype.lower(), Fpath, Fname)

        if key not in formatting.features:
            added.append(key)
        else:
            updated.append(key)

    if added:
        print(f'Features added: {", ".join(added)}')
    if updated:
        print(f'Features updated: {", ".join(updated)}')
    if missing:
        print(f'Warning: The following requested features are not in the correct format and will not be added to the data:\n  > ' + "\n  > ".join(missing))
            
def chronostratigraphy(lower_age : float, upper_age : float, fig : 'plt.Figure' = None, ax : 'plt.Axes' = None, ranks_to_display : list = [0,1,2,3,4,5], unit : str = 'Ma', orientation : str = 'vertical', figsize : tuple = None) -> 'plt.Axes':
    """
    Creates a chronostratigraphic timescale on the given axis, vertically or horizontally.

    Parameters
    ----------
    lower_age : float
        The lower age limit for the timescale in Ma.
    upper_age : float
        The upper age limit for the timescale in Ma.
    fig : matplotlib.figure.Figure, optional
        The figure to draw the timescale on. Default is None, in which a new figure will be created. If a custom figure is provided, a custom axis must also be provided.
    ax : matplotlib.axes.Axes, optional
        The axis to draw the timescale on. Default is None, in which a new axis will be created. If a custom axis is provided, a custom figure must also be provided.
    ranks_to_display : list, optional
        A list of ranks to display on the timescale.
    unit : str, optional
        The unit for the age scale; this will determine what values ``lower_age`` and ``upper_age`` are interpreted as, and this scale will be used for the x-axis and its label. Default is 'Ma' (millions of years). Options are 'Ma' (millions of years), 'ka' (thousands of years), and 'a' (years).
    orientation : str, optional
        'vertical' (default) or 'horizontal' for horizontal timescale.
    figsize : tuple, optional
        The size of the figure to create if no custom figure and axis are provided. Default is (3, 8) for a vertical timescale or (8, 3) for a horizontal timescale.
    
    Returns
    ----------
    ax : matplotlib.axes.Axes
        The axis with the timescale drawn on it.

    Notes
    ----------
    The timescale is the International Chronostratigraphic Chart from the International Commission on Stratigraphy, which is updated periodically. The data for the timescale is stored in the package and can be updated by the user if desired; see the documentation for more information.
    See the tutorial notebook for examples of this function.
    
    Examples
    ----------
    >>> import stratapy as sp
    >>> # Create a vertical timescale from 0 to 500 Ma
    >>> sp.chronostratigraphy(0, 500)
    >>>
    >>> # Create a horizontal timescale from 237 to 242 Ma, with a custom figure size and only displaying the period, epoch, and age ranks
    >>> sp.chronostratigraphy(237, 242, orientation='horizontal', figsize=(10, 3), ranks_to_display=[3,4,5])
    """
    if orientation not in ['vertical', 'horizontal']:
        print(f"Warning: orientation '{orientation}' is not valid. Please use 'vertical' or 'horizontal'. Defaulting to 'vertical'.")
        orientation = 'vertical'

    if figsize is None:
        figsize = (3, 8) if orientation == 'vertical' else (8, 3)

    # Create figure if doesn't exist
    if fig is None or ax is None:
        from matplotlib.pyplot import subplots
        fig, ax = subplots(figsize=figsize, dpi=150)


    # Ensure units are valid
    unit_factors = {'Ma': 1, 'ka': 1e-3, 'a': 1e-6}
    if unit.lower() not in [f.lower() for f in unit_factors.keys()]:
        print(f"Warning: unit '{unit}' is not valid. Please use 'Ma', 'ka', or 'a'. Defaulting to 'Ma'.")
        unit = 'Ma'
    factor = unit_factors[[f for f in unit_factors.keys() if f.lower() == unit.lower()][0]]

    # Ensure chronology
    if lower_age > upper_age:
        print(f"Warning: lower_age ({lower_age}) is greater than upper_age ({upper_age}). Swapping the values.")
        lower_age, upper_age = upper_age, lower_age

    from .utils import make_box
    from pandas import read_csv

    df = read_csv(path.join(config.direc, 'assets/GeologicalTimescale.csv'), encoding='utf-8')
    df = df[df.Rank != 'Subsystem']
    rank_dict = {'Stage': 5, 'Series': 4, 'System': 3, 'Erathem': 2, 'Eonothem': 1, 'Super-Eonothem': 0}
    rank_width = 1
    # Convert the ages in the dataframe to the desired unit
    df['Age_S'] = df['Age_S'] / factor
    df['Age_E'] = df['Age_E'] / factor

    if orientation == 'horizontal':
        y_range = [ranks_to_display[0] * rank_width, ranks_to_display[-1] * rank_width + rank_width]
        ax.set_ylim(y_range)
        xlims = (lower_age, upper_age)
        ax.set_xlim(xlims)
        # Set y-ticks with rank names
        ax.set_yticks([rank_dict[k] * rank_width + rank_width / 2 for k in list(rank_dict.keys())[::-1] if rank_dict[k] in ranks_to_display])
        ax.set_yticklabels(list(rank_dict.keys())[::-1][y_range[0]:y_range[1]], rotation=0, fontsize=formatting.fontsizes['y_tick_labels'])
    else:
        x_range = [ranks_to_display[0] * rank_width, ranks_to_display[-1] * rank_width + rank_width]
        ax.set_xlim(x_range)
        ylims = (lower_age, upper_age)
        ax.set_ylim(ylims)
        ax.invert_yaxis()
        if ax.get_ylabel() == '':
            ax.set_ylabel(f'Age ({unit})', fontsize=formatting.fontsizes['y_axis_label'])
        # Set x-ticks with rank names
        ax.set_xticks([rank_dict[k] * rank_width + rank_width / 2 for k in list(rank_dict.keys())[::-1] if rank_dict[k] in ranks_to_display])
        ax.set_xticklabels(list(rank_dict.keys())[::-1][x_range[0]:x_range[1]], rotation=90, fontsize=formatting.fontsizes['chronostratigraphy_labels'])

    # Filter data within age limits
    df_cut = df[((df['Age_S'] >= lower_age) & (df['Age_S'] <= upper_age)) | ((df['Age_E'] >= lower_age) & (df['Age_E'] <= upper_age)) | ((df['Age_S'] <= lower_age) & (df['Age_E'] >= upper_age))]
    for i, row in df_cut.iterrows():
        if row['Age_S'] < lower_age:
            df_cut.at[i, 'Age_S'] = lower_age
        if row['Age_E'] > upper_age:
            df_cut.at[i, 'Age_E'] = upper_age

    text_entries, text_shorts = [], []
    for i, row in df_cut.iterrows():
        if row['Rank'] not in rank_dict or rank_dict[row['Rank']] not in ranks_to_display:
            text_entries.append(None)
            text_shorts.append(None)
            continue
        # For horizontal, swap x/y in make_box
        if orientation == 'horizontal':
            # You need to modify make_box to support horizontal mode, or wrap it here
            # Example: pass a flag or swap x/y when calling make_box
            ax, t, t2 = make_box(ax, row, rank_dict, rank_width, fontsize=formatting.fontsizes['chronostratigraphy_periods'], orientation='horizontal')
        else:
            ax, t, t2 = make_box(ax, row, rank_dict, rank_width, fontsize=formatting.fontsizes['chronostratigraphy_periods'])
        text_entries.append(t)
        text_shorts.append(t2)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    # Remove text that doesn't fit within the box, and center text in box
    for i, (t, t2) in enumerate(zip(text_entries, text_shorts)):
        if t is None or t2 is None:
            continue
        if orientation == 'horizontal':
            x_pix1, _ = ax.transData.transform((df_cut.iloc[i]['Age_S'], 0))
            x_pix2, _ = ax.transData.transform((df_cut.iloc[i]['Age_E'], 0))
            region_width_pixels = abs(x_pix2 - x_pix1)
            text_bbox = t.get_window_extent(renderer=renderer)
            text_width = text_bbox.width
            text_bbox2 = t2.get_window_extent(renderer=renderer)
            text_width2 = text_bbox2.width
            if text_width > region_width_pixels * .9:
                t.set_text('')
            else:
                t2.set_text('')
            if text_width2 > region_width_pixels * .8:
                t2.set_text('')
            # Center text in box
            t.set_x(df_cut.iloc[i]['Age_E'] - (df_cut.iloc[i]['Age_E'] - df_cut.iloc[i]['Age_S']) / 2)
            t2.set_x(df_cut.iloc[i]['Age_E'] - (df_cut.iloc[i]['Age_E'] - df_cut.iloc[i]['Age_S']) / 2)
            t.set_y(rank_dict[df_cut.iloc[i]['Rank']] * rank_width + rank_width / 2)
            t2.set_y(rank_dict[df_cut.iloc[i]['Rank']] * rank_width + rank_width / 2)
        else:
            _, y_pix1 = ax.transData.transform((0, df_cut.iloc[i]['Age_S']))
            _, y_pix2 = ax.transData.transform((0, df_cut.iloc[i]['Age_E']))
            region_height_pixels = abs(y_pix2 - y_pix1)
            text_bbox = t.get_window_extent(renderer=renderer)
            text_height = text_bbox.height
            text_bbox2 = t2.get_window_extent(renderer=renderer)
            text_height2 = text_bbox2.height
            if text_height > region_height_pixels * .9:
                t.set_text('')
            else:
                t2.set_text('')
            if text_height2 > region_height_pixels * .8:
                t2.set_text('')
            t.set_y(df_cut.iloc[i]['Age_E'] - (df_cut.iloc[i]['Age_E'] - df_cut.iloc[i]['Age_S']) / 2)
            t2.set_y(df_cut.iloc[i]['Age_E'] - (df_cut.iloc[i]['Age_E'] - df_cut.iloc[i]['Age_S']) / 2)
            t.set_x(rank_dict[df_cut.iloc[i]['Rank']] * rank_width + rank_width / 2)
            t2.set_x(rank_dict[df_cut.iloc[i]['Rank']] * rank_width + rank_width / 2)
            t2.set_y(df_cut.iloc[i]['Age_E'] - (df_cut.iloc[i]['Age_E'] - df_cut.iloc[i]['Age_S']) / 1.8)
            t.set_y(df_cut.iloc[i]['Age_E'] - (df_cut.iloc[i]['Age_E'] - df_cut.iloc[i]['Age_S']) / 2)

    return ax
    