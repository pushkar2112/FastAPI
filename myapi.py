from fastapi import FastAPI
# We run our web server using uvicorn
# uvicorn myapi:app --reload # Command to run the uvicorn server
# AutoGenerated docs at /docs

app = FastAPI() # Create a FastAPI instance

# Endpoint methods
# GET - GET INFO
# POST - CREATE SOMETHING NEW
# PUT - UPDATE
# DELETE - DELETE SOMETHING 

# Create new endpoint for home page
@app.get("/")
def index():
    return {"name": "First Data"}
