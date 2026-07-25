Changelog
=========

All notable changes to this project will be documented in this file.

v1.0.1
------
July 25th, 2026

- Added a new optional parameter to `LogObject.plot()` called `consec_units` which allows users to choose whether consecutive units of the same rock type should be combined into a single stratum (default behaviour) or plotted separately with individual bed contacts. See GitHub issue #1 for more details.

v1.0.0
------
June 28th, 2026

**stratapy V1.0 releases! Find the paper in Scientific Reports**: https://www.nature.com/articles/s41598-026-58501-2

- Updated default grain size axis to be 'clastic' instead of 'sedimentary' and 'geological' to be 'sedimentary'. Added new grain size presets for the extended Dunham classification and a carbonate scale from Leighton and Pendexter.
- Added ability to add custom contact types through `stratapy.update_contacts()`.
- Added continuous integration and provided comprehensive test coverage for the package, including fixing some incompatibilities with older versions of Python.
- Fixed an issue where white lithology patterns were not displaying as transparent when ``transparent=True`` was used in the save method.

v0.9.2
------
May 4th, 2026

- Fixed issues with smoothing of unit borders.
- Updated default grain size axis values.
- Fixed issue with API reference not displaying in the documentation.
- Fixed issues with font sizes and added an annotated figure showing all available font size keys.
- Other minor bug fixes and improvements post-release.
- stratapy visits EGU! https://doi.org/10.5194/egusphere-egu26-18130

v0.9.1
------
March 29th, 2026

- Quick link fixes and other minor release tweaks.

v0.9.0
------
March 29th, 2026

- Initial release of stratapy, including all core features and functionality.


