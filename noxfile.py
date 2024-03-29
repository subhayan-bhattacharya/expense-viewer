import nox


@nox.session
def tests(session):
    session.install(".[tests]")
    session.run("pytest", "-v")


@nox.session
def lint(session):
    session.install("flake8", "mypy")
    session.install("types-python-dateutil")
    session.run("flake8", "--extend-ignore=E203", "src", "tests")
    session.run("mypy", "src", "tests")
