from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
  return "Hello world!"

@app.get('/movies')
def movies():
  return {'movies':{'movie1','movie2'}}