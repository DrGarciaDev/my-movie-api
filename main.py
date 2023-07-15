from fastapi import FastAPI

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

@app.get(path='/', tags=['Home'])
def message():
    return "Hello world"