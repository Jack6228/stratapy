"""
Sets up custom hatch patterns and formatting for lithologies, minerals, and features used in stratigraphic plotting within the stratapy package, as well as initialising default font sizes.

Module is imported into stratapy.core.
"""

from os import path, getcwd
from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap

class SetupFormatting:
    """
    This class creates and/or initialises all of the formatting variables used within stratapy.

    Attributes
    ----------
    lithologies : dict
        A dictionary of the lithologies/strata with their hatch patterns and colors.
    minerals_list : dict
        A dictionary of the minerals with their colors and markers.
    features : dict
        A dictionary of the features with their image paths and names.
    contact_types : dict
        A dictionary of the contact types with their line styles and widths.
    default_lithologies : dict
        A dictionary of the default lithologies with their keys and names.
    direc : str
        The directory where the stratapy package is located (on the user's system).
    user_direc : str
        The current working directory of the user.
    fontsizes : dict
        A dictionary of the default font sizes used within stratapy (title, x_axis_label, y_axis_label, x_tick_labels, y_tick_labels, grain_brackets, legend_entry, legend_subtitle, chronostratigraphy).
         
    Methods
    -------
    __init__()
        Initialise the formatting variables used within stratapy.
    CreatePatchProperties()
        Set up styling for all the lithologies/strata, grains, and minerals.
    """

    def __init__(self):
        """
        Initialise the formatting variables used within stratapy.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Initialise formatting variables
        self.lithologies, self.minerals_list, self.features, self.contact_types = self.CreatePatchProperties()

        # Keep a list of the default values for reference when adding custom ones
        self.default_lithologies = {key: value[-1] for key, value in self.lithologies.items()}
        self.default_features = {key: value[-1] for key, value in self.features.items()}

        # Also create global font sizes
        self.fontsizes = {
            'title': 14,
            'x_axis_label': 14,
            'y_axis_label': 14,
            'x_tick_labels': 12.8,
            'y_tick_labels': 12.8,
            'grain_brackets': 12.8*.8,
            'legend_entry': 10,
            'legend_subtitle': 11,
            'chronostratigraphy_periods': 11,
            'chronostratigraphy_labels': 12.8,
        }

    def reset(self) -> None:
        """
        Reset the formatting variables to their default values.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Call the __init__ method to reset the formatting variables
        self.__init__()

    def CreatePatchProperties(self) -> tuple[dict[str, tuple[str, str]], dict[str, int], dict[str, tuple[str, tuple[int, int, int, int]]]]:
        """
        Set up styling dicts and vars for all the lithologies/strata, grains, and minerals.

        Parameters
        ----------
        None

        Returns
        ----------
        rock_types : dict
            A dictionary of the lithologies/strata with their hatch patterns and colors.
        mineral_types : dict   
            A dictionary of the minerals with their colors and RGBA values.
        feature_types : dict
            A dictionary of the features with their image paths and names.
        contact_types : dict
            A dictionary of the contact types with their line styles and widths.
        """
        # A dict of FGDC lithologies (key: name, color/colormap for the coloured version)
        FGDC_lithologies = { 
            '601': ('Fine gravel', (236/255, 180/255, 0/255)),
            '602': ('Coarse gravel', (236/255, 180/255, 0/255)),
            '603': ('Crossbedded gravel', (183/255, 217/255, 204/255)),
            '605': ('Fine breccia', (167/255, 186/255, 134/255)),
            '606': ('Coarse breccia', (167/255, 186/255, 134/255)),
            '607': ('Massive sandstone', (253/255, 244/255, 63/255)),
            '608': ('Bedded sandstone', (253/255, 244/255, 63/255)),
            '609': ('Crossbedded sandstone', (253/255, 244/255, 63/255)),
            '610': ('Crossbedded sandstone', (253/255, 244/255, 63/255)),
            '611': ('Ripple-bedded sandstone', (253/255, 244/255, 63/255)),
            '612': ('Argillaceous sandstone', (225/255, 240/255, 216/255)),
            '613': ('Calcareous sandstone', (154/255, 206/255, 254/255)),
            '614': ('Dolomitic sandstone', (205/255, 255/255, 217/255)),
            '616': ('Siltstone', (255/255, 211/255, 69/255)),
            '617': ('Calcareous siltstone', (146/255, 220/255, 183/255)),
            '618': ('Dolomitic siltstone', (146/255, 220/255, 183/255)),
            '619': ('Sandy shale', (219/255, 254/255, 188/255)),
            '620': ('Clay', (219/255, 254/255, 188/255)),
            '620b': ('Mudstone', (76/255, 79/255, 74/255)),
            '621': ('Cherty shale', (219/255, 254/255, 188/255)),
            '622': ('Dolomitic shale', (219/255, 254/255, 188/255)),
            '623': ('Calcareous shale', (219/255, 254/255, 188/255)),
            '624': ('Shale', (219/255, 254/255, 188/255)),
            '625': ('Oil shale', (187/255, 255/255, 221/255)),
            '626': ('Chalk', (86/255, 224/255, 252/255)),
            '627': ('Limestone', (67/255, 175/255, 249/255)),
            '628': ('Clastic limestone', (56/255, 180/255, 177/255)),
            '629': ('Fossiliferous clastic limestone', (86/255, 224/255, 252/255)),
            '630': ('Nodular limestone', (67/255, 175/255, 249/255)),
            '631': ('Saccharoidal dolomite', (67/255, 175/255, 249/255)),
            '632': ('Crossbedded limestone', (67/255, 175/255, 249/255)),
            '633': ('Cherty crossbedded limestone', (67/255, 175/255, 249/255)),
            '634': ('Cherty and sandy crossbedded clastic limestone', (67/255, 175/255, 249/255)),
            '635': ('Oolitic limestone', (67/255, 175/255, 249/255)),
            '636': ('Sandy limestone', (67/255, 175/255, 249/255)),
            '637': ('Silty limestone', (67/255, 175/255, 249/255)),
            '638': ('Argillaceous limestone', (67/255, 175/255, 249/255)),
            '639': ('Cherty limestone', (67/255, 175/255, 249/255)),
            '640': ('Cherty limestone', (67/255, 175/255, 249/255)),
            '641': ('Dolomitic limestone', (67/255, 175/255, 249/255)),
            '642': ('Dolostone', (107/255, 195/255, 255/255)),
            '643': ('Crossbedded dolostone', (107/255, 195/255, 255/255)),
            '644': ('Oolitic dolostone', (107/255, 195/255, 255/255)),
            '645': ('Sandy dolostone', (107/255, 195/255, 255/255)),
            '646': ('Silty dolostone', (107/255, 195/255, 255/255)),
            '647': ('Argillaceous dolostone', (107/255, 195/255, 255/255)),
            '648': ('Cherty dolostone', (107/255, 195/255, 255/255)),
            '649': ('Bedded chert', (154/255, 191/255, 192/255)),
            '650': ('Bedded chert', (154/255, 191/255, 192/255)),
            '651': ('Fossiliferous bedded chert', (154/255, 191/255, 192/255)),
            '652': ('Fossiliferous rock', (56/255, 180/255, 177/255)),
            '653': ('Diatomaceous rock', (205/255, 22/255, 255/255)),
            '654': ('Graywacke', (184/255, 234/255, 195/255)),
            '655': ('Crossbedded graywacke', (184/255, 234/255, 195/255)),
            '656': ('Ripple-bedded graywacke', (184/255, 234/255, 195/255)),
            '657': ('Peat', (255/255, 207/255, 129/255)),
            '658': ('Coal', 'gray'),
            '659': ('Impure coal', 'gray_r'),
            '660': ('Underclay', (213/255, 230/255, 204/255)),
            '661': ('Flint clay', (213/255, 230/255, 204/255)),
            '662': ('Bentonite', (192/255, 208/255, 192/255)),
            '663': ('Glauconite', (96/255, 204/255, 191/255)),
            '664': ('Limonite', (254/255, 198/255, 42/255)),
            '665': ('Siderite', (254/255, 160/255, 96/255)),
            '666': ('Phosphatic-nodular rock', (191/255, 227/255, 220/255)),
            '667': ('Gypsum', (206/255, 157/255, 255/255)),
            '668': ('Salt', (1/255, 156/255, 205/255)),
            '669': ('Interbedded sandstone and siltstone', (146/255, 220/255, 183/255)),
            '670': ('Interbedded sandstone and shale', (219/255, 254/255, 188/255)),
            '671': ('Interbedded ripple-bedded sandstone and shale', (219/255, 254/255, 188/255)),
            '672': ('Interbedded shale and silty limestone', (172/255, 228/255, 200/255)),
            '673': ('Interbedded shale and limestone', (172/255, 228/255, 200/255)),
            '674': ('Interbedded shale and limestone', (172/255, 228/255, 200/255)),
            '675': ('Interbedded calcareous shale and limestone', (172/255, 228/255, 200/255)),
            '676': ('Interbedded silty limestone and shale', (172/255, 228/255, 200/255)),
            '677': ('Interbedded limestone and shale', (172/255, 228/255, 200/255)),
            '678': ('Interbedded limestone and shale', (172/255, 228/255, 200/255)),
            '679': ('Interbedded limestone and shale', (67/255, 175/255, 249/255)),
            '680': ('Interbedded limestone and calcareous shale', (67/255, 175/255, 249/255)),
            '681': ('Till', (210/255, 194/255, 124/255)),
            '682': ('Till', (210/255, 194/255, 124/255)),
            '683': ('Till', (210/255, 194/255, 124/255)),
            '684': ('Loess', (245/255, 225/255, 189/255)),
            '685': ('Loess', (245/255, 225/255, 189/255)),
            '686': ('Loess', (245/255, 225/255, 189/255)),
            '701': ('Metamorphism', (167/255, 167/255, 255/255)),
            '702': ('Quartzite', (159/255, 255/255, 159/255)),
            '703': ('Slate', (230/255, 205/255, 255/255)),
            '704': ('Schistose', (219/255, 219/255, 231/255)),
            '705': ('Schist', (219/255, 219/255, 231/255)),
            '706': ('Contorted schist', (219/255, 219/255, 231/255)),
            '707': ('Schist and gneiss', (236/255, 214/255, 254/255)),
            '708': ('Gneiss', (236/255, 214/255, 254/255)),
            '709': ('Contorted gneiss', (236/255, 214/255, 254/255)),
            '711': ('Tuffaceous rock', (249/255, 211/255, 211/255)),
            '712': ('Crystal tuff', (249/255, 211/255, 211/255)),
            '713': ('Devitrified tuff', (249/255, 211/255, 211/255)),
            '714': ('Volcanic breccia/tuff', (255/255, 239/255, 217/255)),
            '715': ('Volcanic breccia/agglomerate', (255/255, 213/255, 157/255)),
            '716': ('Zeolitic rock', (233/255, 255/255, 233/255)),
            '717': ('Basaltic flows', (221/255, 179/255, 151/255)),
            '719': ('Granite', (249/255, 181/255, 187/255)),
            '720': ('Banded igneous rock', (185/255, 149/255, 152/255)),
            '721': ('Igneous rock', (255/255, 183/255, 222/255)),
            '722': ('Igneous rock', (255/255, 183/255, 222/255)),
            '723': ('Igneous rock', (244/255, 139/255, 0/255)),
            '724': ('Igneous rock', (244/255, 139/255, 0/255)),
            '725': ('Igneous rock', (235/255, 96/255, 1/255)),
            '726': ('Igneous rock', (235/255, 96/255, 1/255)),
            '727': ('Igneous rock', (147/255, 60/255, 1/255)),
            '728': ('Igneous rock', (147/255, 60/255, 1/255)),
            '729': ('Porphyritic rock', (255/255, 225/255, 232/255)),
            '730': ('Porphyritic rock', (255/255, 225/255, 232/255)),
            '731': ('Vitrophyre', (255/255, 195/255, 248/255)),
            '732': ('Quartz', (159/255, 255/255, 159/255)),
            '901': ('Ash', (235/255, 96/255, 1/255)),
            '902': ('Bedded ash', (235/255, 96/255, 1/255)),
            '903': ('Crossbedded tephra', (235/255, 96/255, 1/255)),
            '904': ('Tephra (20% lithics)', (235/255, 96/255, 1/255)),
            '904-1': ('Tephra (40% lithics)', (235/255, 96/255, 1/255)),
            '904-2': ('Tephra (60% lithics)', (235/255, 96/255, 1/255)),
            '904-3': ('Tephra (80% lithics)', (235/255, 96/255, 1/255)),
        }
        # Key prefixes for FGDC patterns
        FGDC_patterns = [101, 102, 103, 104, 105, 106, 114, 116, 117, 118, 119, 120, 121, 122, 123, 124, 132, 134, 135, 136, 137, 201, 202, 204, 206, 207, 214, 215, 216, 217, 218, 219, 226, 228, 229, 230, 231, 232, 233, 301, 302, 303, 304, 305, 306, 313, 314, 315, 316, 317, 318, 319, 327, 328, 330, 331, 401, 402, 403, 405, 406, 411, 412, 416, 417, 418, 419, 420, 423, 424, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 521, 522, 523, 591, 592, 593, 594]

        # 'rock_types' is a dict of tuples representing formatting for all lithological or pattern fills. The first string in the tuple represents the type of fill ('fill', 'lith', 'pattern').
        rock_types = {'no': ('fill', 'w', '', 'k', 'Not observable')}

        # Create a custom colourmap like gray_r but which is transparent instead of white. Ensures visibility of patterns regardless of background colour.
        cmap_transparent = LinearSegmentedColormap.from_list('custom_cmap_transparent', [(0,0,0,0), (0,0,0,1)], N=256)

        # Add each FGDC lithology with tuple (type, url, cmap, name)
        for k, v in FGDC_lithologies.items():
            # The colour/colourmap in the dict is for the coloured version of the pattern. If a colour, make it a colourmap
            if v[1] not in colormaps():
                cmap = LinearSegmentedColormap.from_list('custom_cmap', [v[1], 'k'], N=256)
            else:
                cmap = v[1]
            # Add the lithology to the rock_types dict with tuple (type, url, cmap, name) - with a black & white version, and a coloured version, suffixed with '*'
            
            rock_types[k] = ('lith', f'{k}.png', cmap_transparent, v[0])

            rock_types[k+'*'] = ('lith', f'{k}.png', cmap, v[0])

        # Overwrite coal to use 'k' colourmap as the image is inverted
        rock_types['658'] = ('lith', '658.png', LinearSegmentedColormap.from_list('custom_cmap', ['k', 'k'], N=256), 'Coal')
            
        # Add each pattern using the -K option for each pattern, apart from 426 which only has -CMYK, with tuple (type, url, cmap, name)
        for code in FGDC_patterns:
            # Use the -K option, unless 426 then -CMYK. Set all to use 'gray' colourmap
            if code == 426:
                rock_types[str(code)] = ('pattern', f'{str(code)}-CMYK.png', cmap_transparent, str(code))
            else:
                rock_types[str(code)] = ('pattern', f'{str(code)}-K.png', cmap_transparent, str(code))

        # Create the default minerals with tuple (fillcolor, edgecolor, marker). Display names are the title case of the key
        mineral_types = {
                    'amphibole': ('green', 'green', 'D'),
                    'anhydrite': ('cornsilk', 'darkkhaki', 'o'),
                    'anorthite': ('g', None, 's'), 
                    'aragonite': ('orangered', None, 'd'), 
                    'augite': ('g', None, 's'),
                    'biotite': ('chocolate', None, '|'),
                    'calcite': ('gray', None, 'd'),
                    'celestite': ('lightskyblue', None, '*'),
                    'chert': ('gray', None, 'o'), 
                    'chlorite': ('green', None, 's'), 
                    'chrysotile': ('dodgerblue', None, '|'), 
                    'clinopyroxene': ('darkgreen', None, 's'),
                    'diopside': ('darkgreen', None, 's'), 
                    'dolomite': ('gold', 'gray', 'd'),
                    'epidote': ('palegreen', None, '|'), 
                    'flint': ('gray', None, 's'),
                    'fluorite': ('purple', None, 's'),
                    'garnet': ('red', None, 'h'),
                    'glauconite': ('springgreen', None, 'o'),
                    'gypsum': ('whitesmoke', 'darkgray', 's'),
                    'halite': ('lavenderblush', 'orchid', 's'),
                    'hematite': ('firebrick', None, 'o'),
                    'hornblende': ('green', 'brown', 'h'), 
                    'illite': ('gray', None, 'h'), 
                    'jasper': ('orangered', None, 'o'),
                    'kaolinite': ('aliceblue', 'royalblue', 'h'),
                    'k-feldspar': ('pink', None, 's'),
                    'lizardite': ('dodgerblue', None, '|'),
                    'magnetite': ('black', None, 'o'),
                    'microcline': ('pink', None, 's'), 
                    'muscovite': ('silver', None, 's'), 
                    'olivine': ('forestgreen', 'forestgreen', 'o'),
                    'orthoclase': ('pink', None, 'v'), 
                    'orthopyroxene': ('g', None, 's'),
                    'plagioclase': ('gray', None, 's'),
                    'pyrite': ('gold', None, 's'),
                    'quartz': ('gray', 'lightgray', 'd'),
                    'siderite': ('orange', None, 'o'),
                    'smectite': ('purple', None, 'h'), 
                    'spinel': ('steelblue', None, 's'), 
                    'titanite': ('mediumvioletred', None, 'd'), 
                    'tourmaline': ('r', None, 'd'), 
                    'volcanic glass': ('k', None, 6),  
                    'zeolites': ('whitesmoke', 'k', 'o'),
                    'zircon': ('k', None, 's'),
                }

        # Create the default features list with tuple (type, image path, name)
        feature_types = {
            # Palaeontological
            'ammonite': ('fossil', 'Ammonite.png', 'Ammonite'),
            'arthropod': ('fossil', 'Arthropod.png', 'Arthropod'),
            'archaeocyath sponge': ('fossil', 'ArchaeocyathSponge.png', 'Archaeocyath sponge'),
            'benthic foraminifera': ('fossil', 'benthic foraminifera.png', 'Benthic foraminifera'),
            'bivalve': ('fossil', 'bivalve.png', 'Bivalve'),
            'brachiopod': ('fossil', 'Brachiopod.png', 'Brachiopod'),
            'bryozoan': ('fossil', 'Bryozoan.png', 'Bryozoan'),
            'charcoal': ('fossil', 'Charcoal.png', 'Charcoal'),
            'colonial coral': ('fossil', 'Colonial coral.png', 'Colonial coral'),
            'conodont': ('fossil', 'Conodont.png', 'Conodont'),
            'coralline algae': ('fossil', 'Coralline algae.png', 'Coralline algae'),
            'crinoid': ('fossil', 'Crinoid.png', 'Crinoid'),
            'diatom': ('fossil', 'Diatom.png', 'Diatom'),
            'echinoderm': ('fossil', 'Echinoderm.png', 'Echinoderm'),
            'fragmented': ('fossil', 'fragmented.png', 'Fragmented'),
            'fungal spore': ('fossil', 'Fungal spore.png', 'Fungal spore'),
            'gastropod': ('fossil', 'gastropod.png', 'Gastropod'),
            'graptolite': ('fossil', 'Graptolite.png', 'Graptolite'),
            'green algae': ('fossil', 'Green algae.png', 'Green algae'),
            'leaf': ('fossil', 'Leaf.png', 'Leaf'),
            'microbial mat': ('fossil', 'Microbial mat.png', 'Microbial mat'),
            'mollusc': ('fossil', 'Mollusc.png', 'Mollusc'),
            'ooid': ('fossil', 'Ooid.png', 'Ooid'),
            'ostracod': ('fossil', 'Ostracod.png', 'Ostracod'),
            'pecten shell': ('fossil', 'Pecten shell.png', 'Pecten shell'),
            'pelagic foraminifera': ('fossil', 'Pelagic foraminifera.png', 'Pelagic foraminifera'),
            'pollen': ('fossil', 'Pollen.png', 'Pollen'),
            'radiolarian': ('fossil', 'Radiolarian.png', 'Radiolarian'),
            'rhizolith': ('fossil', 'Rhizolith.png', 'Rhizolith'),
            'serpulid': ('fossil', 'Serpulid worm.png', 'Serpulid'),
            'shell hash': ('fossil', 'Shell hash.png', 'Shell hash'),
            'solitary coral': ('fossil', 'Solitary coral.png', 'Solitary coral'),
            'stromatolite': ('fossil', 'Stromatolite.png', 'Stromatolite'),
            'tooth': ('fossil', 'Tooth.png', 'Tooth'),
            'trace fossil': ('fossil', 'Trace fossil.png', 'Trace fossil'),      
            'trilobite': ('fossil', 'Trilobite.png', 'Trilobite'),
            'vertebrate bone': ('fossil', 'Vertebrate bone.png', 'Vertebrate Bone'),
            'wood': ('fossil', 'Wood.png', 'Wood'),

            # Sedimentary
            'bioturbation high': ('structure', 'bioturbation_high.png', 'Bioturbation (high)'),
            'bioturbation medium': ('structure', 'bioturbation_med.png', 'Bioturbation (med.)'),
            'bioturbation low': ('structure', 'bioturbation_low.png', 'Bioturbation (low)'),
            'bored clast': ('structure', 'bored_clast.png', 'Bored clast'),
            'clast imbrication': ('structure', 'clast_imbrication.png', 'Clast imbrication'),
            'clasts': ('structure', 'clasts_gravel.png', 'Clasts'),
            'climbing ripples': ('structure', 'climbing_ripples.png', 'Climbing ripples'),
            'concretions': ('structure', 'concretions.png', 'Concretions'),
            'convolute bedding': ('structure', 'convolute_bedding.png', 'Convolute bedding'),
            'cross bedding': ('structure', 'cross_bedding.png', 'Cross-bedding'),
            'current ripple': ('structure', 'current_ripple.png', 'Current ripple'),
            'dewatering structures': ('structure', 'dewatering_structures.png', 'Dewatering structures'),
            'flute marks': ('structure', 'flute_marks.png', 'Flute marks'),
            'groove marks': ('structure', 'groove_marks.png', 'Groove marks'),
            'herringbone cross stratification': ('structure', 'herringbone_crossstratification.png', 'Herringbone cross-stratification'),
            'hummocky cross stratification': ('structure', 'hummocky.png', 'Hummocky cross-stratification'),
            'lens': ('structure', 'LenticularLens.png', 'Lenticular lens'),
            'lenticular bedding': ('structure', 'lenticular_bedding.png', 'Lenticular bedding'),
            'load clasts': ('structure', 'load_clast.png', 'Load clasts'),
            'dessication cracks': ('structure', 'mudcracks.png', 'Dessication cracks'),
            'normal grading': ('structure', 'normal_grading.png', 'Normal grading'),
            'planar crossbedding': ('structure', 'planar_cross_bedding.png', 'Planar cross-bedding'),
            'planar laminations': ('structure', 'planar_laminations.png', 'Planar laminations'),
            'reverse grading': ('structure', 'reverse_grading.png', 'Reverse grading'),
            'rip up clasts': ('structure', 'ripup_clasts.png', 'Rip-up clasts'),
            'scours': ('structure', 'scour_marks.png', 'Scours'),
            'striations': ('structure', 'striations_lineations.png', 'Striations'),
            'stylolites': ('structure', 'stylolites.png', 'Stylolites'),
            'swaley cross stratification': ('structure', 'swaley.png', 'Swaley cross-stratification'),
            'trough crossbedding': ('structure', 'trough_cross_bedding.png', 'Trough cross-bedding'),

            # Tectonic
            'anticline': ('tectonic', 'anticline.png', 'Anticline'),
            'syncline': ('tectonic', 'syncline.png', 'Syncline'),
            'plunging anticline': ('tectonic', 'plunging_anticline.png', 'Plunging anticline'),
            'plunging syncline': ('tectonic', 'plunging_syncline.png', 'Plunging syncline'),
            'normal fault': ('tectonic', 'normal_fault.png', 'Normal fault'),
            'thrust fault': ('tectonic', 'thrust_fault.png', 'Thrust fault'),
            'horizontal strata': ('tectonic', 'horizontal_strata.png', 'Horizontal strata'),
            'vertical strata': ('tectonic', 'vertical_strata.png', 'Vertical strata'),
            'strike slip fault': ('tectonic', 'strike-slip_fault.png', 'Strike-slip fault'),
        }   
        
        # Prefix filepaths with the features or patterns folder of package assets
        features_dir = path.join( path.dirname(path.abspath(__file__)), 'assets', 'features')
        for k, v in feature_types.items():
            feature_types[k] = (v[0], path.join(features_dir, v[1]), v[2])
        patterns_dir = path.join( path.dirname(path.abspath(__file__)), 'assets', 'patterns')
        for k, v in rock_types.items():
            if k != 'no':
                rock_types[k] = (v[0], path.join(patterns_dir, v[1]), v[2], v[3])
        
        # Create the available contact types with tuple (linewidth, linestyle, color, name)
        contact_types = {
            '': (.75, 'solid', 'k', 'Normal'),
            'hard': (1.75, 'solid', 'k', 'Sharp'),
            'gradational': (1.5, (0, (5, 3)), 'k', 'Gradational'),
            'erosional': (.75, 'solid', 'k', 'Erosional'),
        }

        return rock_types, mineral_types, feature_types, contact_types
    
class Config:
    """
    Finds the directory of the package and the directory where the user is running the code from.
    """

    def __init__(self):
        """
        Initialise the config variables used within stratapy.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        # Get the directory of the package
        self.direc = path.dirname(path.abspath(__file__))
        # Get the directory where the user is running the code
        self.user_direc = getcwd()

# Initialise both classes for use in other modules
formatting = SetupFormatting()
config = Config()