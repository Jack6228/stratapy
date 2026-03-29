"""
A collection of utility functions for the stratapy package, including reading input files, loading images, and various helper functions for plotting and data manipulation.

Functions from this module are imported into stratapy.core and stratapy.plotting_help.
"""

from os import path
from numpy import array, zeros, clip
import pandas as pd

def find_best_str_match(user_input : str, search_list : list, return_list : list, threshold : float = 0.6) -> str:
    """
    Finds the best matching lithology string from a list based on user input, using a combination of string normalisation and similarity scoring.

    Matching Process:
    - The user input and all candidates in the search list are converted to lowercase and stripped of leading/trailing whitespace, making the match case-insensitive and robust to extra spaces.
    - Punctuation and internal spaces are preserved (not removed), so matches are based on the exact character sequence after normalisation.
    - For each candidate in the search list, the function computes a similarity score using difflib's SequenceMatcher, which measures how closely the input matches the candidate.
    - If the user input is a substring of the candidate (i.e., appears anywhere within it), the similarity score is boosted by 0.2, up to a maximum of 1.0, favoring partial matches.
    - The candidate with the highest similarity score above a set threshold (default 0.6) is selected as the best match.
    - The index of the best match in the search list is used to retrieve the corresponding value from the return list.
    - If no candidate exceeds the threshold, or the lists are empty, the function returns None.

    Parameters
    ----------
    user_input : str
        The lithology string input by the user. Case and leading/trailing spaces are ignored; punctuation and internal spaces are preserved.
    search_list : list
        A list of lithology strings to search through. Each is normalised for comparison.
    return_list : list
        A list of lithology strings to return from, corresponding to the search_list.
    threshold : float, optional
        The minimum similarity score required to consider a match valid (default is 0.6).

    Returns
    -------
    str 
        The best matching lithology string from the return_list, or None if no match exceeds the threshold.

    Notes
    -----
    - Matching is case-insensitive and ignores leading/trailing whitespace.
    - Internal spaces and punctuation are not removed, so they affect the similarity score.
    - Partial matches (where the input is a substring of a candidate) are favored.
    - The function is robust to input types: dicts are converted to lists, and empty inputs return None.
    """
    from difflib import SequenceMatcher
    if not user_input or not search_list:
        return None
    # Ensure lists are actualy lists (will convert dicts to a list of keys)
    if not isinstance(search_list, list):
        search_list = list(search_list)
    if not isinstance(return_list, list):
        return_list = list(return_list)
    
    # Clean input and remove all spaces
    user_input = user_input.lower().strip()
    best_match = None
    highest_similarity = 0
    
    for lithology in search_list:
        lithology_lower = lithology.lower()
        # Calculate similarity using SequenceMatcher
        similarity = SequenceMatcher(None, user_input, lithology_lower).ratio()
        
        # Check if the input is a substring of the lithology (boosts score for partial matches)
        if user_input in lithology_lower:
            similarity = min(similarity + 0.2, 1.0)  # Boost score for substring matches
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = lithology
    
    # Get the index of the best match in the search list if it exists the threshold
    best_match_index = search_list.index(best_match) if best_match and highest_similarity >= threshold else None

    # Get the value from the return list if the index exists
    if best_match_index is not None and best_match_index < len(return_list):
        best_match = return_list[best_match_index]
    else:
        best_match = None

    # Return the best match only if it exceeds the threshold
    return best_match

def make_box(ax : "matplotlib.axes.Axes", row : list, rank_dict : dict, rank_width : float, orientation : str = 'vertical', fontsize : int = 10, rotation : int = 90, font_prop = None) -> tuple:
    """
    Creates a rectangle on the given axis representing a chronostratigraphic unit.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to draw the rectangle on.
    row : list
        A list containing the properties of the chronostratigraphic unit in the order:
        [name, rank, fontcolour, fill, age_start, age_end, shortName, mediumName].
    rank_dict : dict
        A dictionary mapping rank names to their corresponding x-axis positions.
    rank_width : float
        The width of the rectangle on the x-axis.
    orientation : str, optional
        The orientation of the rectangle ('vertical' or 'horizontal'). Default is 'vertical'.
    fontsize : int, optional
        The font size for the text labels. Default is 12.
    rotation : int, optional
        The rotation angle for the text labels. Default is 90.
    font_prop : matplotlib.font_manager.FontProperties, optional
        Font properties for the text labels. Default is None.

    Returns
    -------
    tuple
        A tuple containing the axis, the main text label, and the short name text label.
    """
    from matplotlib.patches import Rectangle
    
    if orientation == 'horizontal':
        rotation = 0
    name, rank, fontcolour, fill, age_start, age_end, shortName, mediumName = row 
    rank = rank_dict[rank]
    length = age_end - age_start
    # If the name is Hadean, set the rank_width to 5
    if name == 'Hadean':
        rank_width *= 3
        rotation = 0
    # Replace nan names with empty strings
    if pd.isna(name):
        name = ''
    
    # Draw rectangle
    if orientation == 'vertical':
        rect = Rectangle((rank, age_start), rank_width, length, facecolor=fill, edgecolor='k', linewidth=1)
    else:
        rect = Rectangle((age_start, rank), length, rank_width, facecolor=fill, edgecolor='k', linewidth=1)
    ax.add_patch(rect)

    # Center coordinates
    if orientation == 'vertical':
        x_center = rank + rank_width / 2
        y_center = age_end - length / 2
    else:  # horizontal
        x_center = age_start + length / 2
        y_center = rank + rank_width / 2
    
    from matplotlib.font_manager import FontProperties
    fontproperties = FontProperties(fname='./geofont/fgdcgeoage.ttf')
    fontproperties = font_prop

    t = ax.text( x_center, y_center, f'{name}', ha='center', va='center_baseline', rotation=rotation, color=fontcolour, fontsize=fontsize, rotation_mode='anchor' )
    t2 = ax.text( x_center, y_center, shortName, ha='center', va='center_baseline', rotation=rotation, color=fontcolour, fontsize=fontsize, rotation_mode='anchor', fontproperties=fontproperties )

    return ax, t, t2

