import edgedb


async def test_edgedb_fixture(tx):
    result = await tx.query("select Account;")
    assert isinstance(result, edgedb.Set)
