# Importing fastapi
from fastapi import FastAPI

# Creating an instance of the FastAPI class
app = FastAPI()

# Defining a route for the root URL ("/") that returns a simple message
@app.get("/")
# Defining a function that will be called when the root URL is accessed
def read_root(): 
    return {"Message": "Hello World"}

@app.get("/greet")
def greet():
    return {"Message": "Hello, welcome to FastAPI!"}

#Path parameter example
@app.get("/greet/{name}")
def greet_name(name: str, age: int):
    return {"Message": f"Hello {name}, you are {age} years old!"}

# Query parameter example
@app.get("/greet/query")
def greet_query(name: str):
    return {"Message": f"Hello {name}"}