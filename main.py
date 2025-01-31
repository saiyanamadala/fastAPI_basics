from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
  return "Hello world!"

@app.get('/movies')
def movies():
  return {'movies':{'movie1','movie2'}}

@app.get('/property/{id}')
def property(id:int):
  return f'This is the page of property - {id}'

@app.get('/name/{username}')
def name(username:str):
  return f'username-{username}'