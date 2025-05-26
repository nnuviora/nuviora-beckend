from datetime import datetime
import uuid
from sqlalchemy import Boolean, DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)

    subcategories = relationship("Subcategory", back_populates="category")
    products = relationship("Product", back_populates="category")

    async def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
        }

class Subcategory(Base):
    __tablename__ = "subcategory"

    subcategory_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))

    category: Mapped["Category"] = relationship(back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")

    async def to_dict(self):
        return {
            "subcategory_id": self.subcategory_id,
            "name": self.name,
            "description": self.description,
        }
    
class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    small_description: Mapped[str] = mapped_column(Text)
    traits_id: Mapped[int] = mapped_column(ForeignKey("traits.traits_id"))
    price: Mapped[float] = mapped_column(DECIMAL)
    availability: Mapped[bool] = mapped_column(Boolean)
    currency: Mapped[str] = mapped_column(String(10))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategory.subcategory_id"))
    product_image: Mapped[str] = mapped_column(String)

    category = relationship("Category", back_populates="products")
    subcategory = relationship("Subcategory", back_populates="products")
    traits = relationship("Traits", back_populates="product")
    images = relationship("ProductImage", back_populates="product")
    features = relationship("Feature", back_populates="product")
    reviews = relationship("Review", back_populates="product")

    async def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "small_description": self.small_description,
            "traits_id": self.traits_id,
            "price": self.price,
            "availability": self.availability,
            "currency": self.currency,
            "in_stock": self.in_stock,
            "category_id": self.category_id,
            "subcategory_id": self.subcategory_id,
            "product_image": self.product_image,
        }
    
class Traits(Base):
    __tablename__ = "traits"

    traits_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    traits_name: Mapped[str] = mapped_column(String)
    traits_text: Mapped[str] = mapped_column(Text)

    product: Mapped["Product"] = relationship(back_populates="traits")

    async def to_dict(self):
        return {
            "traits_id": self.traits_id,
            "product_id": self.product_id,
            "traits_name": self.traits_name,
            "traits_text": self.traits_text,
    }

class ProductImage(Base):
    __tablename__ = "product_image"

    product_image_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    image_description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String)

    product: Mapped["Product"] = relationship(back_populates="images")

    async def to_dict(self):
        return {
            "product_image_id": self.product_image_id,
            "product_id": self.product_id,
            "image_description": self.image_description,
            "image_url": self.image_url,
        }

class Feature(Base):
    __tablename__ = "feature"

    feature_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    feature_name: Mapped[str] = mapped_column(String)
    feature_text: Mapped[str] = mapped_column(Text)

    product: Mapped["Product"] = relationship(back_populates="features")

    async def to_dict(self):
        return {
            "feature_id": self.feature_id,
            "product_id": self.product_id,
            "feature_name": self.feature_name,
            "feature_text": self.feature_text,
        }
    
class Review(Base):
    __tablename__ = "review"

    review_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    rating: Mapped[int] = mapped_column(Integer)
    review_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    product: Mapped["Product"] = relationship(back_populates="reviews")

    async def to_dict(self):
        return {
            "review_id": self.review_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "review_text": self.review_text,
            "created_at": self.created_at,
            "user_id": self.user_id
        }