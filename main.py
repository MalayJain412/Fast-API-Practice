# def greet():
#     print("This is Malay")
    
# greet()

###############
# The above code will print in the console, but we want on web page........
###############

# Import necessary modules for FastAPI application
from fastapi import FastAPI,Depends  # FastAPI framework for building APIs
from models import Product   # Import our Pydantic Product model for data validation
from config import session, engine  # Import database session and engine from config
import db_models  # Import SQLAlchemy database models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
# Create FastAPI application instance
# This is the main application object that will handle all HTTP requests
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods=["*"]
)

# Create all database tables based on SQLAlchemy models
# This line ensures that all tables defined in db_models are created in the database
# if they don't already exist. It's called at application startup.
db_models.Base.metadata.create_all(bind=engine)

# Define a simple GET endpoint at the root path "/"
# When someone visits the base URL, this function will be called
@app.get("/")
def greet():
    """
    Root endpoint that returns a simple greeting message.
    This is accessible at: http://localhost:8000/
    """
    return "This is Malay"
#run with uvicorn main

# Sample data: Create a list of Product instances using our Pydantic model
# These are Pydantic models that provide data validation and serialization
# Note: In a real application, this data would typically come from a database
# products=[
#     Product(id=1,name='phone',description='samsung',price='54000.3',quantity=15),
#     Product(id=4,name='Laptop',description='samsung',price='740000',quantity=5),
#     Product(id=3,name="Charger",description="Mobile Charger",price=52,quantity=32)
# ]

#Dependency Injection and fetch from db
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database with product data.
    This function converts Pydantic models to SQLAlchemy models and adds them to the database.
    Only adds data if the table is empty to avoid duplicate entries.
    """
    db = session()  # Create a new SQLAlchemy session for database operations
    
    try:
        # Check if the table already has data to avoid duplicate entries
        existing_count = db.query(db_models.Product).count()
        
        if existing_count > 0:
            print(f"Database already has {existing_count} products. Skipping initialization.")
            db.close()
            return
        
        print("Initializing database with sample data...")
        
        for product in products:
            # Each 'product' is a Pydantic model (from models.Product), not directly compatible with the database
            # We need to convert it to a SQLAlchemy model (db_models.Product) that can be stored in the database
            
            # Step 1: product.model_dump() converts the Pydantic model to a dictionary
            # Example: {'id': 1, 'name': 'phone', 'description': 'samsung', 'price': 54000.3, 'quantity': 15}
            
            # Step 2: ** is the dictionary unpacking operator
            # It takes the dictionary and passes its key-value pairs as keyword arguments
            # So **product.model_dump() becomes: id=1, name='phone', description='samsung', etc.
            
            # Step 3: db_models.Product(**product.model_dump()) creates a SQLAlchemy model instance
            # This is equivalent to: db_models.Product(id=1, name='phone', description='samsung', price=54000.3, quantity=15)
            
            db.add(db_models.Product(**product.model_dump()))  # Add the SQLAlchemy model to the database session
        
        db.commit()  # Commit all changes to the database
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()  # Rollback changes if there's an error
    finally:
        db.close()  # Always close the database session

init_db()

# GET endpoint to retrieve all products
# Returns products list in JSON format
# Accessible at: http://localhost:8000/products
@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    """
    Retrieve all products in the inventory.
    Returns: List of all products in JSON format
    """
    
    db_products = db.query(db_models.Product).all()
    
    return db_products

# GET endpoint with path parameter to retrieve a specific product by ID
# Path parameter {id} captures the ID from the URL
# Accessible at: http://localhost:8000/product/1 (where 1 is the product ID)
@app.get('/products/id/{id}')
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    """
    Retrieve a specific product by its ID.
    Args:
        id (int): The unique identifier of the product
    Returns:
        Product object if found, error message if not found
    """
    
    # for product in products:
    #     if product.id == id:
    #         return product
    
    db_product = db.query(db_models.Product).filter(db_models.Product.id==id).first()
    if db_product:
        return db_product
    return f'Product with id {id} not found, please verify the id, or try by name.'


# @app.get('/products/name/{name}')
# def get_product_by_id(name:str,db:Session=Depends(get_db)):
#     """
#     Retrieve a specific product by its Name.
#     Args:
#         name (str): The unique identifier of the product
#     Returns:
#         Product object if found, error message if not found
#     """
    
#     # for product in products:
#     #     if product.name == name:
#     #         return product
    
#     db_product = db.query(db_models.Product).filter(db_models.Product.name==name).first()
#     if db_product:
#         return db_product
#     return f'Product named {name} not found, please check the name again, or try with id.'


# POST endpoint to add a new product
# Uses Pydantic model for automatic request body validation
# Accessible at: http://localhost:8000/product (with POST method)
@app.post('/products/{id}')
def add_product(product:Product,db:Session=Depends(get_db)):
    """
    Add a new product to the inventory.
    Args:
        product (Product): Product data in request body, validated by Pydantic model
    Returns:
        The newly added product
    """
    
    # products.append(product)  # Add the validated product to our in-memory list
    
    db.add(db_models.Product(**product.model_dump()))
    db.commit()
    return product

# PUT endpoint to update an existing product
# Requires both ID parameter and product data in request body
# Accessible at: http://localhost:8000/product?id=1 (with PUT method)
@app.put('/products/{id}')
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    """
    Update an existing product by ID.
    Args:
        id (int): ID of the product to update (query parameter)
        product (Product): New product data (request body)
    Returns:
        Success/failure message
    """
    # for i in range(len(products)):
    #     if products[i].id==id:
    #         products[i] = product
    #         return "Product added successfully"
        
    #     return "Failed to update"
    
    db_product = db.query(db_models.Product).filter(db_models.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return f"Information for product id: {id} and name: {product.name} updated"
    else:
        return f"No product with id {id} found"

# DELETE endpoint to remove a product by ID
# Uses query parameter to specify which product to delete
# Accessible at: http://localhost:8000/product/del_id?id=1 (with DELETE method)
@app.delete('/products/del_id/{id}')
def delete_product_from_id(id:int,db:Session=Depends(get_db)):
    """
    Delete a product from inventory using its ID.
    Args:
        id (int): ID of the product to delete (query parameter)
    Returns:
        Success message if deleted, error message if not found
    """
    # for i in range(len(products)):
    #     if products[i].id==id:
    #         del products[i]
    #         return f"Item with id:{id} deleted successfully."
    #     return 'Product not found in the inventory, please check the id again.'
    
    db_product = db.query(db_models.Product).filter(db_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return f"Product with id {id} deleted successfully."
    else:
        return f"Product Not found, please check the {id} again"    
    
# # DELETE endpoint to remove a product by name
# # Uses query parameter to specify which product to delete by name
# # Accessible at: http://localhost:8000/product/del_name?name=phone (with DELETE method)
# @app.delete('/products/del_name/{name}')
# def delete_product_from_name(name:str,db:Session=Depends(get_db)):
#     """
#     Delete a product from inventory using its name.
#     Args:
#         name (str): Name of the product to delete (query parameter)
#     Returns:
#         Success message if deleted, error message if not found
#     """
#     # for i in range(len(products)):
#     #     if products[i].name==name:
#     #         del products[i]
#     #         return f"Item with named {name} deleted successfully."
#     #     return 'Product not found in the inventory, please check the name again.'
    
    
#     db_product = db.query(db_models.Product).filter(db_models.Product.name==name).first()
#     if db_product:
#         db.delete(db_product)
#         db.commit()
#         return f'Product named {name} deleted successfully'
#     else:
#         return f'There is no product named {name}, please try with id or check the name again.'
#     pass
    
