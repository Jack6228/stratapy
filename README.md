<div align="center">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Jack6228/stratapy/main/docs/_static/stratapy_horizontal_dark_mode.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Jack6228/stratapy/main/docs/_static/stratapy_horizontal.png">
    <img alt="stratapy Logo" src="https://raw.githubusercontent.com/Jack6228/stratapy/main/docs/_static/stratapy_horizontal.png" width="400">
</picture>
</div>

**A Tool for Automated Stratigraphic Log Visualisation**

A Python-based framework for automated visualisation of creating standardised, reproducible, and digitally integrated stratigraphic logs.

[![PyPI](https://img.shields.io/badge/PyPI-stratapy-FCB001?logo=pypi)](https://pypi.org/project/stratapy/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19320013-blue)](https://doi.org/10.5281/zenodo.19320013)
[![Docs](https://img.shields.io/badge/ReadTheDocs-latest-8ca1af?logo=readthedocs)](https://stratapy.readthedocs.io/en/latest/?badge=latest)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jack6228/stratapy/blob/main/examples/ManuscriptFigures.ipynb)

## Key Features

  * **Simple Input Format:** Use CSV, Excel or similar files to structure your data with a range of supported column types (lithology, grain size, features, lenses, contacts, etc.) and let stratapy handle the visualisation

  * **Vast Customisation:** Tailor every aspect of your logs, from layout and styling to colours and symbology, with a simple parameter-based interface

  * **Standardised Symbology:** Access a curated library of geological symbols and patterns, including USGS standard lithology patterns

  * **Multi-Figure Functionality:** Create complex, multi-panel figures with ease, enabling comprehensive visualisation of stratigraphic data

  * **Publication-Quality Output:** Generate high-resolution figures suitable for academic publication and professional presentations

  * **Accessible for Non-Programmers:** Designed with user-friendliness in mind, enabling geoscientists of all programming skill levels to create stunning visualisations

<div align="center">
    <picture>
        <img src="https://raw.githubusercontent.com/Jack6228/stratapy/main/docs/_static/readme_example.png" alt="Making logs with stratapy" width="600">
    </picture>
</div>

For more examples, see the [documentation](https://stratapy.readthedocs.io/en/latest/) or try it out online with this [Google Colab notebook](https://colab.research.google.com/github/Jack6228/stratapy/blob/main/examples/ManuscriptFigures.ipynb).

## Quick Start

### Installation

```bash
pip install stratapy
```

### Basic Usage

```python
import stratapy as sp

# Load and plot a log
log = sp.load_log('path/to/file.csv')
log.plot()
log.save('output.png')
```

### Multi-Panel Figures

```python
import stratapy as sp

# Automatically plot multiple logs in a single figure
files = ['log1.csv', 'log2.csv', 'log3.csv']
panel = sp.multi_fig(files)
panel.save('output.png')
```

### Use Online - No Installation Required

Try out stratapy immediately without any installation using this [Google Colab notebook](https://colab.research.google.com/github/Jack6228/stratapy/blob/main/examples/ManuscriptFigures.ipynb).

See the [Online Platforms](https://stratapy.readthedocs.io/en/latest/getting_started/installation/online_platforms.html) section of the documentation for more details.

## Documentation

For full API reference and tutorials, visit [our ReadTheDocs page](https://stratapy.readthedocs.io/en/latest/).

## Citation

If you use this software in your research or otherwise, please cite it as follows:

> Smith, J. L., Antoniou, C., & Alexander, R. (2026). stratapy: A Tool for Automated Stratigraphic Log Visualisation (v0.9.1). Zenodo. https://doi.org/10.5281/zenodo.19320013

For detailed citation metadata, see [`CITATION.cff`](CITATION.cff) or use the following BibTeX entry:

```bibtex
@software{smith_stratapy_2026,
  author       = {Smith, Jack Lee and Antoniou, Christina and Alexander, Ruaridh},
  title        = {stratapy: A Tool for Automated Stratigraphic Log Visualisation},
  month        = mar,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v0.9.1},
  doi          = {10.5281/zenodo.19320013},
  url          = {https://doi.org/10.5281/zenodo.19320013},
}
```
## License

Distributed under the **BSD 3-Clause License**. See `LICENSE` for more information.