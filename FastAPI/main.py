from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Similar to Models

class Tea(BaseModel):
    id : int
    name : str 
    origin : str 

teas:List[Tea] = []

# / -> Welcome to Tea house

@app.get('/')
def read_root():
    return {"Message","Welcome to Tea House"}

@app.get('/teas')
def getTeas():
    return teas

@app.post('/teas')
def add_tea(tea : Tea):
    teas.append(tea)
    return "Tea added"

@app.put('/teas/{tea_id}')
def updatetea(tea_id : int , newtea : Tea):
    for index , tea in teas :
        if (tea.id == tea_id):
            tea[index] = newtea
            return newtea
        return {"Error" : "Error Occured"}
    
@app.delete('/teas/{tea_id}')
def deletetea(tea_id : int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            deleted_tea = teas.pop(index)
            return {"Message": f"Tea with id {tea_id} deleted"}
    return {"Error": "Tea not found"}

