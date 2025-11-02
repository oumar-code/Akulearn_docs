from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Aku DaaS Mock')

class QueryRequest(BaseModel):
    query: str

@app.post('/query')
def query(req: QueryRequest):
    # Return a simple mocked response for demo purposes
    return {
        'type':'table',
        'columns':['date','value'],
        'rows':[["2025-01-01", 42],["2025-01-02", 37]]
    }

if __name__=='__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8090)
