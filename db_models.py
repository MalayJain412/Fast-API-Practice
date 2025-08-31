"""
SQLAlchemy Database Models

This file defines database table structures using SQLAlchemy ORM.
Unlike Pydantic models (which handle data validation), SQLAlchemy models:
1. Define actual database table schemas
2. Handle database operations (CRUD)
3. Manage relationships between tables
4. Provide database-specific features (indexes, constraints, etc.)
"""

# Import SQLAlchemy components for database modeling
from sqlalchemy.ext.declarative import declarative_base  # Base class for all models
from sqlalchemy import Column, Integer, String, Float    # Column types for table definition

# Create base class for all database models
# All SQLAlchemy models inherit from this Base class
# This base tracks model metadata and enables table creation
Base = declarative_base()

class Product(Base):
    """
    SQLAlchemy model representing the 'product' table in the database.
    
    This model defines:
    - Table name and structure
    - Column types and constraints
    - Primary keys and indexes
    - Database-specific configurations
    
    Differences from Pydantic Product model:
    - This creates actual database tables
    - Handles database operations and queries
    - Includes database-specific features (indexes, foreign keys, etc.)
    - Used for ORM operations (create, read, update, delete)
    """
    
    # Define the table name in the database
    __tablename__ = 'product'
    
    # Define table columns with their types and constraints
    id = Column(Integer, primary_key=True, index=True)  # Primary key with automatic indexing
    name = Column(String(255))        # Product name (max 255 characters for MySQL compatibility)
    description = Column(String(255)) # Product description (max 255 characters)
    price = Column(Float)             # Product price (floating point number)
    quantity = Column(Integer)        # Available quantity (integer)
    
    # Column explanations:
    # - primary_key=True: Makes this column the unique identifier
    # - index=True: Creates database index for faster lookups
    # - String(255): MySQL requires length specification for VARCHAR columns
    # - Float: Allows decimal numbers for pricing
    # - Integer: Whole numbers for quantities and IDs
