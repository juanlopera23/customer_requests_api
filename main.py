from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

next_id = 0

items = []

class ItemUser (BaseModel):

    name: str
    email : EmailStr
    message : str

class ItemServer (BaseModel):

    id: int
    name: str
    email : EmailStr
    message : str


@app.get("/")

async def root ():

    return {"message" : "hello world"}

@app.post("/requests", status_code= 201)
async def create_request (item_user : ItemUser):

    global next_id
    

    item = ItemServer(
        id = next_id,
        name= item_user.name,
        email = item_user.email,
        message = item_user.message
    )

    items.append(item)
    next_id += 1
    return item

@app.get("/requests")
async def list_requests ():

    return items

@app.get("/requests/{request_id}")
async def search_request (request_id : int):

    search = None

    for request in items:

        if request.id == request_id:

            search = request
    if search == None :
        raise HTTPException(
            status_code= 404,
            detail= "The item doesn't exist"
        )
    else:
        return search

@app.delete("/requests/{request_id}")
async def delete_item (request_id : int):

    
    for request in items:
    
        if request.id == request_id:

            items.remove(request)
            return items 
           

    raise HTTPException(
        status_code= 404,
        detail= "The item doesn't exist"
    )
    
    