"""
This module contains the primary function for creating a stratigraphic log plot using stratapy, as well as some higher-level auxiliary functions for plotting specific components of the log, such as stratum borders and bracket annotations.

Used by stratapy.core and stratapy.plotting_help.
"""

from numpy import mean as npmean, array, concatenate, diff, allclose, errstate, linspace, clip, arctan2, zeros
from scipy.interpolate import splprep, splev
from shapely.geometry import Polygon as ShapelyPolygon, MultiPolygon
from shapely.ops import unary_union

def is_straight_line(x, y) -> bool:
    """
    Checks if a set of points defined by x and y coordinates form a straight line.
    
    Parameters
    ----------
    x : array-like
        The x-coordinates of the points.
    y : array-like
        The y-coordinates of the points.

    Returns
    -------
    bool
        True if the points form a straight line, False otherwise.
    """
    # Avoid division by zero
    with errstate(divide='ignore', invalid='ignore'):
        slopes = diff(y) / diff(x)
    return allclose(slopes, slopes[0], atol=1e-4, equal_nan=True)

def plot_efficient_line(ax, x, y, color, lw, ls, zord, clip_on=True) -> None:
    """
    Plots a set of provided points, but first checks if it is a straight line, in which case only the endpoints are plotted for efficiency.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis on which to plot the line.
    x : array-like
        The x-coordinates of the points.
    y : array-like
        The y-coordinates of the points.
    color : str
        The colour of the line.
    lw : float
        The line width.
    ls : str
        The line style.
    zord : int
        The z-order for layering.
    clip_on : bool, optional
        Whether to clip the line to the axes boundaries (default is True).
    
    Returns
    -------
    None
    """
    if is_straight_line(x, y):
        ax.plot([x[0], x[-1]], [y[0], y[-1]], color=color, linewidth=lw, zorder=zord, linestyle=ls, clip_on=clip_on)
    else:
        ax.plot(x, y, color=color, linewidth=lw, zorder=zord, linestyle=ls, clip_on=clip_on)

def draw_stratum_borders(ax, df, row, helper, geom, idx, prev_bottom) -> array:
    """
    Plots the lower border of a given stratum (accounting for the top of the first stratum) including any contact formatting in relation to the previous stratum. 

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis on which to plot the borders.
    df : pandas.DataFrame
        The dataframe containing the stratigraphic data.
    row : pandas.Series
        The current row of the dataframe (stratum) being processed.
    helper : object
        An object containing helper methods and attributes for plotting.
    geom : list
        The geometries for the current stratum.
    idx : int
        The index of the current row in the dataframe.
    prev_bottom : array-like
        The geometry of the bottom border of the previous stratum.
    
    Returns
    -------
    prev_bottom : array-like
        The geometry of the bottom border of the current stratum, to be used in the next iteration.
    """
    # Extract the upper & lower border geometries and formatting of this stratum
    top_line = geom[1]
    bottom_line = geom[2]
    fmt = helper.contact_types[row['contact']]

    # Plot the top of the uppermost stratum
    if idx == 0:
        plot_efficient_line(ax, top_line[:, 0], top_line[:, 1], color='k', lw=helper.border_lw, ls='solid', zord=helper.zorder_borders, clip_on=False)
    # And the bottom of the lowermost stratum
    if idx == len(df)-1:
        plot_efficient_line(ax, bottom_line[:, 0], bottom_line[:, 1], color='k', lw=helper.border_lw, ls='solid', zord=helper.zorder_borders, clip_on=False)

    if idx > 0:# and plot_upper_border:
        prev_bot = prev_bottom[::-1]
        # Determine gap size (x-axis) between previous bottom and current top. This enables the border to be displayed correctly, accounting for two units meeting with different grain sizes.
        gap = abs(top_line[:, 0][-1] - prev_bot[:, 0][-1])

        # If the gap is zero and the lithologies are different, plot the top line
        if gap == 0 and row['rock'] != df.iloc[idx-1].rock:
            plot_efficient_line(ax, top_line[:, 0], top_line[:, 1], color=fmt[2], lw=fmt[0], ls=fmt[1], zord=helper.zorder_borders)
            
        # If the gap is non-zero and the lithologies are different, plot the longer line
        elif gap > 0 and row['rock'] != df.iloc[idx-1].rock:
            if top_line[:, 0][-1] > prev_bot[:, 0][-1]:
                plot_efficient_line(ax, top_line[:, 0], top_line[:, 1], color=fmt[2], lw=fmt[0], ls=fmt[1], zord=helper.zorder_borders)
            else:
                plot_efficient_line(ax, prev_bot[:, 0], prev_bot[:, 1], color=fmt[2], lw=fmt[0], ls=fmt[1], zord=helper.zorder_borders)

        # If the gap is non-zero and the lithologies are the same, plot the line that spans the gap, i.e. the longer of the two
        elif gap > 0 and row['rock'] == df.iloc[idx-1].rock:
            min_x = min(top_line[:, 0][-1], prev_bot[:, 0][-1])
            if top_line[:, 0][-1] > prev_bot[:, 0][-1]:
                plot_efficient_line(ax, top_line[:, 0][top_line[:, 0] >= min_x], top_line[:, 1][top_line[:, 0] >= min_x], color=fmt[2], lw=fmt[0], ls=fmt[1], zord=helper.zorder_borders)
            else:
                plot_efficient_line(ax, prev_bot[:, 0][prev_bot[:, 0] >= min_x], prev_bot[:, 1][prev_bot[:, 0] >= min_x], color=fmt[2], lw=fmt[0], ls=fmt[1], zord=helper.zorder_borders)

    # Return the bottom line for the next iteration
    return bottom_line.copy()

