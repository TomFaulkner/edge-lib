#!/usr/bin/env python3

import test

from invoke import Collection, task


@task
def edge(c):
    c.run(
        """
    edgedb-py --target async --file
    edgedb-py --target blocking --no-skip-pydantic-validation --file
    cp generated_async_edgeql.py src/ca/data/queries_async.py
    cp generated_edgeql.py src/ca/data/queries_blocking.py
    poetry install
    python edge_model_gen.py
    echo import pydantic > pd_import
    cat pd_import generated_async_edgeql.py models.py > src/ca/data/queries_async.py && rm generated_async_edgeql.py
    cat pd_import generated_edgeql.py models.py > src/ca/data/queries_blocking.py && rm generated_edgeql.py models.py
    isort --float-to-top src/ca/data/queries_async.py src/ca/data/queries_blocking.py
    python edge_dataclass_to_pydantic.py
    black src/ca/data/queries_async.py src/ca/data/queries_blocking.py
    rm pd_import
    """  # noqa E501: line too long
    )


namespace = Collection(edge, )
