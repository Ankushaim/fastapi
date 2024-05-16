from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get('/test')
async def root():
    return {'key': 'value'}
