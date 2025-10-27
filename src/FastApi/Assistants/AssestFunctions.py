from fastapi import Request

async def get_mongo_db_collections_names(request: Request):
    # request.app.mongo_db is the Database object
    return await request.app.mongo_db.list_collection_names()