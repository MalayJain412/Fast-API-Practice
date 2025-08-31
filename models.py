"""
Pydantic Models for Data Validation and Serialization

This file defines data models using Pydantic, which provides:
1. Automatic data validation for incoming requests
2. JSON serialization/deserialization
3. Type hints and documentation
4. Error handling for invalid data
"""

from pydantic import BaseModel # Pydantic's BaseModel for data validation and serialization

class Product(BaseModel):
    """
    Pydantic model for Product data validation.
    
    This model is used for:
    - Validating incoming JSON data in API requests
    - Serializing Python objects to JSON responses
    - Providing type hints and automatic documentation
    - Converting between different data formats
    
    All fields are required unless marked as Optional.
    Pydantic automatically validates data types and raises errors for invalid data.
    """
# class Product():  # Old approach without validation
    id: int          # Product unique identifier (must be integer)
    name: str        # Product name (must be string)
    description: str # Product description (must be string)
    price: float     # Product price (must be float/number)
    quantity: int    # Available quantity (must be integer)
    
    ### Legacy approach without Pydantic (commented out)
    # Before using Pydantic BaseModel, we had to manually define __init__ method
    # and handle data validation ourselves. Pydantic automates all of this.
    
    # def __init__(self,id:int,name:str,description:str,price:float,quantity:int):
    #     """
    #     Manual constructor that we used before Pydantic.
    #     With BaseModel, this is automatically generated with validation.
    #     """
    #     self.id=id
    #     self.name=name
    #     self.description=description
    #     self.price=price
    #     self.quantity=quantity
    
    # Benefits of using Pydantic BaseModel over manual class:
    # 1. Automatic type validation (ensures id is int, name is str, etc.)
    # 2. JSON serialization with .model_dump() method
    # 3. JSON deserialization from dictionaries
    # 4. Better error messages for invalid data
    # 5. Integration with FastAPI for automatic API documentation
    # 6. Support for complex validation rules and custom validators

