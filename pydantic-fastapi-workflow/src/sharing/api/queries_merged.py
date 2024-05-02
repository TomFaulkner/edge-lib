from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter
from uuid import UUID

INSERT_PROTAG_INIT_QUERY = r"""
select (insert Protagonist {
    name := <str>$name
}) {
    id
};
"""
class InsertProtagInitInput(BaseModel):
    name: str


class InsertProtagInitResult(BaseModel):
    id: UUID


insert_protag_init_adapter = TypeAdapter(InsertProtagInitResult)


async def insert_protag_init(
    executor: AsyncIOExecutor,
    *,
    input: InsertProtagInitInput,
) -> InsertProtagInitResult:
    resp = await executor.query_single_json(
        INSERT_PROTAG_INIT_QUERY,
        **input.model_dump(exclude_unset=True),
    )
    return insert_protag_init_adapter.validate_json(resp, strict=False)