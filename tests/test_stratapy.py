from pathlib import Path
import copy

import matplotlib
matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt
import pytest
import stratapy as sp


@pytest.fixture(autouse=True)
def _close_figures():
    """Prevent matplotlib figure buildup across tests."""
    yield
    plt.close("all")


def test_import_and_metadata():
    assert hasattr(sp, "__version__")
    assert isinstance(sp.__version__, str)
    assert len(sp.__version__) > 0


def test_load_example_file():
    log = sp.load("examples.tutorial.csv")
    assert log is not None
    assert hasattr(log, "df")
    assert len(log.df) > 0
    assert log.y_mode in {"height", "depth", "age"}


@pytest.mark.parametrize("display_mode", ["default", "grainsize", "log"])
def test_plot_display_modes_smoke(display_mode):
    log = sp.load("examples.tutorial.csv")
    log.plot(display_mode=display_mode, dpi=100)
    assert hasattr(log, "fig")
    assert hasattr(log, "ax")


def test_save_adds_png_extension_when_missing(tmp_path: Path):
    log = sp.load("examples.tutorial.csv")
    log.plot(dpi=100)

    out_base = tmp_path / "soft_release_output"
    log.save(str(out_base))  # no extension -> should save .png

    assert (tmp_path / "soft_release_output.png").exists()


def test_add_samples_and_twin_axis_smoke():
    log = sp.load("examples.sedimentary_log.csv")
    log.plot(display_mode="log", dpi=100)
    log.add_samples([1.35, 2.2, 2.9], label="Samples")
    log.add_twin_axis(0.27, label="Above Sea Level (m)")
    assert hasattr(log, "ax")


def test_add_chronostratigraphy_smoke():
    # Matches tutorial/manuscript age-based usage
    log = sp.load("examples.age_based_log_Ka.csv")
    log.plot(y_axis_unit="ka", dpi=100)
    log.add_chronostratigraphy(ranks_to_display=[3, 4, 5], width_ratio=0.25, spacing=0.03)
    assert hasattr(log, "chrono_ax")


def test_multi_fig_smoke_and_save(tmp_path: Path):
    files = ["examples.multi_log_1.csv", "examples.multi_log_2.csv"]
    panel = sp.multi_fig(
        files,
        nrows=1,
        ncols=2,
        sharex=True,
        legend=False,
        dpi=100,
    )
    assert len(panel.logs) == 2
    assert len(panel.axes) == 2

    out_file = tmp_path / "multi_fig_soft_release.png"
    panel.save(str(out_file))
    assert out_file.exists()


def test_correlated_logs_smoke_and_save(tmp_path: Path):
    files = ["examples.multi_log_1.csv", "examples.multi_log_2.csv"]
    panel = sp.correlated_logs(
        files,
        legend=False,
        dpi=100,
    )
    assert len(panel.logs) == 2
    assert len(panel.axes) == 2

    out_file = tmp_path / "correlated_soft_release.png"
    panel.save(str(out_file))
    assert out_file.exists()


def test_standalone_legend_smoke(tmp_path: Path):
    out_file = tmp_path / "legend_soft_release.png"
    sp.standalone_legend(
        ["examples.tutorial.csv", "examples.sedimentary_log.csv"],
        filename=str(out_file),
        dpi=100,
        legend_columns=2,
    )
    assert out_file.exists()


def test_update_helpers_smoke_with_restore():
    # Protect global mutable formatting state
    lithologies_before = copy.deepcopy(sp.formatting.lithologies)
    minerals_before = copy.deepcopy(sp.formatting.minerals_list)
    features_before = copy.deepcopy(sp.formatting.features)

    try:
        sp.update_minerals({"pytest_garnet": ("#FF00FF", "k", "d")})
        sp.update_lithologies({"pytest_lith": ("limestone", "tan", "Pytest Lithology")})
        sp.update_features({"pytest_scaphopod": ("", "trace fossil", "Pytest Scaphopod")})

        assert "pytest_garnet" in sp.formatting.minerals_list
        assert "pytest_lith" in sp.formatting.lithologies
        assert "pytest_scaphopod" in sp.formatting.features
    finally:
        sp.formatting.lithologies = lithologies_before
        sp.formatting.minerals_list = minerals_before
        sp.formatting.features = features_before