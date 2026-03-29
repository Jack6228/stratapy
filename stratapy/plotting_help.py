"""
This module contains helper classes. The PlottingHelp class is used to store variables and functions which create and format plots; it is initialised within the stratapy.core.LogObject.plot() method and passed to the stratapy.plot.create_log() function.
The other three classes help to create custom legend features for stratapy plots.

The PlottingHelp class is imported into LogObject.plot() within stratapy.core. The other classes are used within PlottingHelp only.
"""

# Creating packages
from shapely.geometry import Point, Polygon as ShapelyPolygon
from shapely.ops import unary_union
from matplotlib.patches import Polygon, Rectangle
from .utils import colour_to_rgba, load_assets
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

class PlottingHelp:
    """
    This helper class stores all variables and functions related to plotting and has a range of methods to create the log.
    """

    def __init__(self, vars, display_mode, feature_mode, unit_borders, legend_loc, legend_columns, legend_border, fontsize, figsize, dpi, ppi, N, x_label, x_axis, y_label, y_axis_unit, spines, mineral_size, feature_size, xmax, x_ticks, x_tick_labels, legend_titles, legend_kwargs, grain_brackets) -> None:
        """
        Initialises the PlottingHelp class with all plotting variables and parameters
        """
        # Extract parameters from the vars object
        self.y_mode = vars.y_mode
        self.lithologies = vars.lithologies
        self.minerals_list = vars.minerals_list
        self.features = vars.features
        self.contact_types = vars.contact_types
        self.df = vars.df

        self.unit_borders = unit_borders
        self.x_ticks = x_ticks
        self.x_tick_labels = x_tick_labels
        self.xmax = xmax
        self.legend_border = legend_border
        self.fontsize = fontsize
        self.legend_titles = legend_titles
        self.legend_kwargs = legend_kwargs
        self.grain_brackets = grain_brackets

        # Collect parameters from the dataframe
        self.max_y_val, self.min_y_val = self.df['height/age'].max(), self.df['height/age'].min() - self.df.iloc[-1]['thickness']

        # Get the stylings and visualisations
        self.lithologies, self.minerals_list, self.features = load_assets(self.df, self.lithologies, self.minerals_list, self.features)

        # Set all of the default parameters for plotting
        self.dpi = dpi
        plt.rcParams.update({ 'figure.dpi': self.dpi})
        self.ppi = ppi
        # zorders
        self.zorder_unit = 1
        self.zorder_extras = len(self.df) + 10
        self.zorder_borders = self.zorder_extras + 10
        self.border_lw = .75  # Width of the outline around pacakges, no observation cross, etc.

        self.spines = spines
        self.mineral_size = mineral_size
        self.max_feature_width = feature_size

        self.N = N # number of points in the co-ordinate arrays for each edge of strata geometries, higher is more compute intensive

        self.x_label = x_label
        self.x_axis = x_axis
        self.y_label = y_label
        self.y_axis_unit = y_axis_unit

        self.figsize = figsize # Increasing the figure size will mean that hatching patterns will look denser
        self.display_mode = display_mode 
        self.feature_mode = feature_mode

        self.legend_loc = legend_loc
        self.legend_columns = legend_columns
        self.leg_box_size = 20
        self.max_x_grain = max(self.df['top_grain'].max(), self.df['bottom_grain'].max())

        # Depending on how lenses are to be displayed, either keep them in the lenses column or move them to the features column
        max_num_features_in_one_stratum = 0

        if self.feature_mode == 'default':
            # If wanting lenses to appear in the features column, prefix them with '^' and add to the features column (but keep them in the lenses column as well)
            for i, row in self.df.iterrows():
                lense_names = [l for l in row['lenses'].split(';') if l != '']
                mineral_names = [ l for l in row['minerals'].split(';') if l != '']
                feature_names = [f for f in row['features'].split(';') if f != '']
                # Remove trailing and leading whitespace
                lense_names = [l.strip() for l in lense_names]
                mineral_names = [m.strip() for m in mineral_names]
                feature_names = [f.strip() for f in feature_names]
                if row['features'] != '':
                    # Prefix existing features with '^' too, if they are in the lithologies dict
                    self.df.at[i, 'features'] = ';'.join([f'^{x}' if x in self.lithologies.keys() else x.strip() for x in row['features'].split(';') ])
                if row['lenses'] != '': 
                    if row['features'] != '':
                        # Then add the lenses
                        self.df.at[i, 'features'] += ';' + ';'.join([f'^{x}' for x in lense_names])
                    else:
                        self.df.at[i, 'features'] = ';'.join([f'^{x}' for x in lense_names])
                max_num_features_in_one_stratum = max(max_num_features_in_one_stratum, len(lense_names) + len(mineral_names) + len(feature_names))
        elif self.feature_mode == 'semi-merge':
            # If only having features in the column, then just get the maximum number of features in any given unit
            feature_lengths = [len(row['features'].split(';')) for _, row in self.df.iterrows() if row['features'] != '']
            max_num_features_in_one_stratum = max(feature_lengths) if feature_lengths else 0
        else:
            # If merging all features, minerals and lenses into the lithology, no features column is needed
            max_num_features_in_one_stratum = 0

        self.max_num_features_in_one_stratum = max_num_features_in_one_stratum

    def compute_stratum_polygon(self, unit_params, N, x_offset, x_left=0) -> list:
        """
        Creates a numpy array of xy co-ordinates for a closed polygon representing a rock package.

        Parameters:
        -----------
        unit_params : pandas.core.series.Series
            A pandas DataFrame row containing the parameters for the package.
        N : int, optional
            The number of points to be used for the package; higher value means more detailed package edges. Default is 100.
        x_offset : float
            The x-offset of the package, i.e., the width of the lithology column when using the column display mode. Otherwise should be 0 to display the full package.
        x_left : float, optional
            The x-coordinate of the left edge of the package. Default is 0 - only changed when generating the co-ords for a stratum without the lithology column in display mode.

        Returns:
        --------
        output : list
            A list of numpy arrays containing the co-ordinates of the full polygon, top edge, bottom edge, left edge and right edge of the package.
        """
        # Extract geometry
        y_upper = unit_params['height/age']
        if self.y_mode in ['age', 'depth']:
            y_lower = y_upper + unit_params['thickness']
        else:
            y_lower = y_upper - unit_params['thickness']
        x_right_top = unit_params['top_grain']
        x_right_bottom = unit_params['bottom_grain']
        cap_type = unit_params['connection_type']

        # If the x values are -1, this means that the no observation block should be auto-sized depending on display_mode
        if x_right_top == -1:
            if self.display_mode in ['grainsize', 'log']:
                x_right_top, x_right_bottom = 0, 0
            elif self.display_mode == 'default':
                # For default, set to 50% of the min grain size, or 10% of max grain size if min is 0
                min_grain = min(self.x_ticks) if self.x_ticks else 0
                if min_grain == 0:
                    x_right_top, x_right_bottom = 0.1 * self.max_x_grain, 0.1 * self.max_x_grain
                else:
                    x_right_top, x_right_bottom = 0.5 * min_grain, 0.5 * min_grain

        # Override the x_right values if using the lithology column display mode
        if x_offset != 0:
            x_right_top, x_right_bottom = x_offset, x_offset

        # First create the lower bound of the rock package
        x_bottom = np.linspace(x_left, x_right_bottom, N, endpoint=True)
        # Use sine or cosine wave depending on magnitude of the erosion
        if unit_params['erosion_bottom'] >= 0:
            y_bottom = unit_params['erosion_bottom'] * np.sin(unit_params['freq_bottom'] * np.pi * x_bottom) + y_lower
        else:
            y_bottom = abs(unit_params['erosion_bottom']) * np.sin(unit_params['freq_bottom'] * np.pi * x_bottom - np.pi) + y_lower

        xy_bottom = np.array([x_bottom, y_bottom]).T

        # Then the upper bound
        x_top = np.linspace(x_left, x_right_top, N, endpoint=True)
        # Again, depending on magnitude of erosion, use sine or cosine wave
        if unit_params['erosion_top'] >= 0:
            y_top = unit_params['erosion_top'] * np.sin(unit_params['freq_top'] * np.pi * x_top) + y_upper
        else:
            y_top = abs(unit_params['erosion_top']) * np.sin(unit_params['freq_top'] * np.pi * x_top - np.pi) + y_upper
        xy_top = np.array([x_top, y_top]).T

        # Vertical line at on the left of the package
        xy_left = np.array([np.full(N, x_left), np.linspace(y_lower, y_upper, N, endpoint=True)]).T

        # And finally the connection between the top and bottom of the package. Default to vertical line for the column display mode (i.e. where offset is 0)
        if cap_type in ['concave', 'convex'] and x_offset == 0:
            xy_right = np.array( self.cap_parabolic(y_top[-1], y_bottom[-1], x_right_top, x_right_bottom, cap_type, N=N) ).T
        elif 'sawtooth' in cap_type and x_offset == 0:
            xy_right = np.array( self.cap_sawtooth(cap_type, y_top[-1], y_bottom[-1], x_right_bottom, 3) ).T
        else:
            xy_right = np.array( [np.linspace(x_right_top, x_right_bottom, N), np.linspace(y_top[-1], y_bottom[-1], N, endpoint=True)] ).T

        # Combine points in the correct order to complete the polygon (depending on the sine wave direction)
        # Tag each point with its side
        tagged_bottom = [(x, y, 'bottom') for x, y in xy_bottom[::-1]]
        tagged_left   = [(x, y, 'left')   for x, y in xy_left]
        tagged_top    = [(x, y, 'top')    for x, y in xy_top]
        tagged_right  = [(x, y, 'right')  for x, y in xy_right]

        # Combine all points
        tagged_points = tagged_bottom + tagged_left + tagged_top + tagged_right
        stratum_points = np.array([(x, y) for x, y, _ in tagged_points])

        # Filter to only the main region (in case of geometry which creates overlapping regions, take the largest)
        try:
            p_x, p_y = unary_union([ShapelyPolygon(stratum_points).buffer(0)]).exterior.xy
            filtered_points = list(zip(p_x, p_y))
        except:
            filtered_points = [tuple(pt) for pt in stratum_points]

        # Keep only tagged points that are in the filtered polygon
        filtered_tagged_points = [pt for pt in tagged_points if (pt[0], pt[1]) in filtered_points]

        # Separate back into sides, preserving order
        xy_bottom_f = np.array([[x, y] for x, y, side in filtered_tagged_points if side == 'bottom'])
        xy_left_f   = np.array([[x, y] for x, y, side in filtered_tagged_points if side == 'left'])
        xy_top_f    = np.array([[x, y] for x, y, side in filtered_tagged_points if side == 'top'])
        xy_right_f  = np.array([[x, y] for x, y, side in filtered_tagged_points if side == 'right'])

        # The full polygon
        stratum_points_f = np.array(filtered_points)

        # Output: [full polygon, top, bottom, left, right]
        return [stratum_points_f, xy_top_f, xy_bottom_f, xy_left_f, xy_right_f]

    def compute_unit_polygons(self, unit_params, x_offset, N) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
        """
        Creates polygons for strata to be displayed. Output varies depending on display mode: for default, all returns three identical instances of the polygon, for the lithology column mode, returns three polygons: (image filled column region, complete region of column and stratum, stratum only without column).

        Parameters:
        -----------
        unit_params : pandas.core.series.Series
            A pandas DataFrame row containing the parameters for the package.
        x_offset : float
            The x-offset of the package, i.e., the width of the lithology column when using the column display mode. Otherwise should be 0 to display the full package.
        N : int, optional
            The number of points to be used for the package; higher value means more detailed package edges.

        Returns:
        --------
        points : list
            A list of length three with the co-ordinates - details of each as given in the function description.
        """
        # Regardless of the display mode, create the polygon for the part of the package that will be filled
        stratum_points = self.compute_stratum_polygon(unit_params, N, x_offset)
        # Now, if the display mode is for the lithology column, we need to create polygons for the package, package incl. column and without the column
        if x_offset != 0:
            # Co-ords for the full stratum (i.e. the package + column) by setting the x_offset to 0
            col_and_stratum_points = self.compute_stratum_polygon(unit_params, N, x_offset=0)
            # And for the stratum without the column (x_offset is zero as not using the lithology column, x_left is the x_offset)
            stratum_only_points = self.compute_stratum_polygon(unit_params, N, x_offset=0, x_left=x_offset) 
            return stratum_points, col_and_stratum_points, stratum_only_points
        else:
            return stratum_points, stratum_points, stratum_points

    def cap_sawtooth(self, cap_type, y_lower, y_upper, x_right_bottom, N_teeth, max_x_dev=0.3) -> tuple[list, list]:
        """
        Creates an x and y array of co-ordinates for a sawtooth edge on the right side of the stratum.
        
        Parameters:
        -----------
        cap_type : str
            The type of sawtooth connection, either 'sawtooth_top' or 'sawtooth_bottom'.
        y_lower : float
            The y-coordinate of the lower edge of the stratum.
        y_upper : float
            The y-coordinate of the upper edge of the stratum.
        x_right_bottom : float
            The x-coordinate of the bottom right edge of the stratum.
        N_teeth : int
            The number of teeth in the sawtooth pattern.
        max_x_dev : float
            The maximum x deviation of the sawtooth from the right edge. Default is 0.3.

        Returns:
        --------
        x : list
            The x-coordinates of the sawtooth edge.
        y : list
            The y-coordinates of the sawtooth edge.
        """
        # Calculate new x and y points to trace a sawtooth, bottom to top
        # For x, create a list of length 2*N_teeth + 1 alternating between start[0] and start[0] + max_x_dev
        x = [x_right_bottom if i % 2 == 0 else x_right_bottom + max_x_dev for i in range(2 * N_teeth + 1)]
        if cap_type == 'sawtooth':
            # For y, create a list of length 2*N_teeth + 1 with one point at y_lower and two at every notch
            y = [y_lower if i == 0 else val for i in range(N_teeth + 1) for val in ([y_lower + i * (y_upper - y_lower) / N_teeth] * (2 if i > 0 else 1))]
        else:
            # For y, create a list of length 2*N_teeth + 1 with two points at every notch and one at y_upper
            y = [y_upper if i == 2 * N_teeth else val for i in range(N_teeth + 1) for val in ([y_lower + i * (y_upper - y_lower) / N_teeth] * (2 if i < N_teeth else 1))]
        
        return x, y

    def cap_parabolic(self, y_lower, y_upper, x_right_top, x_right_bottom, side, N=100) -> tuple[np.ndarray, np.ndarray]:
        """
        Creates an x and y array of co-ordinates for the right edge of the stratum.

        Parameters:
        -----------
        y_lower : float
            The y-coordinate of the lower edge of the stratum.
        y_upper : float
            The y-coordinate of the upper edge of the stratum.
        x_right_top : float
            The x-coordinate of the top right edge of the stratum.
        x_right_bottom : float
            The x-coordinate of the bottom right edge of the stratum.
        side : str
            The type of parabolic connection, either 'concave' or 'convex'.
        N : int
            The number of points to be used for the parabolic edge. Default is 100.

        Returns:
        --------
        parabolic : np.ndarray
            The x-coordinates of the parabolic edge.
        y : np.ndarray
            The y-coordinates of the parabolic edge.
        """
        # Create y array
        y = np.linspace(y_lower, y_upper, N)
        # Compute parabolic curve for convex or concave
        if side == 'concave':
            parabolic = -np.sin(np.pi * (y - y_lower) / (y_upper - y_lower)) / 10 + min(x_right_bottom, x_right_top)
        else:
            parabolic = np.sin(np.pi * (y - y_lower) / (y_upper - y_lower)) / 10 + min(x_right_bottom, x_right_top)
        # Determine x array
        x = np.linspace(x_right_top, x_right_bottom, N) - min(x_right_top, x_right_bottom)
        # Add slant to the parabolic curve 
        parabolic += x
        return parabolic, y

    def display_stratum(self, fig, ax, poly_verts, key=None, fmt=None, border=False, ppi=50, zorder=1, lens=False) -> None:
        """
        Plots a specified polygon with the desired formatting.
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            The figure to draw on
        ax : matplotlib.axes.Axes
            The axes to draw on
        poly_verts : array-like
            Array of x-y co-ordinates of the polygon to be plotted, shape (N x 2)
        key : str
            The key of the lithology/mineral/feature/no observation to be plotted.
        fmt : tuple
            The formatting tuple for the polygon to be plotted, as given by the relevant asset dictionary.
        border : bool
            Whether the default border of the region being plotted should be drawn. Default to False, meaning edgecolor is 'none', True changes it to 'k' (black).
        ppi : int
            Pixels per inch for the image
        zorder : int
            Which layer to plot the polygon on. Defaults to 1.
        lens : bool
            Whether the polygon being drawn is for a lens feature. Default is False. If True, an additional white polygon of the lens is drawn behind the main polygon to cover any underlying patterns in the event where the pattern fill is transparent.

        Returns:
        --------
        None
        """
        # If no observation - draw cross
        if key.lower() == 'no':
            # Create a polygon patch with the desired formatting
            ax.fill(poly_verts[:, 0], poly_verts[:, 1], color=fmt[1], hatch=fmt[2], edgecolor='k', lw=.5, zorder=zorder, alpha=0)
            # And draw lines
            x_min, y_min = poly_verts.min(axis=0)
            x_max, y_max = poly_verts.max(axis=0)
            # Draw lines at the top and bottom of the polygon
            ax.plot([x_min, x_max], [y_max, y_min], color='k', lw=self.border_lw, zorder=self.zorder_extras)
            ax.plot([x_min, x_max], [y_min, y_max], color='k', lw=self.border_lw, zorder=self.zorder_extras)

        # Else if a fill pattern
        elif fmt[0] == 'fill':
            # Create a polygon patch with the desired formatting
            ax.fill(poly_verts[:, 0], poly_verts[:, 1], color=fmt[1], hatch=fmt[2], edgecolor=fmt[3], lw=self.border_lw, zorder=zorder)

        # Otherwise (lithologies and patterns)
        else:
            # Load the image
            image_data = fmt[1]

            # Create Polygon patch
            edgecol = 'k' if border else 'none'
            poly = Polygon(poly_verts, closed=True, facecolor='none', edgecolor=edgecol, zorder=zorder)
            ax.add_patch(poly)
            
            # Get polygon bounding box
            x0, y0 = poly_verts.min(axis=0)
            x1, y1 = poly_verts.max(axis=0)
            poly_width = x1 - x0
            poly_height = y1 - y0
            
            # Get the size of the axis in inches
            ax_width, ax_height = ax.get_window_extent().size / fig.dpi
            x_lims, y_lims = ax.get_xlim(), ax.get_ylim()
            y_lims = sorted(y_lims)  # Ensure y-limits are in correct order

            # Create a transformation to scale the data coordinates to inches
            transform_ax2inch = [ax_width / (x_lims[1] - x_lims[0]), ax_height / (y_lims[1] - y_lims[0])]
            transform_inch2ax = [1 / transform_ax2inch[0], 1 / transform_ax2inch[1]]

            # Now get the size of the polygon, also in inches
            poly_width_inch = poly_width * transform_ax2inch[0]
            poly_height_inch = poly_height * transform_ax2inch[1]
            
            # Get the aspect ratio of the image
            img_height, img_width = image_data.shape[:2]
            
            # Create a custom transform from pixels to inches - a larger number means a smaller image and more tiles needed
            transform_px2inch = 1/ppi  # Assuming ppi pixels per inch for both x and y (e.g. just under swatches)
            
            # Convert the image to inches
            img_width_inch = img_width * transform_px2inch
            img_height_inch = img_height * transform_px2inch

            # Determine how many images are needed to be tiled to fill the polygon area
            x_tile_count = int(np.ceil(poly_width_inch / img_width_inch))
            y_tile_count = int(np.ceil(poly_height_inch / img_height_inch))

            # Tile the image to fill the polygon area; the number of values in the tile tuple must equal the number of dimensions in the image data, so add 1's if image is not 2D
            if len(image_data.shape) == 2:
                # If the image is 2D, tile it as is
                tiled_image = np.tile(image_data, (y_tile_count, x_tile_count))
            else:
                tpl = (y_tile_count, x_tile_count) + (1,) * (len(image_data.shape) - 2)
                tiled_image = np.tile(image_data, tpl)

            # Compute the extent of the image in data coordinates - the image should be centered horizontally, and vertically aligned to the top
            tiled_image_width = img_width * x_tile_count
            tiled_image_height = img_height * y_tile_count
            # Convert from pixels to data coordinates
            tiled_image_width_data = tiled_image_width * transform_px2inch * transform_inch2ax[0]
            tiled_image_height_data = tiled_image_height * transform_px2inch * transform_inch2ax[1]
            # Align
            x_left = x0 + (poly_width - tiled_image_width_data) / 2 # Align to the center of the polygon
            x_right = x_left + tiled_image_width_data
            y_top = y0 + poly_height  # Align to the top of the polygon
            y_bottom = y_top - tiled_image_height_data
            extent = (x_left, x_right, y_bottom, y_top)

            # If the formatting is of lenth 2, it is a FGDC lithology, so use grey_r cmap, otherwise (len 3) it is a pattern, so use the desired cmap
            cmap = fmt[2]

            # Create image artist with explicit extent
            from matplotlib.image import AxesImage
            img = AxesImage(ax, origin=self.imshow_origin, extent=extent, cmap=cmap, zorder=zorder)  # Ensure image is above polygon
            
            # Set image data
            img.set_array(tiled_image)
            
            # Clip image to polygon
            img.set_clip_path(poly)
            
            # Add image to axes
            ax.add_image(img)

            # Draw background polygon if needed - only when lenses are on top of units (feature_mode is not 'default')
            if lens and self.feature_mode != 'default':
                # Draw a white polygon behind the main polygon to cover any underlying patterns
                ax.fill(poly_verts[:, 0], poly_verts[:, 1], color='none', edgecolor='none', zorder=zorder-1)

    def compute_feature_positions(self, N) -> np.ndarray:
        """
        Distributes N features evenly across the feature display area.

        Parameters:
        -----------
        N : int
            The number of features to distribute.

        Returns:
        --------
        arr : np.ndarray
            An array of x-coordinates for the center of each feature.
        """
        # By default each feature is the specified width, with 20% padding (10% each side)
        left = self.divider_x
        right = self.x_axis_max
        # Compute l and r width padding, assuming maxN
        width = self.max_feature_width
        spacing = self.spacing
        # Compute total width occupied by features and form the array
        mpd = (spacing + width) * (self.max_num_features_in_one_stratum - N)  # total width of all features, including spacing
        arr = np.linspace(left+mpd/2+spacing/2, right-mpd/2-spacing/2, N, endpoint=False) + (width+spacing)/2
        return arr    

    def display_feature(self, fig, ax, image_data, x_pos, center_y, max_width, max_height) -> None:
        """
        Displays a feature image on a matplotlib axis at a specified position and size, with optional "broken" line overlay.
        
        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The matplotlib figure object containing the axis.
        ax : matplotlib.axes.Axes
            The axis on which to display the image.
        image_data : str
            The key for the feature image in `self.features`. If prefixed with '/', a diagonal "broken" line is drawn over the image.
        x_pos : float
            The x-coordinate (in data units) for the center of the image.
        center_y : float
            The y-coordinate (in data units) for the center of the image.
        max_width : float
            The maximum allowed width (in data units) for the image.
        max_height : float
            The maximum allowed height (in data units) for the image.
        
        Returns
        -------
        None
        
        Notes
        -----
        - The image is scaled to fit within the specified width and height, preserving its aspect ratio.
        - If `image_data` is prefixed with '/', a diagonal "broken" line is drawn over the image to indicate a discontinuity.
        - Handles grayscale, RGB, and RGBA images, preserving their data types and value ranges.
        """
        # Check if it is prefixed by '/' for broken line
        if image_data.startswith('/'):
            broken = True
            image_data = image_data[1:]  # Remove the prefix
        else:
            broken = False
        
        # Get the image array
        image_data = self.features[image_data][1]
        # Find the aspect ratio of the image
        img_height, img_width = image_data.shape[:2]
        img_aspect = img_width / img_height
        
        # Get the transform from data units to inches
        ax_size_du = [self.total_x_width, self.total_y_height]
        ax_aspect_du = ax_size_du[0] / ax_size_du[1]        # aspect ratio in data units
        # Aspect ratio of the axis in inches
        bbox = ax.get_position()
        fig_width, fig_height = fig.get_size_inches()
        ax0_width = bbox.width * fig_width
        ax0_height = bbox.height * fig_height
        ax_aspect_inches = ax0_width / ax0_height
        # Compute the overall aspect ratio for the image to be plotted by combining data unit, inches, and image aspect ratios
        aspect_combined = ax_aspect_du * img_aspect / ax_aspect_inches

        # Ensure that the image fits in the desired box
        # Must be less than max height
        final_width = max_height * aspect_combined
        # Must be less than max width
        if final_width > max_width:
            final_width = max_width
            max_height = final_width / aspect_combined
        left = x_pos - final_width / 2
        right = x_pos + final_width / 2
        bottom = center_y - max_height / 2
        top = center_y + max_height / 2
        if self.y_mode in ['depth', 'age']:
            top, bottom = sorted([top, bottom])  # Ensure top is always greater than bottom
        extent = (left, right, bottom, top)

        # Create a 2D array with 1's along the diagonal and 0's elsewhere
        if broken:
            # Set line width to 1/86th of the image width
            eye_width = max(1, int(img_width / 86))  # Ensure the line width is at least 1 pixel

            # Create a boolean mask for the anti-diagonal band of width (2*eye_width+1)
            rows, cols = np.ogrid[:img_height, :img_width]
            diag = np.abs(rows + cols - (img_width - 1)) <= eye_width

            # Ensure original image isn't modified
            img_cp = image_data.copy()

            # Handle grayscale, RGB and RGBA consistently and respect dtype/value range
            if img_cp.ndim == 2:
                # grayscale
                if np.issubdtype(img_cp.dtype, np.floating):
                    img_cp[diag] = 0.0
                else:
                    img_cp[diag] = 0
            else:
                # RGB/RGBA: set RGB channels to black
                black_val = 0.0 if np.issubdtype(img_cp.dtype, np.floating) else 0
                for c in range(3):
                    img_cp[..., c][diag] = black_val

                # If RGBA, make the line fully opaque
                if img_cp.shape[2] == 4:
                    alpha_val = 1.0 if np.issubdtype(img_cp.dtype, np.floating) else 255
                    img_cp[..., 3][diag] = alpha_val
        else:
            img_cp = image_data

        self.place_image_extent(ax, img_cp, extent=extent)

    def place_image_extent(self, ax, img_array, extent, zorder=10):
        """
        Places an image on the given axes with the specified extent in data coordinates, using BboxImage for efficient rendering.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes on which to place the image.
        img_array : np.ndarray
            The image data as a numpy array.
        extent : tuple
            A tuple (left, right, bottom, top) specifying the extent of the image in data coordinates.
        zorder : int
            The z-order for the image artist. Default is 10 to ensure it is above most other elements.

        Returns
        -------
        None
        """
        # Unpack based on imshow order: (left, right, bottom, top)
        l, r, b, t = extent
        
        # Map: left -> xmin, bottom -> ymin, right -> xmax, top -> ymax
        bbox_data = Bbox.from_extents(l, b, r, t)
        
        bbox_trans = TransformedBbox(bbox_data, ax.transData)
        
        # Use interpolation='nearest' for maximum speed
        image_artist = BboxImage(bbox_trans, interpolation='nearest', zorder=zorder)
        image_artist.set_data(img_array)
        # Ensure clip_on to dislay on top of axis
        image_artist.set_clip_on(False)
        
        ax.add_artist(image_artist)

    def populate_features_column(self, fig, ax, row, geom) -> None:
        """
        Place features and lenses in the features column of the log.
        
        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The matplotlib figure object to plot on.
        ax : matplotlib.axes.Axes
            The matplotlib axes object to plot on.
        row : pandas.core.series.Series
            A pandas DataFrame row containing the stratum data, including features and minerals.
        geom : np.ndarray
            The co-ordinates of the stratum polygon.
        
        Returns
        -------
        None
        """
        # Get the features in this stratum
        features_to_plot = str(row['features']).split(';') 
        # If the lense mode is 'default', add the minerals to the features to plot
        if self.feature_mode == 'default':
            features_to_plot += str(row['minerals']).split(';')
        # Remove any empty strings
        features_to_plot = [f for f in features_to_plot if f != '']
        # Now plot all of the features, with a max height of the thickness of this stratum

        # Ensure that max_height is at least the minimum value
        max_width = self.max_feature_width
        max_height = self.total_y_height / 10

        # Correct y-value for the erosion and y-axis mode
        min_y, max_y =  geom[0][:, 1].min(), geom[0][:, 1].max()
        erosion_bottom = row['erosion_bottom']
        erosion_top = row['erosion_top']
        if self.y_mode in ['depth', 'height']:
            min_y = min_y + 2*abs(erosion_bottom)
            max_y = max_y - 2*abs(erosion_top)
        else:
            min_y = min_y - 2*abs(erosion_top)
            max_y = max_y + 2*abs(erosion_bottom)

        center_y = (min_y + max_y) / 2
        max_height = 0.8*(max_y - min_y)  # Ensure the feature fits within the stratum height
        max_height = 1e3 # A ludicrously high value to ensure features always fit

        x_vals = self.compute_feature_positions(len(features_to_plot))

        for i, image_data in enumerate(features_to_plot):

            # Get the position of this feature
            x_pos = x_vals[i]
            
            # If '^' is in the feature's name, plot the outline and fill with the desired hatch pattern, otherwise, imshow the desired image
            if image_data.startswith('^'):
                lens = self.compute_lens_polygon(ax, x_pos - max_width/2, x_pos + max_width/2, center_y - max_height/2, center_y + max_height/2)
                self.display_stratum(fig, ax, lens[0], key=image_data[1:], fmt=self.lithologies[image_data[1:]], border=True, ppi=self.ppi*2, lens=True)

            else:
                # If a mineral
                if image_data in self.minerals_list.keys() and len(self.minerals_list[image_data]) == 3:
                    if self.feature_mode == 'default':
                        fmt = self.minerals_list[image_data]
                        # Plot a triangle of three scatter points centered at (4, 150)
                        height = max_height
                        ratio = self.total_x_width / self.total_y_height
                        width = (height * ratio) / np.tan(np.deg2rad(60)) * 2
                        # If the width is larger than the max_width, set it to the max_width and recompute the height
                        scale = .65 # scaling the minerals to be smaller than the features, accounting for mineral size
                        if width > max_width*scale:
                            width = max_width*scale
                            height = (width/2) * np.tan(np.deg2rad(60)) / ratio
                        
                        # Adjust height to fit
                        height *= .75

                        midpt = (x_pos, center_y)
                        # Ensure that the two values are the lower value
                        if self.y_mode in ['depth', 'age']:
                            triangle_y = [midpt[1] + height / 2, midpt[1] - height / 2, midpt[1] + height / 2]
                        else:
                            triangle_y = [midpt[1] - height / 2, midpt[1] + height / 2, midpt[1] - height / 2]

                        triangle_x = [midpt[0] - width / 2, midpt[0], midpt[0] + width / 2]
                        # Auto increase the mineral size for feature mode
                        ax.scatter(triangle_x, triangle_y, color=fmt[0], marker=fmt[2], s=self.mineral_size, edgecolor=fmt[1], zorder=3)
                else:
                    self.display_feature(fig, ax, image_data, x_pos, center_y, max_width, max_height)
            
    def fig_setup(self, fig, ax, override_ylims) -> tuple["matplotlib.figure.Figure", "matplotlib.axes.Axes"]:
        """
        Sets up the figure and axes for plotting, including y-axis limits and labels based on the specified y-mode.

        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            The figure to draw on. If None, a new figure will be created.
        ax : matplotlib.axes.Axes
            The axes to draw on. If None, new axes will be created.
        override_ylims : tuple, optional
            A tuple specifying the y-axis limits to override the default limits (used for multi_fig operations).

        Returns:
        --------    
        fig : matplotlib.figure.Figure
            The figure to draw on.
        ax : matplotlib.axes.Axes
            The axes to draw on.
        """
        if fig is None or ax is None:
            fig, ax = plt.subplots(1, 1, figsize=self.figsize)

        # Set the left bound of the strata
        x_offset = 0
        self.imshow_origin = 'lower'

        # Infer y-axis unit from y_mode if not specified
        if self.y_axis_unit == '':
            if self.y_mode == 'age':
                self.y_axis_unit = 'Ma'
            else:
                self.y_axis_unit = 'm'

        # Set axis properties based on y_mode
        if self.y_mode == 'age':
            if self.y_label == None:
                self.y_label = 'Age'
            if self.y_label == '':
                y_label = ''
            else:
                y_label = f'{self.y_label} ({self.y_axis_unit})'
            invert = False
            self.y_limits = (self.df['height/age'].min(), self.df['height/age'].max() + self.df.iloc[-1]['thickness']) 
            if override_ylims is not None:
                y_limits = override_ylims
            else:
                y_limits = self.y_limits
            ax.set_ylim(y_limits)
            ax.invert_yaxis()

        elif self.y_mode == 'height':
            if self.y_label == None:
                self.y_label = 'Height'
            if self.y_label == '':
                y_label = ''
            else:
                y_label = f'{self.y_label} ({self.y_axis_unit})'
            invert = False
            self.y_limits = (self.df['height/age'].min() - self.df.iloc[-1]['thickness'], self.df['height/age'].max()) 
            if override_ylims is not None:
                y_limits = override_ylims
            else:
                y_limits = self.y_limits
            ax.set_ylim(y_limits)
            self.imshow_origin = 'upper'

        elif self.y_mode == 'depth':
            if self.y_label == None:
                self.y_label = 'Depth'
            if self.y_label == '':
                y_label = ''
            else:
                y_label = f'{self.y_label} ({self.y_axis_unit})'
            invert = False
            self.df['height/age'] = self.df['height/age'] * -1
            self.y_limits = (self.df['height/age'].min(), self.df['height/age'].max() + self.df.iloc[-1]['thickness']) 
            if override_ylims is not None:
                y_limits = override_ylims
            else:
                y_limits = self.y_limits
            ax.set_ylim(y_limits)
            ax.invert_yaxis()
        
        # Get the highest used grain size
        largest_grain_size = max(self.df['bottom_grain'].max(), self.df['top_grain'].max())
        # Find the grain x label which encloses the largest value (i.e. if value is 5, it will be the tick at 5, if value is 5.01, it will go to the one above, i.e. 6 [by default])
        largest_grain_value_to_display_idx = next((i for i, val in enumerate(self.x_ticks) if val >= largest_grain_size), -1)

        # Determine the grain size axis values
        if self.display_mode == 'log':
            # For log mode, no grain sizes are shown, so set max_x to 0 and set all of the connection_types in the dataframe to ''
            x_max = 0
            self.df['connection_type'] = ''
        elif (largest_grain_size < max(self.x_ticks)) :
            # If largest grain is not the above but lower than the highest, ensure max_x is set to the grain size after this value
            x_max = self.x_ticks[largest_grain_value_to_display_idx]
        else:
            # If largest grain size is >= the largest value in self.x_ticks_dict, then it is what it is
            x_max = largest_grain_size

        # Trim the x-axis to only display relevant grain sizes, accounting for if user desires a custom xmax
        if self.xmax is not None:
            x_max = self.xmax
        self.x_ticks = [x for x in self.x_ticks if x <= x_max]
        self.x_tick_labels = [self.x_tick_labels[self.x_ticks.index(x)] for x in self.x_ticks]

        # Create the bounds (if neccessary) for the lithology column and features column, and their tick labels
        if self.display_mode == 'grainsize':
            self.lithology_column_thickness = 1.5
        elif self.display_mode == 'log':
            self.lithology_column_thickness = 4
        else:
            self.lithology_column_thickness = 0

        # Adjust x-positions for the lithology column thickness
        self.max_x_grain += self.lithology_column_thickness   # Max grain size position
        x_max += self.lithology_column_thickness              # User requested max x position
        x_offset += self.lithology_column_thickness           # Units' x offset

        if self.display_mode == 'grainsize':
            # Adjust x-tick positions for the lithology column (incl. new first tick for the column itself)
            self.x_ticks = [self.lithology_column_thickness/2] + [x + self.lithology_column_thickness for x in self.x_ticks]
            # Replace the first tick label with the Lithology label
            self.x_tick_labels = ['Lithology'] + self.x_tick_labels
            # Draw vertical lithology column line only between y_limits, not full axis
            ax.axvline(x=self.lithology_column_thickness, color='black', lw=self.border_lw, zorder=self.zorder_extras)
            # If x_offset isn't 0, adjust grain sizes
            self.df.loc[self.df['top_grain'] > 0, 'top_grain'] += x_offset
            self.df.loc[self.df['bottom_grain'] > 0, 'bottom_grain'] += x_offset
            
        elif self.display_mode == 'log':
            # Adjust x-ticks
            self.x_ticks = [0, self.lithology_column_thickness]
            self.x_tick_labels = ['', '']
            self.df['top_grain'] = self.lithology_column_thickness
            self.df['bottom_grain'] = self.lithology_column_thickness

        # Define spacing between features and/or borders
        self.spacing = .1

        # Compute spacing for the features column based on the max number in one stratum
        if self.max_num_features_in_one_stratum > 0:
            
            # Determine where the divider between units and features column goes
            if self.display_mode == 'log':
                divider_x = x_max
            else:
                divider_x = x_max + 3 * self.spacing

            # Compute the absolute maximum value of x-axis (incl. column); each feature uses 'max_width' space, with 'spacing' of padding either side.
            x_axis_max = divider_x + (self.max_num_features_in_one_stratum * self.max_feature_width) + (self.max_num_features_in_one_stratum + 1) * self.spacing

        else:
            # If no features, just add a small amount of padding, unless log mode
            if self.display_mode != 'log':
                # Adding double the spacing here to allow more room for units, e.g. if a convex cap is used
                x_axis_max = x_max# + 3 * self.spacing
            else:
                x_axis_max = x_max
            # Ensure x_divider is at the end of the x-axis
            divider_x = x_axis_max

        # Set the axes labels, limits, ticks; if there are grain brackets, add padding to the x_label
        x_label_padding = 10 if not self.grain_brackets else 25
        ax.set_xlabel(self.x_label, labelpad=x_label_padding, fontsize=self.fontsize['x_axis_label'])
        ax.set_ylabel(y_label, labelpad=10, fontsize=self.fontsize['y_axis_label'])
        ax.set_xticks(self.x_ticks)
        ax.set_xticklabels(self.x_tick_labels, fontsize=self.fontsize['x_tick_labels'])
        ax.set_xlim(0, x_axis_max)
        # Also set y tick label font size
        ax.tick_params(axis='y', labelsize=self.fontsize['y_tick_labels'])

        self.xmax = x_max                  # The maximum x value for grain sizes
        self.divider_x = divider_x         # Divider between units and features column
        self.x_axis_max = x_axis_max       # Absolute maximum x value for the axis
        self.x_offset = x_offset           # Offset for the units' left bounds
        self.invert = invert
        self.total_y_height = abs(y_limits[1] - y_limits[0])
        self.total_x_width = float(ax.get_xlim()[1] - ax.get_xlim()[0])

        # Set mineral size using axis range
        _, ax_height = ax.get_window_extent().size
        # Convert from inches to points
        mineral_size = ax_height * 4 / self.dpi
        # Adjust based on parameter
        self.mineral_size *= mineral_size

        return fig, ax

    def display_minerals(self, ax, unit_bounds, unit_params, y_sep=None, x_sep=0.8) -> None:
        """
        Plots desired minerals in a given stratum in a offset pattern to fill the unit. Will only display minerals within a unit, if they are displayed within the features column, PlottingHelp.populate_features_column() handles this.

        Parameters:
        -----------
        ax : matplotlib.axes.Axes
            The axes to draw on
        unit_bounds : array-like
            Array of x-y co-ordinates of the polygon to be plotted, shape (N x 2)
        unit_params : dict
            Properties of the stratum, e.g., minerals, thickness etc.
        y_sep : float
            Vertical separation between minerals. If None, it is set to 1/30th of the total y-height of the figure.
        x_sep : float
            Horizontal separation between minerals. Default to 0.8 data units.
        
        Returns:
        --------
        None
        """
        # Determine geometry of the unit
        if self.y_mode == 'height':
            min_y = unit_params['height/age'] - unit_params['thickness']
            max_y = unit_params['height/age']
        else:
            min_y = unit_params['height/age']
            max_y = min_y + unit_params['thickness']
        
        # Create a numpy array of positions within the polygon bounds
        if self.x_offset != 0:
            # If a lithology column is present, only go up to its bound, with only 3 points
            mineral_x = np.linspace(0, self.x_offset, 3)
        else:
            # Otherwise, fill the entire stratum with minerals, with a separation of x_sep and at least 3 points
            N = max( int((self.max_x_grain-self.x_offset)/x_sep), 3)
            mineral_x = np.linspace(self.x_offset, self.max_x_grain, N)

        # Compute y separations if needed
        if y_sep is None:
            y_sep = self.total_y_height / 30 

        # Create y positions
        mineral_y = np.arange(min_y, max_y, y_sep) + (y_sep)/2

        # Convert to a 2D grid and keep only points within the geometry
        X, Y = np.meshgrid(mineral_x, mineral_y)
        polygon = ShapelyPolygon(unit_bounds)
        # Define the radius of the scatter points in data units
        scatter_radius = min(0.15, self.total_y_height / 70)

        # Offset odd rows by half the x spacing - using either even or odd rows, depending on which results in the most use of space by the minerals
        num_minerals_plotted = []
        x_sep = mineral_x[1] - mineral_x[0]
        for row in [0, 1]:
            if row % 2 == 0:
                X1, Y1 = X.copy(), Y.copy()
                X1[row::2] += x_sep / 2
            else:
                X1, Y1 = X.copy(), Y.copy()
                X1[row::2] += x_sep / 2
            # Check if the scatter points are fully enclosed in the polygon
            mask = np.array([ polygon.contains(Point(x, y).buffer(scatter_radius)) for x, y in zip(X1.flatten(), Y1.flatten()) ])
            # Filter the points based on the mask
            X1, Y1 = X1.flatten()[mask], Y1.flatten()[mask]
            num_minerals_plotted.append(len(X1))

        # Use the best one
        X[np.argmax(num_minerals_plotted)::2] += x_sep / 2
        # Check if the scatter points are fully enclosed in the polygon
        mask = np.array([ polygon.contains(Point(x, y).buffer(scatter_radius)) for x, y in zip(X.flatten(), Y.flatten()) ])
        # Filter the points based on the mask
        X, Y = X.flatten()[mask], Y.flatten()[mask]

        # Get the minerals to be plotted
        minerals = str(unit_params['minerals']).split(';')
        # Remove trailing and leading whitespace
        minerals = [m.strip() for m in minerals if m.strip() in self.minerals_list.keys()]
        N = len(minerals)

        # Create a scatter plot with the filtered points
        legend_scatter_handles = {}
        for i in range(N):
            point_color = self.minerals_list[minerals[i]][0]
            point_marker = self.minerals_list[minerals[i]][2]
            point_edge = self.minerals_list[minerals[i]][1]
            point_label = minerals[i]
            ax.scatter(X[i::N], Y[i::N], color=point_color, marker=point_marker, s=self.mineral_size, edgecolor=point_edge, zorder=self.zorder_extras, label=point_label)
            legend_scatter_handles[minerals[i]] = plt.Line2D([], [], color=point_color, marker=point_marker, linestyle='None', label=point_label)

    def display_merged_features(self, fig, ax, row, geom) -> None:
        """
        Displays the lenses (and features if merge mode) for a given stratum in the unit itself.
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            The figure to draw on.
        ax : matplotlib.axes.Axes
            The axes to draw on.
        row : pandas.Series
            The row of the dataframe corresponding to the stratum.
        geom : np.ndarray
            The coordinates of the stratum polygon.
        
        Returns:
        --------
        None
        """
        # Get the lenses to plot and the bounds of the unit
        names = row['lenses'].split(';')
        if self.feature_mode == 'merge':
            # Add the features to plot here 
            names += row['features'].split(';')
        # Remove empty names
        names = [n for n in names if n != '']

        x_min, x_max = geom[0][:, 0].min(), geom[4][:, 0][len(geom[4][:, 0]) // 2]
        y_min, y_max = geom[0][:, 1].min(), geom[0][:, 1].max()

        erosion_bottom = row['erosion_bottom']
        erosion_top = row['erosion_top']
        # Adjust the y_min and y_max account for erosion (so they display in the middle of the non-eroded section)
        if self.y_mode in ['depth', 'height']:
            y_min = y_min + 2*abs(erosion_bottom)
            y_max = y_max - 2*abs(erosion_top)
        else:
            y_min = y_min - 2*abs(erosion_top)
            y_max = y_max + 2*abs(erosion_bottom)

        # Assume the same spacings from the features column
        width = self.max_feature_width
        spacing = self.spacing
        available_width = x_max - x_min
        used_space = (len(names) * width) + (len(names) + 1) * spacing

        # If the available space is less than the used space, cut to the max number of lenses that can fit, and adjust spacing below
        if available_width < used_space:
            # Change the width to fit all lenses
            width = (available_width - (len(names) + 1) * spacing) / len(names)
            spacing = spacing * (available_width / used_space)
            available_width = x_max - x_min
            used_space = (len(names) * width) + (len(names) + 1) * spacing

        # If the available space is more than the used space, adjust spacing so that all lenses fit
        if available_width > used_space:
            spacing += (available_width - used_space) / (len(names) + 1)

        # Loop through the lenses and plot them
        for n, nam in enumerate(names):
            if nam in self.lithologies.keys():
                x_left = x_min + spacing + (n) * (width + spacing)
                x_right = x_left + width
                lens = self.compute_lens_polygon(ax, x_left, x_right, y_min, y_max, width)
                # Plot the lens and border
                self.display_stratum(fig, ax, lens[0], key=nam, fmt=self.lithologies[nam], ppi=self.ppi*2, zorder=self.zorder_borders-1, lens=True)
                ax.plot(lens[0][:, 0], lens[0][:, 1], color='k', linewidth=self.border_lw, zorder=self.zorder_borders)
            else:
                max_width = self.max_feature_width
                max_height = self.total_y_height / 10
                max_height = 0.8*(y_max - y_min)  # Ensure the feature fits within the stratum height
                max_height = 1e3  # A ludicrous value will ensure features always fit to width instead
                self.display_feature(fig, ax, nam, x_min + spacing + (n) * (width + spacing) + width/2, (y_min + y_max)/2, max_width, max_height)

    def compute_lens_polygon(self, ax, x_min, x_max, y_min, y_max, lens_width=2) -> list[np.ndarray]:
        """
        Finds the geometry of where lenses should be drawn, given the bounds of the unit and desired lens width and amplitude.

        Parameters:
        -----------
        x_min : float
            Minimum x value of the unit
        x_max : float
            Maximum x value of the unit
        y_min : float
            Minimum y value of the unit
        y_max : float
            Maximum y value of the unit
        width : float
            Desired width of the lens in data units

        Returns:
        --------
        list
            A list containing a single numpy array of the x-y co-ordinates of the lens polygon, shape (N x 2)   
        """
        # Get the axis aspect ratio
        lens_ratio = 0.9 / 0.2
        ax_size_du = [self.total_x_width, self.total_y_height]
        ax_aspect_du = ax_size_du[0] / ax_size_du[1]
        # Compute the aspect ratio of the axis in inches
        ax_size_inches = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
        ax_aspect = ax_size_inches.width / ax_size_inches.height
        # Correct the axis data units ratio by the inches ratio
        ax_aspect_du /= ax_aspect
        
        # If displaying within a column (called from populate_features_column())
        if self.feature_mode == 'default':
            width = x_max - x_min
            lens_width = 0.9 * width
            lens_amplitude = lens_width / lens_ratio / ax_aspect_du

            y_mid = y_min + (y_max - y_min) / 2
            x_mid = x_min + width / 2
            x_top = np.linspace(x_mid - lens_width/2, x_mid + lens_width/2, self.N)
            x_bottom = x_top.copy()
            y_top = y_mid + lens_amplitude * np.sin(np.pi * (x_top - x_mid) / lens_width - np.pi/2)
            y_bottom = y_mid - lens_amplitude * np.sin(np.pi * (x_bottom - x_mid) / lens_width - np.pi/2)

        # For in-unit lenses, the width is supplied from the create_log() function, just compute the height
        else:
            lens_amplitude = lens_width / lens_ratio / ax_aspect_du

            y_mid = (y_min + y_max) / 2
            x_mid = (x_min + x_max) / 2
            x_top = np.linspace(x_min, x_max, self.N)
            x_bottom = x_top.copy()
            y_top = y_mid + lens_amplitude * np.sin(np.pi * (x_top - x_mid) / lens_width - np.pi/2)
            y_bottom = y_mid - lens_amplitude * np.sin(np.pi * (x_bottom - x_mid) / lens_width - np.pi/2)
        
        # Compute the co-ords of the lens, and get the rock type
        points = np.array([np.concatenate([x_top, x_bottom[::-1]]), np.concatenate([y_top, y_bottom[::-1]])]).T
        return [points]
        
    def create_empty_legend_marker(self, type, fmt, key='') -> tuple:
        """
        This function creates an empty legend marker for lithologies, features, minerals, titles, lines, and samples, which is then filled with the appropriate custom handler and label for the legend entry.

        Parameters
        ----------
        type : str
            The type of the marker, can be 'lithology', 'feature', 'mineral', 'title', or 'line'.
        fmt : tuple or str
            The formatting tuple for the marker (from lithologies, features, or minerals_list dictionaries), or a string for the title.
        key : str
            Optional name for the legend entry being created, used for minerals and lines. Defaults to ''.

        Returns
        -------
        tuple
            A tuple containing the empty handle, custom handler, and label for the legend entry.
        """
        if type == 'lithology':
            empty_handle = plt.Line2D([], [], c='none')
            custom_handler = ImageHandler(key, fmt, self.rel_box_size)
            label = fmt[-1]
            return  empty_handle, custom_handler, label
        elif type == 'feature':
            empty_handle = plt.Line2D([], [], c='none')
            custom_handler = ImageHandler(key, fmt, self.rel_box_size, outline=False)
            label = fmt[-1]
            return empty_handle, custom_handler, label
        elif type == 'mineral':
            empty_handle = plt.Line2D([], [], c=fmt[0], marker=fmt[2], markersize=self.leg_marker_size, linestyle='None', markeredgecolor=fmt[1])
            custom_handler = None
            label = key
            return empty_handle, custom_handler, label
        elif type == 'title':
            empty_handle = [fmt] + [plt.Line2D([], [], c='none') for _ in range(self.legend_columns - 1)]
            custom_handler = [LegendTitle(self.fontsize['legend_subtitle'])] + [None] * (self.legend_columns - 1)
            label = [''] * self.legend_columns
            # Return each tuple as an element in a list
            return list(zip(empty_handle, custom_handler, label))
        elif type == 'line':
            if fmt[-1].lower() == 'erosional':
                empty_handle = plt.Line2D([], [], linestyle=fmt[1], color=fmt[2], linewidth=fmt[0])
                custom_handler = HandlerSineLine()
            else:
                empty_handle = plt.Line2D([], [], linestyle=fmt[1], color=fmt[2], linewidth=fmt[0])
                custom_handler = None
            label = fmt[-1]
            return empty_handle, custom_handler, label
        elif type == 'sample':
            # sample markers
            empty_handle = plt.Line2D([], [], c=fmt[0], marker=fmt[2], markersize=self.leg_marker_size, linestyle='None', markeredgecolor=fmt[1])
            custom_handler = None
            label = key
            return empty_handle, custom_handler, label
        elif type == 'empty':
            empty_handle = plt.Line2D([], [], c='none')
            custom_handler = None
            label = ''
            return empty_handle, custom_handler, label

    def parse_legend_kwargs(self, legend_kwargs) -> tuple[dict, dict]:
        """
        Sets all of the legend_kwarg parameters, ensuring the main three are not overwritten, and makes a backup of the default kwargs in case the user-supplied kwargs fail.

        Parameters:
        -----------
        legend_kwargs : dict
            The user-supplied legend keyword arguments.

        Returns:
        --------
        tuple
            A tuple containing two dictionaries:
            - The first dictionary contains the final legend keyword arguments to be used.
            - The second dictionary contains the default legend keyword arguments for fallback.
        """
        # Ensure the main three params aren't in legend_kwargs
        ignore = ['handles', 'labels', 'handler_map', 'ncol', 'ncols']
        if 'ncol' in legend_kwargs or 'ncols' in legend_kwargs:
            print("stratapy's `legend_columns` parameter overrides any user-supplied 'ncol' or 'ncols' in legend_kwargs, these will be ignored.")

        [legend_kwargs.pop(key) for key in ignore if key in legend_kwargs]

        # Get desired legend position
        loc_params = {'top': ((0.5, .95), 'lower center'), 'right': ((.94, 0.5), 'center left'), 'bottom': ((0.5, 0.05), 'upper center'), 'left': ((0, 0.5), 'center right')}
        loc_params = loc_params[self.legend_loc]

        # Set legend_kwargs defaults if not provided, and keep a track of the defaults in case user-supplied kwargs fail
        # Set default for labelspacing and store in default_legend_kwargs
        legend_defaults = {
            'labelspacing': 2.2,
            'handletextpad': 1,
            'handlelength': 2,
            'handleheight': 0.7,
            'framealpha': 1,
            'facecolor': 'none',
            'fancybox': False,
            'borderpad': 1.2,
            'edgecolor': 'k',
            'borderaxespad': 0,
        }
        if self.legend_columns == 1:
            legend_defaults['handletextpad'] = 1.5
            legend_defaults['borderpad'] = 1.5
        # Then add in the default values for the optional parameters in `.plot()`
        legend_defaults.setdefault('ncols', self.legend_columns)
        legend_defaults.setdefault('frameon', self.legend_border)
        legend_defaults.setdefault('bbox_to_anchor', loc_params[0])
        legend_defaults.setdefault('loc', loc_params[1])

        # This will be used in the event that the user-supplied kwargs fail. Create a copy of this and add in the user-supplied kwargs as plan A.
        user_kwargs = legend_defaults.copy()

        # Add all the user-supplied kwargs (in `legend_kwargs`) to this dict
        for key, value in legend_kwargs.items():
            # Update values, overwriting existing ones
            user_kwargs[key] = legend_kwargs.get(key, value)

        # Fontsize is set using `formatting.fontsizes['legend_entry']` or `formatting.fontsizes['legend_subtitle']`, ignoring any user-supplied fontsize
        if 'fontsize' in user_kwargs:
            print(f"Ignoring user-supplied legend fontsize of {user_kwargs['fontsize']}, use e.g., `formatting.fontsizes['legend_entry'] = 14` to set legend font size instead.")
        user_kwargs['fontsize'] = self.fontsize['legend_entry']

        return user_kwargs, legend_defaults

    def make_legend(self, fig, lithology_legend) -> 'matplotlib.legend.Legend':
        """
        Creates the legend for the stratigraphic column, including lithologies, minerals, features, and contact types.

        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            The figure to draw the legend on.
        lithology_legend : list
            List of lithology keys to include in the legend.

        Returns:
        --------
        matplotlib.legend.Legend
            The created legend object.
        """
        legend_kwargs, default_legend_kwargs = self.parse_legend_kwargs(self.legend_kwargs)  
        ncol = self.legend_columns

        self.rel_box_size = 20
        self.leg_marker_size = self.rel_box_size * .5

        # Create an empty list to store tuples of (handles, labels, custom handlers)
        legend_items = []

        #### Lithologies ####
        # Add the subtitle
        legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[0]))
        # If the 'no' key is in the legend, ensure it is at the end
        if 'no' in lithology_legend:
            lithology_legend.remove('no')
            lithology_legend.append('no')
        # Reorder the keys to be in columns
        n = len(lithology_legend)
        pad = (-n) % ncol
        padded_legend = lithology_legend + [None] * pad if pad else lithology_legend
        padded_legend = np.array(padded_legend).reshape(-1, ncol, order='F').flatten()
        lithology_legend = [key for key in padded_legend if key is not None]  # Remove None values

        # Now add each lithology to the legend
        [legend_items.append(self.create_empty_legend_marker('lithology', self.lithologies[key], key)) for key in lithology_legend]

        # Ensure that the total number of entries after this subsection is a multiple of the number of columns
        if len(legend_items) % ncol != 0: 
            legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))

        # Sort by key alphabetically
        self.features = dict(sorted(self.features.items()))
        self.minerals_list = dict(sorted(self.minerals_list.items()))
        self.contact_types = dict(sorted(self.contact_types.items()))   
        # If legend is combining many logs, use the required contact types only, else get the unique contact types in the dataframe
        if hasattr(self, 'required_contact_types'):
            needed_contacts = list(self.required_contact_types.keys())
        else:
            needed_contacts = list(self.df['contact'].unique())
            if any(self.df['erosion_bottom'] != 0.):
                needed_contacts.append('erosional')

        # Now filter the contact types to only those needed, excluding 'Normal'
        self.contact_types = {k: v for k, v in self.contact_types.items() if k in needed_contacts and v[-1] != 'Normal'}

        #### Minerals ####
        if len(self.minerals_list) > 0:
            # Add the subtitle
            legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[1]))
            # Add each mineral
            [legend_items.append(self.create_empty_legend_marker('mineral', self.minerals_list[key], key.title())) for key in self.minerals_list.keys()]
            # Ensure that the total number of entries after this subsection is a multiple of the number of columns
            if len(legend_items) % ncol != 0: 
                legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))

        #### All Features ####
        # Structural
        if len([x for x in self.features.values() if x[0] == 'structure']) > 0:
            legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[2]))
            [legend_items.append(self.create_empty_legend_marker('feature', v, key)) for key, v in self.features.items() if v[0] == 'structure']
            if len(legend_items) % ncol != 0: 
                legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))
        # Fossils
        if len([x for x in self.features.values() if x[0] == 'fossil']) > 0:
            legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[3]))
            [legend_items.append(self.create_empty_legend_marker('feature', v, key)) for key, v in self.features.items() if v[0] == 'fossil' and key != 'fragmented']
            # Ensure that the 'fragmented' feature is at the end, if present
            if 'fragmented' in self.features.keys():
                legend_items.append(self.create_empty_legend_marker('feature', self.features['fragmented'], 'fragmented'))
            if len(legend_items) % ncol != 0:
                legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))
        # Tectonic
        if len([x for x in self.features.values() if x[0] == 'tectonic']) > 0:
            legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[4]))
            [legend_items.append(self.create_empty_legend_marker('feature', v, key)) for key, v in self.features.items() if v[0] == 'tectonic']
            if len(legend_items) % ncol != 0:
                legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))

        #### Contacts ####
        if len(self.contact_types) > 0:
            legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[5]))
            # Add the erosion line types, excluding the default 'Normal' contact 
            [legend_items.append(self.create_empty_legend_marker('line', v)) for v in self.contact_types.values()]
            # Ensure that the total number of entries after this subsection is a multiple of the number of columns
            if len(legend_items) % ncol != 0:
                legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))

        ### Samples ###
        # Note: these are added afterwards
        if hasattr(self, 'added_samples_list') and len(self.added_samples_list) > 0:
            # Add the subtitle
            legend_items.extend(self.create_empty_legend_marker('title', self.legend_titles[6]))
            # Add each mineral
            [legend_items.append(self.create_empty_legend_marker('mineral', self.added_samples_list[key], key)) for key in self.added_samples_list.keys()]
            # Ensure that the total number of entries after this subsection is a multiple of the number of columns
            if len(legend_items) % ncol != 0: 
                legend_items += [self.create_empty_legend_marker('empty', None)] * (ncol - (len(legend_items) % ncol))

        # Extract handles, labels, and custom handlers, then create the handler map from them
        handles, custom_handles, labels = zip(*legend_items)
        handler_map = {h: custom_handles[i] for i, h in enumerate(handles) if custom_handles[i] is not None}

        # Reshape legend for number of columns
        handles = np.array(handles).reshape(-1, ncol).T.flatten()
        labels = np.array(labels).reshape(-1, ncol).T.flatten()

        # Try to plot the legend with the legend_kwargs, if error, plot without and throw warning
        try:
            leg = fig.legend(handles, labels, handler_map=handler_map, **legend_kwargs)
        except Exception as e:
            print(f"Warning: Could not plot legend with provided kwargs due to error:\n  > {e}.\n  > Plotting using deafult kwargs.")
            leg = fig.legend(handles, labels, handler_map=handler_map, **default_legend_kwargs)

        return leg

