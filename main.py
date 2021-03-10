from fastapi import FastAPI
import requests
from os import environ
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Node(BaseModel):
    id:int
    message: str

class Nodes(BaseModel):
    items:Optional[List[Node]]

@app.post("/", response_model=Nodes)
def find_nodes(nodes: Nodes):
    next_url = environ.get('NEXT')
    nodes.items = nodes.items or [] # Except None
    this_node = Node(id=len(nodes.items), message=next_url or "It's last one")
    nodes.items.append(this_node)
    if next_url == None:
        return nodes
    else:
        try:
            resp = requests.post("http://%s" % next_url, data=nodes.dict())
            resp_json = resp.json()
            nodes = Nodes(**resp_json)
            return nodes
        except Exception as e:
            this_node.message = "%s failed:%s" % (next_url, e)
            return nodes

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host='0.0.0.0', port=8080)