def draw_bracket_annotation(ax, renderer, helper, ticks, txt) -> None:
    """
    Plots a bracket annotation on a matplotlib axis beneath specified x-axis tick labels.
    The bracket is drawn below the x-axis tick labels specified in `ticks`, with a text label `txt` centered above the bracket.
    The function ensures that at least two of the specified tick labels are present before plotting the bracket.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis on which to plot the bracket.
    renderer : matplotlib.backend_bases.RendererBase
        The renderer used to compute tick label positions.
    helper : object
        An object containing `x_tick_labels` (list of tick label values) and `x_ticks` (list of tick positions).
    ticks : list
        Pair of numerical values for the range of the bracket.
    txt : str
        Text to display above the bracket.
    
    Returns
    -------
    None
    
    Notes
    -----
    - The bracket is only plotted if at least two of the specified tick labels are present.
    - If not all tick labels in `ticks` are present, a warning is printed and nothing is plotted.
    """
    # If no ticks provided, return
    if len(ticks) == 0:
        return

    # Get the lower y value of the x-axis tick labels
    xticklab = ax.get_xticklabels()
    # Ensure not multi line
    xticklab = [x for x in xticklab]
    mins = []
    widths = []
    for xtick in xticklab:
        bbox_display = xtick.get_window_extent(renderer=renderer)
        bbox_data = bbox_display.transformed(ax.transData.inverted())
        if ax.get_ylim()[1] < ax.get_ylim()[0]:
            # If the y-axis is inverted, use the maximum y value
            mins.append(bbox_data.ymax)
        else:
            mins.append(bbox_data.ymin)
        widths.append(bbox_data.width)
    y_ax_min = ax.get_ylim()[0]
    ff = npmean(mins)
    ff_width = ff - y_ax_min
    y_upper = y_ax_min + ff_width * 1
    y_lower = y_ax_min + ff_width * 1.2
    y_text = y_ax_min + ff_width * 1.4

    x_left, x_right = ticks[0], ticks[-1]
    # Account for lithology column, if present
    if helper.lithology_column_thickness > 0:
        x_left += helper.lithology_column_thickness
        x_right += helper.lithology_column_thickness

    # Get the last position in the x-axis (that isn't 'Features')
    # If x_right is beyond the last x position, adjust it, if x_left is also beyond, ignore this bracket
    if x_right > helper.max_x_grain:
        if x_left >= helper.max_x_grain:
            return
        else:
            x_right = helper.max_x_grain

    width = min(widths)
    padd = width*1.5
    x_left -= padd
    x_right += padd

    ax.hlines(y_lower, xmin=x_left, xmax=x_right, color='k', linewidth=1, zorder=5, clip_on=False)
    ax.vlines(x_left, ymin=y_lower, ymax=y_upper, color='k', linewidth=1, zorder=5, clip_on=False)
    ax.vlines(x_right, ymin=y_lower, ymax=y_upper, color='k', linewidth=1, zorder=5, clip_on=False)
    ax.text((x_left+x_right)/2, y_text, txt, ha='center', va='top', fontsize=helper.fontsize['grain_brackets'], color='k', clip_on=False, zorder=5)

