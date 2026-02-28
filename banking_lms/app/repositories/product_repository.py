from sqlalchemy.orm import Session
from app.models.loan_product import LoanProduct
from app.schemas.product_schema import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(self, product: ProductCreate):
        db_product = LoanProduct(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def get_product(self, product_id: int):
        return self.db.query(LoanProduct).filter(LoanProduct.id == product_id).first()
    
    def get_all_products(self, skip: int = 0, limit: int = 10):
        return self.db.query(LoanProduct).offset(skip).limit(limit).all()
    
    def update_product(self, product_id: int, product_data: ProductUpdate):
        db_product = self.get_product(product_id)
        if db_product:
            for key, value in product_data.model_dump(exclude_unset=True).items():
                setattr(db_product, key, value)
            self.db.commit()
            self.db.refresh(db_product)
        return db_product
    
    def delete_product(self, product_id: int):
        db_product = self.get_product(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
        return db_product