def colour_to_rgba(colour : str | tuple) -> tuple[float, float, float, float]:
    """
    Takes in a value (primary expects either strings of matplotlib colours or hex values, or RGB tuples) and converts it to a RGBA tuple.

    Parameters
    ----------
    colour : str or tuple
        A colour in any of the following formats will be converted to an RGBA tuple: RGB, RGBA, hex, matplotlib colour strings.

    Returns
    -------
    tuple[float, float, float, float]
        The RGBA tuple representation of the color.

    Raises
    ------
    ValueError
        If the input color format is not recognised or cannot be converted to RGBA.
    """
    # Check if the color string is in hex format (e.g., '#RRGGBB' or '#RGB')
    if isinstance(colour, str) and colour.startswith('#'):
        # Convert hex to RGB and normaise to [0, 1]
        hex_color = colour.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])  # Expand shorthand hex to full form
        r, g, b = tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
        return (r, g, b, 1.0)  # Add alpha channel as fully opaque
    elif isinstance(colour, tuple) and len(colour) == 3:
        # If it's a tuple, assume it's RGB and convert to RGBA
        return (colour[0], colour[1], colour[2], 1.0)
    elif isinstance(colour, tuple) and len(colour) == 4:
        # If it's already RGBA, return it as is
        return colour
    elif isinstance(colour, str):
        # If not hex or tuple, try to use matplotlib's color conversion
        try:
            from matplotlib.colors import to_rgba
            return to_rgba(colour)
        except:
            raise ValueError(f"Colour '{colour}' is not recognised by matplotlib. A list of named colours is available at https://matplotlib.org/stable/gallery/color/named_colors.html, or you can use hex values (e.g., '#RRGGBB') or RGB tuples (e.g., (1.0, 0.0, 0.0) for red).")
    else:
        raise ValueError(f"Invalid color format: {colour}. Expected hex string, RGB tuple, or RGBA tuple.")