def adaptive_spline_smooth(x, y, s=0.5, k=3) -> tuple[array, array]:
    """
    Smooths a curve using adaptive spline fitting that preserves straight sections.
    
    The function applies higher smoothing weights to straight line segments and lower 
    weights to corners/sharp features, allowing straight sections to remain straight 
    while smoothing out noise and jaggedness in curved regions.
    
    Parameters
    ----------
    x : array-like
        The x-coordinates of the curve points.
    y : array-like
        The y-coordinates of the curve points.
    s : float, optional
        Smoothing factor for spline fitting (default is 0.5). Higher values produce 
        smoother curves at the cost of less adherence to original points.
    k : int, optional
        Degree of the spline (default is 3 for cubic). Must be 1 ≤ k ≤ 5.
    
    Returns
    -------
    x_smooth : ndarray
        Smoothed x-coordinates.
    y_smooth : ndarray
        Smoothed y-coordinates.
    
    Notes
    -----
    - Endpoints are forced to remain fixed during smoothing.
    - Weights are computed based on local curvature (angle changes between segments).
    - Straight sections receive higher weights to preserve their shape.
    """
    # Calculate local curvature via angle changes
    dx = diff(x)
    dy = diff(y)
    angles = arctan2(dy, dx)
    da = diff(angles)
    
    # Compute jaggedness metric (higher = sharper corners)
    jaggedness = zeros(len(x))
    jaggedness[1:-1] = abs(da)
    
    # Create adaptive weights: high weight for straight sections, low for corners
    w = 1.0 / (jaggedness + 0.01)
    w = clip(w, 0.1, 2)
    
    # Force endpoints to stay fixed
    w[0] = 1e6
    w[-1] = 1e6
    
    # Fit spline with adaptive weights
    tck, u = splprep([x, y], w=w, s=s, k=k)
    
    # Evaluate spline at original point density
    u_fine = linspace(0, 1, len(x))
    x_smooth, y_smooth = splev(u_fine, tck)
    
    return x_smooth, y_smooth