from matplotlib.legend_handler import HandlerLine2D, HandlerBase

class LegendTitle(object):
    """
    A custom legend handler to create bold titles in the legend.
    """

    def __init__(self, fontsize, text_props=None) -> None:
        """
        A custom legend handler to create bold titles in the legend.
        """
        self.text_props = text_props or {}
        self.fontsize = fontsize
        super(LegendTitle, self).__init__()

    def legend_artist(self, legend, orig_handle, fontsize, handlebox) -> "mtext.Text":
        """
        Create a bold text artist for the legend title.
        """
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        # Add space to fix padding issues
        import matplotlib.text as mtext
        title = mtext.Text(x0, y0, orig_handle, fontweight='bold', fontsize=self.fontsize)
        handlebox.add_artist(title)
        return title

class HandlerSineLine(HandlerLine2D):
    """
    A custom legend handler to create a sine wave line in the legend.
    """

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans) -> list:
        """
        Create a sine wave line artist for the legend.
        """
        # Create a sine wave within the legend box
        x = np.linspace(0, width, 100)
        y = ydescent + height/2 + (height/2.5) * np.sin(2 * np.pi * x / width)
        line = plt.Line2D(x, y, linestyle=orig_handle.get_linestyle(),
                          color=orig_handle.get_color(),
                          linewidth=orig_handle.get_linewidth())
        line.set_transform(trans)
        return [line]

