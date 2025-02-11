from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List
from uuid import UUID
from datetime import date, timedelta, datetime, time
import strawberry
from strawberry.fastapi import GraphQLRouter

class Event(BaseModel):
  event_id: UUID
  start_date: date
  start_time: datetime
  end_time: datetime
  repeat_time: time
  execute_after: timedelta

class Profile(BaseModel):
  name: str
  email: str
  age: int

class Image(BaseModel):
  name: str
  url: HttpUrl

class Product(BaseModel):
  name: str
  price: int = Field(title="price of item", description="This is the item price", gt=0)  #Field is used to define the Metadata and this metadata can be seen in the swagger UI
  discount: int
  discounted_price: float
  tags: Set[str]=[]    #Set of string type
  image: List[Image]    #Nested pydantic model

class Offer(BaseModel):
  name: str = Field(example="Apple Pay Discount")  #shows example value in the documentation
  description: str
  price: float
  prouducts: List[Product]

class User(BaseModel):
  name: str
  email: str

  class Config:           # This shows the example data in the documentation
    schema_extra={
      "example": {
        "name": "Sairam",
        "email": "sai@gmail.com"
      }
    }

app = FastAPI()

@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):   #Form() is used to accept the field value as form in the documentation
  return username

@app.post('/addEvent')
def addEvent(event: Event):
  return event

@app.post('/addOffer')
def addOrder(offer:Offer):
  return offer

@app.post('/purchase')
def purchase(user:User, product:Product):
  return {"user":user, "product": product}

@app.post('/addProduct/{product_id}')
def addProduct(product:Product, product_id:int, category:str):
  product.discounted_price=product.price-(product.price*product.discount)/100
  return {"product_id" : product_id, "product" : product, "category": category}

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

@app.post('/profile')
def profile(profile:Profile):
  return profile

# ------------------ GraphQL Implementation ------------------

# Define GraphQL types
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, GraphQL!"

    @strawberry.field
    def get_movies(self) -> List[str]:
        return ["Movie1", "Movie2", "Movie3"]

    @strawberry.field
    def get_product(self, name: str) -> str:
        return f"Product: {name}"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, name: str, price: int) -> str:
        return f"Product {name} created with price {price}"

# Create Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Add GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")