def create_log(helper : object, fig, ax, override_ylims, share_legend) -> tuple[object, object, object, object]:
    """
    Calls all of the functions necessary to plot the final figure.
    This function is called after the data has been loaded using `sp.load()`.

    Parameters
    ----------
    helper : object
        An instance of the PlottingHelp class, which contains all necessary data and methods for plotting.
    fig : matplotlib.figure.Figure
        The figure object to plot on.
    ax : matplotlib.axes.Axes   
        The axes object to plot on.
    override_ylims : tuple or None
        If provided, this tuple will override the automatic y-axis limits (used for composite logs with shared y-axis).
    share_legend : bool
        Whether to share the legend across subplots in a composite log. Defers legend creation to the end of the plotting process if True.

    Returns
    ----------
    fig : matplotlib.figure.Figure  
        The figure object containing the plotted stratigraphy.
    ax : matplotlib.axes.Axes
        The axes object containing the plotted stratigraphy.
    leg : matplotlib.legend.Legend or None
        The legend object, or None if no legend is created. 
    helper : object
        The helper object, to provide later access to various variables and methods.
    """
    # Create a figure and axis
    fig, ax = helper.fig_setup(fig, ax, override_ylims)

    # Remove spines if desired
    if not helper.spines:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # If log mode, also remove left and bottom spines
        if helper.display_mode == 'log':
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

    # Create variables to store image-based information
    combined_strata, combined_right = [], []
    previous_bottom = None

    # Pre compute all unit geometries first (a is lith-column, b complete region of column and stratum, c stratum without column)
    all_geom_a, all_geom_b, all_geom_c = zip(*(helper.compute_unit_polygons(row, helper.x_offset, helper.N) for _, row in helper.df.iterrows()))
    zord = 1 # zorder for layering units and borders

    # Loop over each row (stratum) in the dataframe
    for r, row in helper.df.iterrows():
        # Create a variable to determine whether to plot the upper border of a unit (for combined strata)
        plot_upper_border = False

        # Get the lithology of this stratum and its display properties
        lithology_key = row.rock
        lithology_properties = helper.lithologies[lithology_key]

        # Extract geometries for this unit
        geom_a, geom_b, geom_c = all_geom_a[r], all_geom_b[r], all_geom_c[r]

        # Check if this stratum is part of a larger combination of strata
        if (r < len(helper.df)-1 and row.rock == helper.df.iloc[r+1].rock) and (row.rock != 'no') and ((r == 0) or (r > 0 and row.rock != helper.df.iloc[r-1].rock)):
            combined_strata.append(geom_a[0])
            plot_upper_border = True
            combined_right.append(geom_b[4])

        elif (r > 0 and row.rock == helper.df.iloc[r-1].rock) and (r < len(helper.df)-1 and row.rock == helper.df.iloc[r+1].rock) and row.rock != 'no':
            combined_strata.append(geom_a[0])
            combined_right.append(geom_b[4])

        elif (r > 0 and row.rock == helper.df.iloc[r-1].rock) and ( (r < len(helper.df)-1 and row.rock != helper.df.iloc[r+1].rock) or r == len(helper.df)-1 ) and row.rock != 'no':
            combined_strata.append(geom_a[0])
            combined_right.append(geom_b[4])

            # Make a copy of the combined_right list for matching right-side back to combined unit
            combined_right_original = combined_right.copy()
            combined_right = concatenate(combined_right)
            
            # If any unit in the combined unit is marked as smooth, smooth the right-edge of this combined unit
            if any(helper.df.iloc[r-len(combined_strata)+1:r+1]['smooth']):
                # Remove duplicate consecutive points while maintaining order
                unique_points = [combined_right[0]]
                for point in combined_right[1:]:
                    if not (point == unique_points[-1]).all():
                        unique_points.append(point)
                combined_right = array(unique_points)
                cr_x, cr_y = combined_right[:, 0], combined_right[:, 1]
                new = adaptive_spline_smooth(cr_x, cr_y, s=1, k=3)
                combined_right = array(new).T

            # Create the unit polygon - does not include the smoothed right-edge
            geom = unary_union([ShapelyPolygon(sp).buffer(0) for sp in combined_strata])
            if isinstance(geom, MultiPolygon):
                # Use the largest polygon by area
                largest = max(geom.geoms, key=lambda g: g.area)
                x, y = largest.exterior.xy
            else:
                x, y = geom.exterior.xy
            all_points = array([x, y]).T

            # Match the smoothed right-edge to the original right-edge points in the polygon to integrate the smoothed edge
            if any(helper.df.iloc[r-len(combined_strata)+1:r+1]['smooth']):
                right_start_idx = None
                right_end_idx = None
                for idx, point in enumerate(all_points):
                    if right_start_idx is None and allclose(point, concatenate(combined_right_original)[0], atol=1e-6):
                        right_start_idx = idx
                    if allclose(point, concatenate(combined_right_original)[-1], atol=1e-6):
                        right_end_idx = idx
                
                # If found, reconstruct the polygon with smoothed right edge
                if right_start_idx is not None and right_end_idx is not None:
                    if right_start_idx < right_end_idx:
                        new_points = concatenate([all_points[:right_start_idx], combined_right, all_points[right_end_idx:]])
                    else:
                        new_points = concatenate([all_points[:right_end_idx], combined_right[::-1], all_points[right_start_idx:]])
                    comb_points = new_points
                else:
                    comb_points = all_points
            else:
                comb_points = all_points

            # Display the unit
            helper.display_stratum(fig, ax, comb_points, key=lithology_key, fmt=lithology_properties, ppi=helper.ppi)
            # Plot the combined unit's border
            if helper.unit_borders:
                ax.plot(combined_right[:, 0], combined_right[:, 1], color='k', linewidth=helper.border_lw, zorder=helper.zorder_borders)
                # If this is the last unit, also plot the bottom border
                if r == len(helper.df)-1:
                    plot_efficient_line(ax, geom_b[2][:, 0], geom_b[2][:, 1], color='k', lw=helper.border_lw, ls='solid', zord=helper.zorder_borders, clip_on=False)

            # Reset the combined strata lists
            combined_strata = []
            combined_right = []

        else:
            # If the top grain size of this unit is larger than the bottom of the previous unit, increase zorder to display above the previous unit AND it's border. This prevents unwanted overlaps between unit fills and borders.
            if r > 0 and row['top_grain'] > helper.df.iloc[r-1]['bottom_grain']:
                zord += 1
            else:
                zord = 1

            # Plot unit
            helper.display_stratum(fig, ax, geom_a[0], key=lithology_key, fmt=lithology_properties, ppi=helper.ppi, zorder=zord)
            # If grainsize mode, draw the unit's border and fill it as transparent
            if helper.display_mode == 'grainsize':
                ax.fill(geom_c[0][:, 0], geom_c[0][:, 1], color=(0, 0, 0, 0), lw=helper.border_lw, zorder=zord-1)

            # Display right border, with same zorder as unit to prevent overlaps
            if helper.unit_borders:
                plot_efficient_line(ax, geom_b[4][:, 0], geom_b[4][:, 1], color='k', lw=helper.border_lw, ls='solid', zord=zord)
            plot_upper_border = True

        # if r>0:
        #     print(helper.df.iloc[r]['height/age'], helper.df.iloc[r-1]['height/age'] + helper.df.iloc[r-1]['thickness'], helper.df.iloc[r-1].thickness)
        if (r > 0 and helper.df.iloc[r]['height/age'] != helper.df.iloc[r-1]['height/age'] + helper.df.iloc[r-1]['thickness'] and helper.unit_borders):
            # print(f"drawing border at bottom of unit {r} ({helper.df.iloc[r]['height/age']}) at y={previous_bottom[:, 1][0]}")
            # If there is a gap between units, plot the bottom border of the previous unit to close the gap
            ax.plot(previous_bottom[:, 0], previous_bottom[:, 1], color='k', lw=helper.border_lw, ls='solid', zorder=helper.zorder_borders, clip_on=False)
        
        if (plot_upper_border and helper.unit_borders):
            # Plot the top border, accounting for the contact and previous unit's geometry
            previous_bottom = draw_stratum_borders(ax, helper.df, row, helper, geom_b, r, previous_bottom)
        else:
            # Store for later
            previous_bottom = geom_b[2].copy()

        if helper.feature_mode != 'off':
            # Display all minerals/lenses/features which need to go in the features column, if not using 'merge' feature mode
            if (row['features'] != '' or row['minerals'] != '') and (helper.feature_mode != 'merge'):
                helper.populate_features_column(fig, ax, row, geom_c)

            # Otherwise, display any of these which go within strata:
            # Minerals
            if row['minerals'] != '' and helper.feature_mode != 'default':
                helper.display_minerals(ax, geom_a[0], row)
            # Lenses & features
            if (row['lenses'] != '' or row['features'] != '') and (helper.feature_mode != 'default'):
                # Features are shown in the lithology column for log mode
                if helper.display_mode == 'log':
                    helper.display_merged_features(fig, ax, row, geom_a)
                else:
                    helper.display_merged_features(fig, ax, row, geom_c)

    # Add bounds around the logs if spines are not being used
    if not helper.spines:
        # Right (only use if in log mode)
        if helper.display_mode == 'log':
            ax.plot([helper.x_axis_max, helper.x_axis_max], [helper.y_limits[0], helper.y_limits[1]], color='k', lw=helper.border_lw, zorder=200, clip_on=False)
            # Also top and bottom in log mode only
            ax.plot([0, helper.x_axis_max], [helper.y_limits[1], helper.y_limits[1]], color='k', lw=helper.border_lw, zorder=200, clip_on=False)
            ax.plot([0, helper.x_axis_max], [helper.y_limits[0], helper.y_limits[0]], color='k', lw=helper.border_lw, zorder=200, clip_on=False)
        # Left
        ax.plot([0, 0], helper.y_limits, color='k', linewidth=helper.border_lw, zorder=100, clip_on=False)

    # Manually compute the legend order after the fact, ensuring that we go inversely through the dataframe
    leg = []
    for r, row in helper.df.iloc[::-1].iterrows():
        # Lithologies
        lithology_key = row.rock
        if lithology_key not in leg and lithology_key != 'no':
            leg.append(lithology_key)
        # Lenses
        for lr in row['lenses'].split(';'):
            if lr not in leg and lr != '':
                leg.append(lr)
    # Invert if y-mode is height or depth
    # if helper.y_mode in ['height', 'depth']:
    leg = leg[::-1]
    # Add not observed manually, if present
    if 'no' in helper.lithologies.keys():
        leg.append('no')
    
    helper.lithology_legend = leg

    # Create legend, unless multi_fig() is being used (share_legend=True), in which case the legend will be created separately by multi_fig()
    if share_legend is not None:
        leg = None
    else:
        leg = helper.make_legend(fig, helper.lithology_legend)

    # Reverse the magnitude of the numbers on the y-axis for age logs
    if helper.invert:
        old_labels = [l.get_text() for l in ax.get_yticklabels()]
        new_labels = [f'-{l}' if l[0].isdigit() and float(l) != 0 else ('0' if l[0].isdigit() else l[1:]) for l in old_labels]
        ax.set_yticklabels(new_labels)

    # If the display_mode is log, remove x_ticks as they are redundant
    if helper.display_mode == 'log':
        ax.set_xticks([])

    # Get the renderer for plotting brackets
    fig = ax.figure
    renderer = fig.canvas.get_renderer()

    # Plot brackets around grain sizes, only needed if not in log mode
    if helper.display_mode != 'log' and helper.x_axis:
        for k, v in helper.grain_brackets.items():
            draw_bracket_annotation(ax, renderer, helper, v, k)

    # Hide x-axis if desired
    if not helper.x_axis:
        ax.set_xticks([])
        ax.spines['bottom'].set_visible(False)

    # Return the figure, axis, legend, and helper for later use
    return fig, ax, leg, helper