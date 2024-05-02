from fastapi import FastAPI, Request, HTTPException
from .dependency import get_client #  (untested!)
# from .queries_merged import whatever you nammed your generated edgeql files
from .queries_merged import insert_protag_init, InsertProtagInitInput, InsertProtagInitResult
from fastapi import APIRouter

app = FastAPI()

protagonist_router = APIRouter(prefix="/protagonist")


@protagonist_router.put("/update")
async def insert_protag(data: InsertProtagInitInput, client=Depends(get_client)) -> InsertProtagInitResult:
    # don't need this: async with get_client() as client:
        try:
            result = await insert_protag_init(client, input=data)
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def read_root(request: Request):
    return {"message": "Hello!"}


app.include_router(protagonist_router)
