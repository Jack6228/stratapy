import nox

# GitHub will automatically set up Python versions based on the matrix defined in the workflow file (ci.yaml).
@nox.session(python=False)
def ci(session):
    # Install dependency versions
    session.install("numpy==2.0.*", "pandas==2.2.*", "matplotlib>=3.9")
    # install package and test tooling
    session.install(".", "pytest")
    # Smoke-check
    session.run("python", "-c", "import stratapy, sys; print(stratapy.__version__)")
    # Run tests
    session.run("pytest", "-q")