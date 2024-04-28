import os
from contextlib import suppress

import edgedb
import pytest


class RollbackTransaction(Exception):
    """Just here to rollback edgedb transactions."""


def _create_db():
    creation_db_client = edgedb.create_client()
    try:
        with suppress(edgedb.errors.UnknownDatabaseError):
            _drop_db()
        creation_db_client.execute("CREATE DATABASE _test;")
    finally:
        creation_db_client.close()
        del creation_db_client
    edgedb.create_client(database="_test").query("select 3.14")


def _drop_db():
    try:
        db_client = edgedb.create_client()
        db_client.execute("DROP DATABASE _test")
    finally:
        db_client.close()


def _migrate_db():
    try:
        db_client = edgedb.create_client()
        for migration_file in os.listdir("dbschema/migrations"):
            with open("dbschema/migrations/" + migration_file) as f:
                migration_body = f.read()
                db_client.execute(migration_body)
    finally:
        db_client.close()


@pytest.fixture
def settings():
    from ca.depends import get_settings

    return get_settings()


@pytest.fixture
async def tx():
    with suppress(RollbackTransaction):
        try:
            client = edgedb.create_async_client()
            async for tx in client.transaction():
                async with tx:
                    yield tx
            raise RollbackTransaction()
        finally:
            with suppress(Exception):
                await client.aclose()


@pytest.fixture
def app():
    from ca.main import get_app

    return get_app()


@pytest.fixture
async def customer(tx):
    from ca.svc.customer import register

    return await register(tx)


_user = {"username": "tester", "first_name": "Scott", "last_name": "Adams"}


@pytest.fixture
async def user(customer, settings, tx):
    from ca.data.user.register_user_async_edgeql import register_user
    from ca.lib.passwords import hash_pw

    user_ = _user | {"customer": customer["id"]}
    passwd = hash_pw("password", settings).encode()
    return await register_user(tx, password_hash=passwd, **user_)


@pytest.fixture
async def customer_account(tx):
    from ca.data.queries_async import customer_add

    return await customer_add(tx, name="Great Customer")


@pytest.fixture
async def account_checking(tx, customer_account):
    from ca.svc import account

    return await account.create(
        tx,
        **{
            "account_type": "Cash",
            "name": "Checking",
            "customer": customer_account.id,
            "is_parent": False,
            "is_child": False,
        },
    )
