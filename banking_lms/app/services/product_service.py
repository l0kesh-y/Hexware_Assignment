from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.exceptions.custom_exceptions import ProductNotFoundException

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.db = db
    
    def create_product(self, product: ProductCreate):
        try:
            return self.repository.create_product(product)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_product(self, product_id: int):
        product = self.repository.get_product(product_id)
        if not product:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return product
    
    def get_all_products(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_products(skip, limit)
    
    def update_product(self, product_id: int, product_data: ProductUpdate):
        product = self.repository.get_product(product_id)
        if not product:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        
        try:
            return self.repository.update_product(product_id, product_data)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_product(self, product_id: int):
        product = self.repository.get_product(product_id)
        if not product:
            raise ProductNotFoundException(f"Product with id {product_id} not found")
        return self.repository.delete_product(product_id)
