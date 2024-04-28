from invoke import task

edge = "EDGEDB_INSTANCE=wat_test"

pr = "poetry run"


def pytest_params(lf, debug):
    lf = "--lf" if lf else ""
    debug = "--log-level=DEBUG -vv" if debug else ""
    return f"{lf} {debug}"


@task
def unit(c, lf=False, debug=False):
    c.run(
        f"{pr} pytest --code-highlight=yes {pytest_params(lf, debug)} tests/unit",
        pty=True,
    )


@task
def test_db(c):
    c.run(
        """
        edgedb instance destroy --force --non-interactive -I wat_test || true
        edgedb instance create --non-interactive wat_test
        edgedb migrate -I wat_test
        """,
        pty=True,
    )


@task
def feature(c):
    c.run(f"{pr} behave tests/behave/features", pty=True)


@task(test_db)
def func(c, lf=False, debug=False):
    c.run(f"{edge} {pr} pytest {pytest_params(lf, debug)} tests/functional", pty=True)


@task(test_db)
def view(c, lf=False):
    pass