def read_strata_file(filename: str, formatting : "module", x_ticks_dict : dict) -> tuple[pd.DataFrame, str]:
    """
    Reads in a strata file (.csv, .txt, .xlsx) and processes it into a DataFrame suitable for stratigraphy plotting.

    Parameters
    ----------
    filename : str
        Path to the strata file.
    formatting : module
        The formatting module containing default lithologies and minerals.
    x_ticks_dict : dict
        Dictionary mapping grain size labels to float values.
    
    Returns
    -------
    tuple[pd.DataFrame, str]
        A tuple containing the processed DataFrame and the determined y_mode ('height', 'depth', or 'age').

    Raises
    ------
    ValueError
        If the file cannot be read, if required columns are missing, or if data is in an invalid format.
    FileNotFoundError
        If the specified file cannot be found.

    Notes
    -----
    Warnings are printed for any issues encountered during processing, but which do not prevent the function from successfully loading data.
    """
    from difflib import get_close_matches
    
    # Set expected column names
    columns = ['height/age', 'rock', 'thickness', 'bottom_grain', 'top_grain', 'connection_type', 'erosion', 'lenses', 'minerals', 'features', 'contact']
    # Attempt to read in file
    if filename.lower().endswith('.xlsx'):
        try:
            df = pd.read_excel(filename, header=None)
        except ValueError:
            raise ValueError(f"Error reading in the file '{filename}'. Ensure that the file is in the correct format.")
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found. Ensure that the file is in the correct directory.")
    elif filename.lower().endswith('.csv') or filename.lower().endswith('.txt'):
        try:
            df = pd.read_csv(filename, header=None)
        except ValueError:
            raise ValueError(f"Error reading in the file '{filename}'. Ensure that the file is in the correct format.")
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found. Ensure that the file is in the correct directory.")
    else:
        raise ValueError(f"File '{filename}' is not a valid .csv, .txt, or .xlsx file. Please provide a valid file.")

    # Get the dimensions of the data
    num_rows, num_cols = df.shape
    if num_cols > len(columns):
        print(f'[{path.basename(filename)}] Warning: File {filename} has more columns than expected. Expected {len(columns)}, found {num_cols}. Extra columns will be ignored.')

    # Determine if the header is all strings (otherwise no header present) and replace it with the expected columns
    header = df.iloc[0].to_list()
    if all(isinstance(item, str) for item in header):
        if all(item in columns for item in header):
            df.columns = header
        else:
            # Column headers don't match, throw warning
            if len(header) != len(columns) and header != columns[:len(header)]:
                print(f'[{path.basename(filename)}] Warning: the number of columns in {filename} ({len(header)}) does not match the expected number of columns ({len(columns)}). This may cause issues if columns are not in the expected order.')
            else:
                print(f'[{path.basename(filename)}] Warning: the columns in {filename} do not match the expected headers. Using default headers - this may cause issues if columns are not in the expected order.')
            df.columns = columns[:len(header)]
        # Remove the first row which is now the header
        df = df[1:]
        df = df.reset_index(drop=True)
    else:
        print(f"[{path.basename(filename)}] No column headers found in {filename}. Using default column names which may cause issues if columns are not in the expected order.")

    # Add any missing columns with NaN values and sort
    for col in columns:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[columns]

    #### Validite Data ####

    ## height/age
    # -------------------
    # Ensure floats
    try:
        df['height/age'] = df['height/age'].astype(float)
    except ValueError:
        non_float_values = [x for x in df["height/age"] if not isinstance(x, (float, int)) and not str(x).replace('.', '', 1).replace('-', '', 1).isdigit()]
        raise ValueError(f"[{path.basename(filename)}] Depth values in the input file must be floats, but found non-float values: {non_float_values}")
    # Determine y-mode
    if len(df) == 1:
        y_mode = 'height'
    elif df['height/age'].is_monotonic_increasing:
        y_mode = 'age'
    elif df['height/age'].is_monotonic_decreasing:
        # Choose mode depending on whether positive or negative numbers are more common
        below_zero = df['height/age'][df['height/age'] < 0].count()
        if below_zero >= len(df) / 2:
            y_mode = 'depth'
        else:
            y_mode = 'height'
    else:
        raise ValueError(f'[{path.basename(filename)}] height/age values must be either monotonically increasing or decreasing')
    
    # Adjust order for age logs
    if y_mode == 'age':
        df['height/age'] *= 1

    ## Thickness
    # -------------------
    # Infer if not provided
    thicknesses = df['height/age'].diff().shift(-1).abs().to_list()
    if df['thickness'].notnull().sum() > 0:
        user_thicknesses = df['thickness'].to_list()
        thicknesses = [user_thicknesses[i] if user_thicknesses[i] == user_thicknesses[i] else thicknesses[i] for i in range(len(thicknesses))]
    # Special case where last layer thickness is not set
    if thicknesses[-1] != thicknesses[-1]:
        if len(df) > 1:
            print(f"[{path.basename(filename)}] The thickness of the last layer ('{df.iloc[-1]['rock']}' @ y={df.iloc[-1]['height/age']}) is not set, so it is being set to be the same of the previous layer ({thicknesses[-2]:.2f}).\n > Consider setting the thickness of this layer manually if you wish for it to be displayed.")
            thicknesses[-1] = thicknesses[-2]
        else:
            print(f"[{path.basename(filename)}] The thickness of the last layer ('{df.iloc[0]['rock']}' @ y={df.iloc[0]['height/age']}) is not set, so it is being set to 10 as there are no other layers to interpolate.\n > Consider setting the thickness of this layer manually if you wish for it to be displayed.")
            thicknesses[-1] = 10.
    # Update thicknesses
    df['thickness'] = thicknesses
    # Must be floats
    try:
        df['thickness'] = df['thickness'].astype(float)
    except ValueError:
        raise ValueError('Package thickness values must be floats')

    ## Lithologies
    # -------------------
    # Remove NaNs
    rocks = df['rock'].fillna('').to_list()
    # Get list of available mineral keys
    rock_keys = [str(f) for f in formatting.lithologies.keys()]
    rock_names = [f[-1].lower() for f in formatting.lithologies.values()]
    default_rock_names = [f[-1].lower() for f in formatting.default_lithologies.values()]
    missing, suffix = [], False
    
    # For each rock, find the best matching lithology key
    for rii, rock in enumerate(rocks):
        rocks_ = rock.split(';')
        # Convert to lower, strip whitepsace and convert dashes
        rocks_ = [f.lower().strip() if isinstance(f, str) else f for f in rocks_]
        for r_i in range(len(rocks_)):
            # Check for suffixed asterisk and remove it for matching
            if rocks_[r_i].endswith('*'):
                rocks_[r_i] = rocks_[r_i][:-1].strip()
                suffix = True
            # Check for match
            if (rocks_[r_i] not in rock_keys and rocks_[r_i] not in rock_names) and rocks_[r_i] != '':
                closest_match = get_close_matches(rocks_[r_i], rock_names, n=1, cutoff=0.6)
                if closest_match:                
                    closest_match = closest_match[0]
                    missing.append( f"'{rocks_[r_i]}' not found, did you mean '{closest_match}'?")
                    # Set to 'not observed'
                    rocks_[r_i] = 'no'
                else:
                    missing.append( f"'{rocks_[r_i]}' not found, check spelling or select a different key.")
                    # Set to 'not observed'
                    rocks_[r_i] = 'no'
            else:
                # If the rock is in the list of available keys, convert it to the key if it's currently the name
                if rocks_[r_i] in default_rock_names:
                    key_index = default_rock_names.index(rocks_[r_i])
                    rocks_[r_i] = rock_keys[key_index]
                elif rocks_[r_i] in rock_names:
                    key_index = rock_names.index(rocks_[r_i])
                    rocks_[r_i] = rock_keys[key_index]
            
            if suffix:
                # Add the asterisk back if it was removed for matching
                rocks_[r_i] += '*'
                suffix = False

        # Remove empty entries and re-merge
        rocks[rii] = ';'.join([f for f in rocks_ if f != ''])
    df['rock'] = rocks

    if len(missing) > 0:
        print(f"[{path.basename(filename)}] The following desired lithologies are not available so will be ignored:")
        for m in set(missing):
            print(f"  > {m}")

    ## Grain Sizes 
    # -------------------
    labels, label_floats = list(x_ticks_dict.keys()), list(x_ticks_dict.values())
    # Convert all to str
    df['bottom_grain'] = df['bottom_grain'].astype(str)
    df['top_grain'] = df['top_grain'].astype(str)
    # Remove leading and trailing whitespace
    df['bottom_grain'] = df['bottom_grain'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['top_grain'] = df['top_grain'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    # Replace labels with floats without downcasting dtypes
    replace_dict = dict(zip(labels, label_floats))
    # Convert dict to all strings to avoid downcasting dtypes
    replace_dict = {str(k): str(v) for k, v in replace_dict.items()}
    df['bottom_grain'] = df['bottom_grain'].replace(replace_dict)
    df['top_grain'] = df['top_grain'].replace(replace_dict)
    # If there are still strings, set to NaN
    df['bottom_grain'] = pd.to_numeric(df['bottom_grain'], errors='coerce')
    df['top_grain'] = pd.to_numeric(df['top_grain'], errors='coerce')
    # If the rock is 'no' and either bottom_grain or top_grain are NaN, set them to -1 for auto-filling later depending on display_mode
    df.loc[(df['rock'] == 'no') & (df['bottom_grain'].isna()) & (df['top_grain'].isna()), ['bottom_grain', 'top_grain']] = -1
    # Swap top & bottom, fill NaNs and set float
    df['bottom_grain'], df['top_grain'] = df['bottom_grain'].fillna(df['top_grain']).fillna(1).astype(float), df['top_grain'].fillna(df['bottom_grain']).fillna(1).astype(float)

    ## Connections
    # -------------------
    available_connections = ['', 'concave', 'convex', 'sawtooth', 'sawtooth_r']
    df['connection_type'] = df['connection_type'].fillna('')
    # Convert to lower and remove leading and trailing whitespace
    df['connection_type'] = df['connection_type'].apply(lambda x: x.lower().strip() if isinstance(x, str) else x)

    # If connection type contains '^' char, set True in 'smooth' column and remove the char
    df['smooth'] = df['connection_type'].apply(lambda x: True if isinstance(x, str) and '^' in x else False)
    df['connection_type'] = df['connection_type'].apply(lambda x: x.replace('^', '') if isinstance(x, str) else x)

    # Only allow sawtooth patterns if the top & bottom grain sizes are the same
    df['connection_type'] = df.apply(lambda row: '' if row['bottom_grain'] != row['top_grain'] and row['connection_type'] in ['sawtooth', 'sawtooth_r'] else row['connection_type'], axis=1)

    missing = set(df['connection_type'].unique()) - set(available_connections)
    if missing:
        print(f"Desired connection types: {missing} are not available so will be ignored.")
        df['connection_type'] = df['connection_type'].apply(lambda x: '' if x in missing else x)

    # If the rock type is 'no', then adjust values for this edge case
    for i in range(len(df)):
        if df.loc[i, 'rock'] == 'no':
            df.loc[i, 'bottom_grain'] = min(df.loc[i, 'bottom_grain'], df.loc[i, 'top_grain'])
            df.loc[i, 'top_grain'] = df.loc[i, 'bottom_grain']
            # Also clear any minerals, lenses, or features if the rock type is 'no'
            df.loc[i, 'minerals'] = ''
            df.loc[i, 'lenses'] = ''
            df.loc[i, 'features'] = ''    
            df.loc[i, 'connection_type'] = ''

    ## Erosion
    # -------------------
    DEFAULT_AMP = 0
    DEFAULT_FREQ = 2
    # Treats values as strings, tries to separate by ';' to allow for amplitude;frequency inputs 
    erosion_vals = df['erosion'].fillna('0').astype(str).to_list()
    erosion_bottom, freq_bottom = zip(*[(parts[0] if len(parts) > 0 else DEFAULT_AMP, parts[1] if len(parts) > 1 else DEFAULT_FREQ) for parts in (x.split(';') for x in erosion_vals)])

    # Convert to float, with errors coerced to 0
    erosion_bottom = [float(x) if str(x).replace('.', '', 1).replace('-', '', 1).isdigit() else 0.0 for x in erosion_bottom]
    freq_bottom = [float(x) if str(x).replace('.', '', 1).replace('-', '', 1).isdigit() else 0.0 for x in freq_bottom]

    for i in range(len(df)):
        # If the layer is 'no', set the erosion and frequency to 0
        if df.loc[i, 'rock'] == 'no':
            erosion_bottom[i] = 0
            freq_bottom[i] = 0
        # If the next layer is 'no', set the erosion and frequency to 0
        if i < len(df) - 1 and df.loc[i + 1, 'rock'] == 'no':
            erosion_bottom[i] = 0
            freq_bottom[i] = 0
        # Ensure the last erosion & freq values are 0
        if i == len(df) - 1 and erosion_bottom[i] != 0:
            erosion_bottom[i] = 0
            freq_bottom[i] = 0

        # If the next layer is the same as this, set the erosion and freq to 0
        if i < len(df) - 1 and df.loc[i, 'rock'] == df.loc[i + 1, 'rock']:
            erosion_bottom[i] = 0
            freq_bottom[i] = 0

    # Create a list of upper erosion & freq values, starting with 0 for the top
    erosion_top = [0] + erosion_bottom[:-1]
    freq_top = [0] + freq_bottom[:-1]

    # Set the erosion & freq values back to the DataFrame
    df['erosion_bottom'] = erosion_bottom
    df['erosion_top'] = erosion_top
    df['freq_bottom'] = freq_bottom
    df['freq_top'] = freq_top

    # Finally, top erosion cannot be more than 90% the thickness of the layer above, and bottom erosion cannot be more than 90% the thickness of the layer itself
    for i in range(len(df)):
        if i > 0:
            df.loc[i, 'erosion_top'] = min(df.loc[i, 'erosion_top'], df.loc[i - 1, 'thickness']*0.9) 
        df.loc[i, 'erosion_bottom'] = min(df.loc[i, 'erosion_bottom'], df.loc[i, 'thickness']*0.9) 

    # Remove the original erosion column
    df = df.drop(columns=['erosion'])    

    ## Lenses
    # -------------------
    # Remove NaNs
    rocks = df['lenses'].fillna('').to_list()
    # Get list of available mineral keys
    rock_keys = list(formatting.lithologies.keys())
    rock_names = [f[-1].lower() for f in formatting.lithologies.values()]
    default_rock_names = [f[-1].lower() for f in formatting.default_lithologies.values()]
    missing = []
    
    # For each rock, find the best matching lithology key
    for rii, rock in enumerate(rocks):
        rocks_ = rock.split(';')
        # Convert to lower, strip whitepsace and convert dashes
        rocks_ = [f.lower().strip() if isinstance(f, str) else f for f in rocks_]
        for r_i in range(len(rocks_)):
            # Check for suffixed asterisk and remove it for matching
            if rocks_[r_i].endswith('*'):
                rocks_[r_i] = rocks_[r_i][:-1].strip()
                suffix = True
            # Check for match
            if (rocks_[r_i] not in rock_keys and rocks_[r_i] not in rock_names) and rocks_[r_i] != '':
                closest_match = get_close_matches(rocks_[r_i], rock_names, n=1, cutoff=0.6)
                if closest_match:                
                    closest_match = closest_match[0]
                    missing.append( f"'{rocks_[r_i]}' not found, did you mean '{closest_match}'?")
                    # Set to 'not observed'
                    rocks_[r_i] = 'no'
                else:
                    missing.append( f"'{rocks_[r_i]}' not found, check spelling or select a different key.")
                    # Set to 'not observed'
                    rocks_[r_i] = 'no'
            else:
                # If the rock is in the list of available keys, convert it to the key if it's currently the name
                if rocks_[r_i] in default_rock_names:
                    key_index = default_rock_names.index(rocks_[r_i])
                    rocks_[r_i] = rock_keys[key_index]
                elif rocks_[r_i] in rock_names:
                    key_index = rock_names.index(rocks_[r_i])
                    rocks_[r_i] = rock_keys[key_index]
            if suffix:
                # Add the asterisk back if it was removed for matching
                rocks_[r_i] += '*'
                suffix = False

        # Remove empty entries and re-merge
        rocks[rii] = ';'.join([f for f in rocks_ if f != ''])
    df['lenses'] = rocks

    if len(missing) > 0:
        print(f"[{path.basename(filename)}] The following desired lens lithologies are not available so will be ignored:")
        for m in set(missing):
            print(f"  > {m}")


    ## Minerals
    # -------------------
    # Remove NaNs
    minerals = df['minerals'].fillna('').to_list()
    # Get list of available mineral keys
    mineral_keys = list(formatting.minerals_list.keys())
    missing = []
    
    # For each feature, find the best matching feature key
    for mii, mineral in enumerate(minerals):
        minerals_ = mineral.split(';')
        # Convert to lower, strip whitepsace and convert dashes
        minerals_ = [f.lower().strip() if isinstance(f, str) else f for f in minerals_]
        for m_i in range(len(minerals_)):
            # Check for match
            if minerals_[m_i] not in mineral_keys and minerals_[m_i] != '':
                closest_match = get_close_matches(minerals_[m_i], mineral_keys, n=1, cutoff=0.6)
                if closest_match:                
                    closest_match = closest_match[0]
                    missing.append( f"'{minerals_[m_i]}' not found, did you mean '{closest_match}'?")
                    # Remove mineral
                    minerals_[m_i] = ''
                else:
                    missing.append( f"'{minerals_[m_i]}' not found, check spelling or select a different key.")
                    # Remove mineral
                    minerals_[m_i] = ''

        # Remove empty entries and re-merge
        minerals[mii] = ';'.join([f for f in minerals_ if f != ''])
    df['minerals'] = minerals

    if len(missing) > 0:
        print(f"[{path.basename(filename)}] The following desired minerals are not available so will be ignored:")
        for m in set(missing):
            print(f"  > {m}")

    ## Features
    # -------------------
    # Remove NaNs
    features = df['features'].fillna('').to_list()
    # Get list of available feature keys
    feature_keys = list(formatting.features.keys())
    missing, prefix = [], False

    # For each feature, find the best matching feature key
    for fii, feature in enumerate(features):
        features_ = feature.split(';')
        # Convert to lower, strip whitepsace and convert dashes
        features_ = [f.lower().strip().replace('-', '').replace('_', ' ') if isinstance(f, str) else f for f in features_]
        for f_i in range(len(features_)):
            prefix = False
            if features_[f_i].startswith('/'):
                features_[f_i] = features_[f_i][1:].strip()
                prefix = True
            # Check for match
            if features_[f_i] not in feature_keys and features_[f_i] != '':
                closest_match = get_close_matches(features_[f_i], feature_keys, n=1, cutoff=0.6)
                if closest_match:                
                    closest_match = closest_match[0]
                    missing.append( f"'{features_[f_i]}' not found, did you mean '{closest_match}'?")
                    # Remove feature
                    features_[f_i] = ''
                else:
                    missing.append( f"'{features_[f_i]}' not found, check spelling or select a different key.")
                    # Remove feature
                    features_[f_i] = ''

            # Or if default match works, reattach prefix
            elif prefix:
                features_[f_i] = '/' + features_[f_i]

        # Remove empty entries and re-merge
        features[fii] = ';'.join([f for f in features_ if f != ''])
    df['features'] = features

    if len(missing) > 0:
        print(f"[{path.basename(filename)}] The following desired features are not available so will be ignored:")
        for m in set(missing):
            print(f"  > {m}")

    ## Contacts
    # -------------------
    types = ['gradational','hard','']
    # Contacts must be a string, or empty
    df['contact'] = df['contact'].fillna('').astype(str)
    
    # If the contact is not empty, ensure it is one of the available types
    for i in range(len(df)):
        if df.loc[i, 'contact'] != '':
            # Convert to lower and remove leading and trailing whitespace
            contact = df.loc[i, 'contact'].lower().strip()
            if contact not in types:
                print(f"[{path.basename(filename)}] Desired contact type: '{contact}' is not available so it will be set to the default. Available options are: {types}.")
                df.loc[i, 'contact'] = ''

    # Shift all contact down by one, to represent top contact of following layer instead of bottom contact of current layer. Drop the last row as it will be NaN
    df['contact'] = df['contact'].shift(1)
    df['contact'] = df['contact'].fillna('')

    return df, y_mode

def parse_params(params: dict) -> dict:
    """
    Validate and normaise plotting and grain-size parameters. This function accepts a dictionary of user-supplied parameters, merges them with library defaults, validates types/values for known keys, applies preset-dependent defaults for grain-related settings, and returns a fully populated parameters dictionary.
    Invalid or unknown parameters are printed as warnings and replaced with defaults; no exceptions are raised.

    Parameters
    ----------
    params : dict
        User-supplied parameter dictionary. Keys not recognised by the function
        (other than 'self') are ignored with a printed warning. Recognised keys,
        their expected types and defaults are:
        - grain_preset : {'sedimentary', 'volcanic', 'geological'}
            Default: 'sedimentary'. Determines preset grain tick and bracket
            dictionaries if they are not provided explicitly.
        - x_ticks_dict : dict or None
            Default: None. If provided must be a dict mapping string tick labels to
            numeric values. If None, a preset mapping is selected based on
            grain_preset.
        - grain_brackets : dict or None
            Default: None. If provided must be a dict; if None a preset mapping is
            selected based on grain_preset.
        - fig : matplotlib.figure.Figure or None
            Default: None. If provided must be a matplotlib Figure instance.
        - ax : matplotlib.axes.Axes or None
            Default: None. If provided must be a matplotlib Axes instance.
        - display_mode : {'default', 'grainsize', 'log'}
            Default: 'default'. Controls size/shape-dependent defaults (e.g.
            figsize when not explicitly set).
        - feature_mode : {'default', 'merge', 'semi-merge', 'off'}
            Default: 'default'.
        - unit_borders : bool
            Default: True.
        - legend : bool
            Default: True.
        - legend_loc : {'top', 'bottom', 'right', 'left'}
            Default: 'right'.
        - legend_columns : int
            Default: 1. Must be a positive integer.
        - legend_border : bool
            Default: True.
        - figsize : tuple(float, float) or None
            Default: (10, 10). If None, defaults depend on display_mode: (3, 10)
            for 'log', otherwise (10, 10). If an invalid value is supplied the
            function warns and falls back to the appropriate default.
        - dpi : int
            Default: 150. Must be a positive integer.
        - ppi : int
            Default: 400. Must be a positive integer.
        - x_label : str
            Default: ''.
        - x_axis : bool
            Default: True.
        - y_label : str or None
            Default: None.
        - y_axis_unit : str
            Default: ''.
        - spines : bool
            Default: True.
        - mineral_size : float or None
            Default: 1. Must be a positive number if provided; otherwise will be
            coerced to None on invalid input.
        - feature_size : float
            Default: 1. Must be a positive number.
        - xmax : float, str, or None
            Default: None. If provided must be a positive number or a value in the x_ticks_dict keys.
        - legend_titles : list of str
            Default: ['Lithologies', 'Minerals', 'Sedimentary Structures',
                      'Palaeontological Features', 'Tectonic Structures',
                      'Bed Contacts'].
        - legend_kwargs : dict
            Default: {}.

    Returns
    -------
    dict
        A new dictionary containing all known parameter keys with validated and/or
        defaulted values. Unknown keys from the input are omitted (and trigger a
        printed warning). No exceptions are thrown for invalid values; instead the
        corresponding entries are replaced with defaults and a warning is printed.

    Notes
    -----
    All validation failures are handled by printing a readable warning and falling back to a documented default; the function does not raise.
    """
    import matplotlib.pyplot as plt
    # Define valid parameters and their defaults
    valid_params = {
        'grain_preset': 'sedimentary',
        'x_ticks_dict': None,
        'grain_brackets': None,
        'fig': None,
        'ax': None,
        'display_mode': 'default',
        'feature_mode': 'default',
        'unit_borders': True,
        'legend': True,
        'legend_loc': 'right',
        'legend_columns': 1,
        'legend_border': True,
        'figsize': (10, 10),
        'dpi': 150,
        'ppi': 400,
        'x_label': '',
        'x_axis': True,
        'y_label': None,
        'y_axis_unit': '',
        'spines': True,
        'mineral_size': 1,
        'feature_size': 1,
        'xmax': None,
        'legend_titles': ['Lithologies', 'Minerals', 'Sedimentary Structures', 'Palaeontological Features', 'Tectonic Structures', 'Bed Contacts'],
        'legend_kwargs': {},
    }
    result = valid_params.copy()

    for k, v in params.items():
        if k not in valid_params and k != 'self':
            print(f"Warning: Unknown parameter '{k}' will be ignored.")
            continue
        result[k] = v

    # Validation logic for stratapy.load() parameters - First check if x_ticks_dict is provided - if so, use custom, else use presets
    if result['x_ticks_dict'] is not None:
        if (
            not isinstance(result['x_ticks_dict'], dict)
            or not all(isinstance(k, str) for k in result['x_ticks_dict'].keys())
            or not all(isinstance(v, (int, float)) for v in result['x_ticks_dict'].values())
        ):
            print(f"Warning: `x_ticks_dict` must be a dictionary with string keys and numeric values. Received {type(result['x_ticks_dict']).__name__}. Defaulting to None.")
            result['x_ticks_dict'] = None
    
    # Validate grain_brackets if provided
    if result['grain_brackets'] is not None:
        if not isinstance(result['grain_brackets'], dict):
            print(f"Warning: `grain_brackets` must be a dictionary. Received {type(result['grain_brackets']).__name__}. Defaulting to None.")
            result['grain_brackets'] = None
    
    # Set defaults for x_ticks_dict if None
    if result['x_ticks_dict'] is None:
        preset = result.get('grain_preset', 'sedimentary')
        if preset not in ['sedimentary', 'volcanic', 'geological']:
            print(f"Warning: `grain_preset` must be one of 'sedimentary', 'volcanic', or 'geological'. Received '{preset}'. Defaulting to 'sedimentary'.")
            preset = 'sedimentary'
            result['grain_preset'] = preset
        if preset == 'volcanic':
            result['x_ticks_dict'] = {'vf': 1, 'f': 1.5, 'm': 2, 'c': 2.5, 'f^': 3, 'm^': 3.5, 'c^': 4, 'block/bomb': 5}
        elif preset == 'geological':
            result['x_ticks_dict'] = {'clay': 1, 'silt': 1.5, 'sand': 2.5, 'gravel': 4, 'cobble': 5, 'boulder': 6}
        else:  # sedimentary
            result['x_ticks_dict'] = {'clay': 1, 'silt': 2, 'vf': 3, 'f': 3.5, 'm': 4, 'c': 4.5, 'vc': 5, 'p': 6, 'cb': 6.5, 'b': 7.5}
    
    # Set defaults for grain_brackets if None
    if result['grain_brackets'] is None:
        preset = result.get('grain_preset', 'sedimentary')
        if preset not in ['sedimentary', 'volcanic', 'geological']:
            preset = 'sedimentary'
            result['grain_preset'] = preset
        if preset == 'volcanic':
            # result['grain_brackets'] = {'ash': ['vf', 'c'], 'lapilli': ['f^', 'c^']}
            result['grain_brackets'] = {'ash': [1, 2.5], 'lapilli': [3, 4]}
        elif preset == 'geological':
            # result['grain_brackets'] = {'fine': [1, 1.5], 'medium': [2.5], 'coarse': [4, 6]}
            result['grain_brackets'] = {}
        else:  # sedimentary
            # result['grain_brackets'] = {'sand': ['vf', 'vc'], 'gravel': ['p', 'cb']}
            result['grain_brackets'] = {'sand': [3, 5], 'gravel': [6, 6.5]}

    # Validation logic for LogObject.plot() parameters
    # fig must be None or a matplotlib figure object
    if result['fig'] is not None and not isinstance(result['fig'], plt.Figure):
        print(f"Warning: `fig` must be a matplotlib figure object or None. Received {type(result['fig']).__name__}. `None` will be used instead, creating a new figure.")
        result['fig'] = None
    # ax must be None or a matplotlib axes object
    if result['ax'] is not None and not isinstance(result['ax'], plt.Axes):
        print(f"Warning: `ax` must be a matplotlib axes object or None. Received {type(result['ax']).__name__}. `None` will be used instead, creating new axes.")
        result['ax'] = None
    # display_mode must be one of three values, otherwise defaults to 'default'
    if result['display_mode'] not in ['default', 'grainsize', 'log']:
        print(f"Warning: `display_mode` must be one of 'default', 'grainsize', or 'log'. Received '{result['display_mode']}'. Defaulting to 'default'.")
        result['display_mode'] = 'default'
    # feature_mode must be one of four values, otherwise defaults to 'default'
    if result['feature_mode'] not in ['default', 'merge', 'semi-merge', 'off']:
        if result['feature_mode'] is not None:
            print(f"Warning: `feature_mode` must be one of 'default', 'semi-merge', 'merge' or 'off'. Received '{result['feature_mode']}'. Defaulting to 'default'.")
        # Default to 'default' mode, unless display_mode is 'log', then 'merge'
        if result['display_mode'] == 'log':
            result['feature_mode'] = 'merge'
        else:
            result['feature_mode'] = 'default'
    # unit_borders must be a boolean, otherwise defaults to True
    if not isinstance(result['unit_borders'], bool):
        print(f"Warning: `unit_borders` must be a boolean. Received {type(result['unit_borders']).__name__}. Defaulting to True.")
        result['unit_borders'] = True
    # legend must be a boolean, otherwise defaults to True
    if not isinstance(result['legend'], bool):
        print(f"Warning: `legend` must be a boolean. Received {type(result['legend']).__name__}. Defaulting to True.")
        result['legend'] = True
    # legend_loc must be one of four values, otherwise defaults to 'right'
    if result['legend_loc'] not in ['top', 'bottom', 'right', 'left']:
        print(f"Warning: `legend_loc` must be one of 'top', 'bottom', 'right', or 'left'. Received '{result['legend_loc']}'. Defaulting to 'right'.")
        result['legend_loc'] = 'right'
    # legend_columns must be an integer greater than 0, otherwise defaults to 1
    if not isinstance(result['legend_columns'], int) or result['legend_columns'] <= 0:
        print(f"Warning: `legend_columns` must be a positive integer. Received {result['legend_columns']}. Defaulting to 1.")
        result['legend_columns'] = 1
    # legend_border must be a boolean, otherwise defaults to True
    if not isinstance(result['legend_border'], bool):
        print(f"Warning: `legend_border` must be a boolean. Received {type(result['legend_border']).__name__}. Defaulting to True.")
        result['legend_border'] = True
    # figsize defaults to None, which uses a default, depending on display_mode, otherwise must be a tuple of two positive floats or integers, otherwise defaults to (10, 10)
    if result['figsize'] is None:
        if result['display_mode'] == 'log':
            result['figsize'] = (3, 10)
        else:
            result['figsize'] = (10, 10)
    elif not (isinstance(result['figsize'], tuple) and len(result['figsize']) == 2 and all(isinstance(i, (int, float)) and i > 0 for i in result['figsize'])):
        if result['display_mode'] == 'log':
            result['figsize'] = (3, 10)
        else:
            result['figsize'] = (10, 10)
        print(f"Warning: `figsize` must be a tuple of two positive floats or integers. Received {params.get('figsize')}. Defaulting to {result['figsize']}.")
    # dpi must be a positive integer, otherwise defaults to 150
    if not isinstance(result['dpi'], int) or result['dpi'] <= 0:
        print(f"Warning: `dpi` must be a positive integer. Received {result['dpi']}. Defaulting to 150.")
        result['dpi'] = 150
    # ppi must be a positive integer, otherwise defaults to 400 
    if not isinstance(result['ppi'], int) or result['ppi'] <= 0:
        print(f"Warning: `ppi` must be a positive integer. Received {result['ppi']}. Defaulting to 400.")
        result['ppi'] = 400
    # x_label must be a string, otherwise defaults to an empty string
    if not isinstance(result['x_label'], str):
        print(f"Warning: `x_label` must be a string. Received {type(result['x_label']).__name__}. Defaulting to an empty string.")
        result['x_label'] = ''
    # x_axis must be a boolean, otherwise defaults to True
    if not isinstance(result['x_axis'], bool):
        print(f"Warning: `x_axis` must be a boolean. Received {type(result['x_axis']).__name__}. Defaulting to True.")
        result['x_axis'] = True
    # y_label must be a string or None, otherwise defaults to None
    if result['y_label'] is not None and not isinstance(result['y_label'], str):
        print(f"Warning: `y_label` must be a string or None. Received {type(result['y_label']).__name__}. Defaulting to None.")
        result['y_label'] = None
    # y_axis_unit must be a string, otherwise defaults to an empty string
    if not isinstance(result['y_axis_unit'], str):
        print(f"Warning: `y_axis_unit` must be a string. Received {type(result['y_axis_unit']).__name__}. Defaulting to an empty string.")
        result['y_axis_unit'] = ''
    # spines must be a boolean, otherwise defaults to False
    if not isinstance(result['spines'], bool):
        print(f"Warning: `spines` must be a boolean. Received {type(result['spines']).__name__}. Defaulting to False.")
        result['spines'] = False
    # mineral_size must be a positive float or None, otherwise defaults to None
    if result['mineral_size'] is not None and (not isinstance(result['mineral_size'], (int, float)) or result['mineral_size'] <= 0):
        print(f"Warning: `mineral_size` must be a positive float or None. Received {result['mineral_size']}. Defaulting to None.")
        result['mineral_size'] = None
    # feature_size must be a positive float or None, otherwise defaults to 1
    if not isinstance(result['feature_size'], (int, float)) or result['feature_size'] <= 0:
        print(f"Warning: `feature_size` must be a positive float. Received {result['feature_size']}. Defaulting to 1.")
        result['feature_size'] = 1
    # xmax must be a positive float, string in x_ticks_dict keys, or None, otherwise defaults to None
    if result['xmax'] is not None:
        if isinstance(result['xmax'], str):
            if result['xmax'] not in result['x_ticks_dict'].keys():
                print(f"Warning: `xmax` string value must be one of the x-tick labels: {list(result['x_ticks_dict'].keys())}. Received '{result['xmax']}'. Defaulting to None.")
                result['xmax'] = None
        elif not isinstance(result['xmax'], (int, float)) or result['xmax'] <= 0:
            print(f"Warning: `xmax` must be a positive float, a string in x-tick labels, or None. Received {result['xmax']}. Defaulting to None.")
            result['xmax'] = None
    # legend_titles must be a list of strings, otherwise defaults to the default legend titles  
    if not (isinstance(result['legend_titles'], list) and all(isinstance(title, str) for title in result['legend_titles'])):
        print(f"Warning: `legend_titles` must be a list of strings. Received {type(result['legend_titles']).__name__}. Defaulting to the default legend titles.")
        result['legend_titles'] = ['Lithologies', 'Minerals', 'Sedimentary Structures', 'Palaeontological Features', 'Tectonic Structures', 'Bed Contacts']
    # legend_kwargs must be a dictionary, otherwise defaults to an empty dictionary
    if not isinstance(result['legend_kwargs'], dict):
        print(f"Warning: `legend_kwargs` must be a dictionary. Received {type(result['legend_kwargs']).__name__}. Defaulting to an empty dictionary.")
        result['legend_kwargs'] = {}

    return result

def merge_legends_and_create_legend(logs : list, ylims : list, fig : "matplotlib.figure.Figure") -> "matplotlib.legend.Legend":
    """
    Merges lithologies, minerals, features, and contacts from all logs into the last log, computes the correct legend order, and creates the legend, returning the legend object.

    Parameters
    ----------
    logs : list
        List of LogObject instances.
    ylims : list
        List of y-limits for each log.
    fig : matplotlib.figure.Figure
        The figure to create the legend on.

    Returns
    -------
    matplotlib.legend.Legend
        The created legend object.
    """
    # Merge dictionaries into the last log's helper
    logs[-1].helper.lithologies = {k: v for l in logs for k, v in l.helper.lithologies.items()}
    logs[-1].helper.minerals_list = {k: v for l in logs for k, v in l.helper.minerals_list.items()}
    logs[-1].helper.features = {k: v for l in logs for k, v in l.helper.features.items()}
    # Also sync contacts between logs
    used_contacts = list( set( ).union( *[ set ( l.df['contact'].unique() ) for l in logs ] ) )
    # If any of the logs has erosion, add 'erosional' (if any of the values in df.erosion_bottom or df.erosion_top are greater than 0)
    if any((l.df['erosion_bottom'].fillna(0) > 0).any() or (l.df['erosion_top'].fillna(0) > 0).any() for l in logs):
        used_contacts.append('erosional')

    logs[-1].helper.required_contact_types = {k: logs[-1].helper.contact_types[k] for k in used_contacts if k in logs[-1].helper.contact_types}

    # Build legend order
    legs = []
    for l in logs:
        legs.extend(l.helper.lithology_legend)
    legs = list(dict.fromkeys(legs))  # Remove duplicates, preserve order

    # Compute bottom relative to y-limits for each log
    from pandas import concat, DataFrame
    new_df = DataFrame()
    for l_i, l in enumerate(logs):
        if l.y_mode == 'age':
            l.df['rel_bot_pc'] = abs((l.df['height/age'] + l.df['thickness']) - ylims[l_i][1]) / abs(ylims[l_i][0] - ylims[l_i][1]) * 100
        else:
            if l.y_mode == 'depth':
                ylims_ = [y * -1 for y in ylims[l_i]]
                l.df['rel_bot_pc'] = abs((-l.df['height/age'] - l.df['thickness']) - ylims_[1]) / abs(ylims_[0] - ylims_[1]) * 100
            else:
                ylims_ = (ylims[l_i][1], ylims[l_i][0])
                l.df['rel_bot_pc'] = abs((l.df['height/age'] - l.df['thickness']) - ylims_[1]) / abs(ylims_[0] - ylims_[1]) * 100
        new_df = concat([new_df, l.df[['rel_bot_pc', 'rock']]], axis=0)

    # Sort to ensure base-to-top order, then drop duplicates to get the topmost occurrence of each lithology, which is the one that should be in the legend. If y_mode is age, reverse the order to be top-to-bottom
    new_df = new_df.sort_values('rel_bot_pc', ascending=False).drop_duplicates(subset='rock', keep='last')
    legs = new_df['rock'].tolist()
    if logs[0].y_mode == 'age':
        legs = legs[::-1]

    # Create the legend using the last log's helper function, which uses the merged dictionaries to get the correct handles and labels for all properties across all logs
    leg = logs[-1].helper.make_legend(fig, legs)
    return leg

def load_image(img_path : str) -> array:
    """
    Load an image from the patterns directory, or return an empty image if not found.

    Parameters
    ----------
    img_path : str  
        The relative path to the image file within the patterns directory.
    
    Returns
    -------
    array
        The loaded image as a numpy array, or an empty image if not found.
    """
    from PIL.Image import open as Image_open
    # If the image is not in the patterns directory, use an empty image
    if path.exists(img_path):
        # Load using PIL to ensure uint8 dtype
        img = array(Image_open(img_path))
    else:
        print(f"Could not find image {img_path} in the patterns directory, using an empty image instead.")
        img = zeros((100, 100, 1))
    # If bony coal (659), adjust values
    if isinstance(img_path, str) and img_path.endswith('659.png'):
        img = clip(img, 0, 0.01)
    return img

def load_assets(df : pd.DataFrame, lithologies : dict, minerals_list : dict, features : dict) -> tuple[dict, dict, dict]:
    """
    Load media files for the plot (only those required for te log - not all)

    Parameters
    ----------  
    df : pd.DataFrame
        The DataFrame containing the stratigraphy data.
    lithologies : dict
        Dictionary of available lithologies with their properties.
    minerals_list : dict
        Dictionary of available minerals with their properties.
    features : dict
        Dictionary of available features with their properties.

    Returns
    -------
    tuple[dict, dict, dict]
        Cropped dictionaries of lithologies, minerals, and features with loaded images.
    """
    # Keep only the minerals, lithologies, and features that will be used in the plot - then load all of them to memory
    properties_used = df.rock.to_list() + df.lenses.to_list() + df.features.to_list()
    # Remove empty strings and split by ';'
    properties_used = [x.replace('^','').replace('/','') for x in properties_used if x != '']
    properties_used = set([x.strip() for sublist in properties_used for x in sublist.split(';')])

    # If lenses are present, keep the lenses in the features dict
    if any(x != '' for x in df['lenses']) or any('^' in x for x in df['features']):
        properties_used.update(['lens'])
    # Also, if any features are fragmented (preceeded with '/', add 'fragmented' to the list of properties used
    if any('/' in x for x in df['features']):
        properties_used.update(['fragmented'])

    # Keep only the lithologies/minerals/features that are in the relevant dicts
    lithologies_used = [x for x in properties_used if x in lithologies.keys()]
    features_used = [x for x in properties_used if x in features.keys()]
    # Do minerals separately
    mineral_props_used = set([x.strip() for sublist in df.minerals.to_list() for x in sublist.split(';') if x.strip() != ''])
    minerals_used = [x for x in mineral_props_used if x in minerals_list.keys()]

    # Crop the dictionaries to only those used
    lithologies = {k: lithologies[k] for k in lithologies_used}
    minerals_list = {k: minerals_list[k] for k in minerals_used}
    features = {k: features[k] for k in features_used}

    # Load all of the features
    for k, v in features.items():
        img = load_image(v[1])
        # Store the image and any other properties in the features dict
        features[k] = (v[0], img, v[-1])

    # Load all the lithologies (if images)
    for k, v in lithologies.items():
        if v[0] in ['lith', 'pattern'] and isinstance(v[1], str) and path.splitext(v[1])[1].lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
            img = load_image(v[1])
            # Store the image and any other properties in the lithologies dict  
            lithologies[k] = (v[0], img, *v[2:])

    return lithologies, minerals_list, features