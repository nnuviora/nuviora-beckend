from pydantic import BaseModel, Field
from typing import Optional, List


class CategorySchema(BaseModel):
    category_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class SubCategorySchema(BaseModel):
    subcategory_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class TraitsSchema(BaseModel):
    trait_id: Optional[int] = Field(default=None)
    traits_name: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class ProductImageSchema(BaseModel):
    product_image_id: Optional[int] = Field(default=None)
    image_description: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class FeatureSchema(BaseModel):
    feature_id: Optional[int] = Field(default=None)
    feature_name: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    review_id: Optional[int] = Field(default=None)
    rating: Optional[int] = Field(default=None)
    review_text: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    user_id: Optional[int] = Field(default=None)

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    product_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    small_description: Optional[str] = Field(default=None)
    traits: Optional[List[TraitsSchema]] = Field(default=None)
    price: Optional[float] = Field(default=None)
    availability: Optional[bool] = Field(default=None)
    currency: Optional[str] = Field(max_length=10)
    in_stock: Optional[bool] = Field(default=None)
    category: Optional[CategorySchema] = Field(default=None)
    subcategory: Optional[SubCategorySchema] = Field(default=None)
    product_images: Optional[List[ProductImageSchema]] = Field(default=None)
    
    features: Optional[List[FeatureSchema]] = Field(default=None)
    reviews: Optional[List[ReviewSchema]] = Field(default=None)
    
    class Config:
        from_attributes = True