class ImageHandler(HandlerBase):
    """
    A custom legend handler to create image-based legend entries for lithologies and features.
    """

    def __init__(self, key, fmt, rel_box_size, outline=True) -> None:
        """
        Initializes the ImageHandler with the given parameters.

        Parameters
        ----------
        key : str
            The key for the legend entry, used to identify the image.
        fmt : tuple 
            Tuple of the formatting of the pattern
        rel_box_size : int
            The relative size of the box in pixels, used to scale the image.
        outline : bool, optional
            Whether to draw an outline around the box (default is True).

        Returns
        -------
        None
        """
        super().__init__()
        self.key = key
        self.rel_box_size = rel_box_size
        # Set default formatting values
        self.fillcolour = 'none'
        self.hatch_pattern = None
        self.hatch_color = 'none'
        self.linewidth = 1.5
        self.edgecolor = 'k' if outline else 'none'
        self.zoom = 0.05
        # Set a default colourmap 
        self.cmap = 'gray_r'
        # Compute an updated box size using the zoom
        box_size = int(self.rel_box_size / self.zoom)

        # Extract formatting information from the fmt tuple
        # For filled regions (only 'not observed' or solid fills)
        if fmt[0] == 'fill':
            _, self.fillcolour, self.hatch_pattern, self.hatch_color, _ = fmt
            self.image_data = np.zeros((self.rel_box_size, self.rel_box_size), dtype=np.uint8)
        # For images
        else:
            # Lithologies or patterns
            if fmt[0] in ['pattern', 'lith']:
                _, self.image_data, self.cmap, _ = fmt
                # If image is smaller than the box size, tile the image to fill the box size
                if self.image_data.shape[0] < box_size or self.image_data.shape[1] < box_size:
                    # Tile the image to fill the box size
                    ndims = len(self.image_data.shape)
                    tpl = ( box_size // self.image_data.shape[0] + 1, box_size // self.image_data.shape[1] + 1 ) + (1,) * (ndims - 2)
                    self.image_data = np.tile(self.image_data, tpl)
                # Crop image to top center square if it is larger than the box size
                if self.image_data.shape[0] > box_size or self.image_data.shape[1] > box_size:
                    # Crop the image to the center square of the specified box size
                    start_row = (self.image_data.shape[0] - box_size) // 2
                    start_col = (self.image_data.shape[1] - box_size) // 2
                    self.image_data = self.image_data[start_row:start_row + box_size, start_col:start_col + box_size]
            # Features
            else:
                _, self.image_data, _ = fmt
                # Adjust zoom if the image is not exactly the box size
                if self.image_data.shape[0] != box_size or self.image_data.shape[1] != box_size:
                    self.zoom *= box_size / max(self.image_data.shape)

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans) -> list:
        """
        Create the image-based legend entry.
        
        Parameters
        ----------
        legend : matplotlib.legend.Legend
            The legend object.
        orig_handle : object
            The original handle for the legend entry.
        xdescent : float
            The x descent of the legend entry.
        ydescent : float
            The y descent of the legend entry.
        width : float
            The width of the legend entry.
        height : float
            The height of the legend entry.
        fontsize : float
            The fontsize of the legend entry.
        trans : matplotlib.transforms
            The transformation to apply to the legend entry.
        
        Returns
        -------
        list
            A list of matplotlib artists to be added to the legend.
        """
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        # Create an OffsetImage with the image data, applying the zoom and colormap
        image_box = OffsetImage(self.image_data, zoom=self.zoom, cmap=self.cmap)
        # The AnnotationBbox places the image in the legend (incl. empty images for fills)
        ab = AnnotationBbox(
            image_box, (width / 2, height / 2),
            frameon=False, pad=0., xycoords=trans,
            bboxprops=dict(linewidth=self.linewidth, edgecolor=self.edgecolor)
        )
        # Rectangular patch draws any filled regions, as well as the outline of the box, if desired
        # If 'no observation' format, ensure there is no fill colour
        if self.key == 'no':
            self.fillcolour = 'none'
        patch = Rectangle(
            (width / 2 - self.rel_box_size / 2, height / 2 - self.rel_box_size / 2),
            self.rel_box_size, self.rel_box_size,
            facecolor=self.fillcolour, hatch=self.hatch_pattern, alpha=1,
            edgecolor=self.edgecolor, linewidth=1
        )
        # Set the hatching colour (rgba)
        patch._hatch_color = colour_to_rgba(self.hatch_color)
        # Edge case for 'no observation' units
        if self.key == 'no':
            # Plot lines from the top left to bottom right and from the top right to bottom left
            l1 = plt.Line2D([width / 2 - self.rel_box_size / 2, width / 2 + self.rel_box_size / 2], [height / 2 - self.rel_box_size / 2, height / 2 + self.rel_box_size / 2], color='k', linewidth=.5)
            l2 = plt.Line2D([width / 2 + self.rel_box_size / 2, width / 2 - self.rel_box_size / 2], [height / 2 - self.rel_box_size / 2, height / 2 + self.rel_box_size / 2], color='k', linewidth=.5)
                            
            return [ab, patch, l1, l2]
        return [ab, patch]