from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
  return "Hello world!"

@app.get('/movies')
def movies():
  return {'movies':{'movie1','movie2'}}

@app.get('/property')
def property(id:int,name:str=None):            #name=None is defualt query parameter; name is replcaed if certain value is provided
  return f'This is the page of property - {id} and name - {name}'

@app.get('/name/{username}')
def name(username:str):
  return f'username-{username}'