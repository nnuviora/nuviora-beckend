from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, and_, or_

from database import get_db
from schemas.product_schema import (
    FeatureSchema,
    ProductCardSchema, 
    ProductDetailSchema,
    ProductImageSchema, 
    ProductSearchSuggestionSchema,
    ProductComparisonSchema,
    ProductRecommendationSchema,
    ProductSubscriptionSchema,
    ProductSubscriptionResponse,
    ProductFiltersSchema,
    ProductCatalogResponse,
    PriceRangeSchema,
    ProductVariationPriceSchema,
    CategorySchema,
    BrandSchema,
    ReviewSchema,
    SubCategorySchema
)
from models.product_model import (
    Product, 
    Category, 
    Subcategory, 
    Brand, 
    Review, 
    ProductImage,
    Feature,
    ProductVariation,
    ProductSubscription
)

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/products/{product_id}")
async def get_product(product_id: int):
    return {"product_id": product_id}

@router.get("/categories/{category_id}")
async def get_category(category_id: int):
    return {"category_id": category_id}

@router.get("/subcategories/{subcategory_id}")
async def get_subcategory(subcategory_id: int):
    return {"subcategory_id": subcategory_id}

@router.get("/products/{product_id}/categories/{category_id}")
async def get_product_category(product_id: int, category_id: int):
    return {"product_id": product_id, "category_id": category_id}

@router.get("/catalog", response_model=ProductCatalogResponse)
async def get_product_catalog(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=100),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_certified: Optional[bool] = None,
    in_stock: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Product).options(
        joinedload(Product.reviews)
    )

    filters = []
    if category:
        filters.append(Product.category.has(name=category))
    if brand:
        filters.append(Product.brand.has(name=brand))
    if min_price:
        filters.append(Product.price >= min_price)
    if max_price:
        filters.append(Product.price <= max_price)
    if is_certified:
        filters.append(Product.is_certified == is_certified)
    if in_stock is not None:
        filters.append(Product.in_stock == in_stock)
    if search:
        filters.append(or_(
            Product.name.ilike(f"%{search}%"),
            Product.small_description.ilike(f"%{search}%")
        ))

    if filters:
        query = query.where(and_(*filters))

    count_stmt = select(func.count(Product.product_id)).where(and_
    (*filters)) if filters else select(func.count(Product.product_id))

    total = await db.execute(count_stmt)
    total_count = total.scalar()

    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    products = result.scalars().all()

    product_cards = []
    for p in products:
        avg_rating = round(sum(r.rating for r in p.reviews) / len(p.reviews), 1) if p.reviews else 0.0
        product_cards.append(ProductCardSchema(
            product_id=p.product_id,
            name=p.name,
            price=p.price,
            currency="UAH",
            average_rating=avg_rating,
            small_description=p.small_description,
            main_image_url=p.image_url,
            category_name=p.category,
            brand_name=p.brand,
            is_certified=p.is_certified,
            in_stock=p.in_stock
        ))

    return ProductCatalogResponse(
        products=product_cards,
        page=page,
        per_page=per_page,
        total_count=total_count,
        total_pages=(total_count + per_page - 1) // per_page,
        has_next=page * per_page < total_count,
        has_prev=page > 1
    ) 
  

@router.get("/search/suggestions", response_model=List[ProductSearchSuggestionSchema])
async def get_product_search_suggestions(search: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Product).where(Product.name.ilike(f"%{search}%")).limit(10)
    result = await db.execute(stmt)
    return [ProductSearchSuggestionSchema(product_id=p.product_id, name=p.name) for p in result.scalars().all()]


@router.post("/compare", response_model=List[ProductComparisonSchema])
async def compare_products(product_id: List[int], db: AsyncSession = Depends(get_db)):
    if len(product_id) < 2:
        raise HTTPException(400, detail="Мінімум 2 товари для порівняння")

    stmt = select(Product).where(Product.product_id.in_(product_id))
    result = await db.execute(stmt)
    return [ProductComparisonSchema.from_orm(p) for p in result.scalars().all()]


""" @router.post("/subscribe", response_model=ProductSubscriptionResponse)
async def subscribe(data: ProductSubscriptionSchema, db: AsyncSession = Depends(get_db)):
    subscription = ProductSubscription(product_id=data.product_id, email=data.email)
    db.add(subscription)
    await db.commit()
    return ProductSubscriptionResponse(message="Підписка оформлена") """


""" @router.get("/{product_id}", response_model=ProductDetailSchema)
async def get_product_detail(product_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Product).options(
        joinedload(Product.images),
        joinedload(Product.reviews),
        joinedload(Product.features)
    ).where(Product.product_id == product_id)

    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(404, detail="Не знайдено")

    return ProductDetailSchema(
        product_id=product.product_id,
        name=product.name,
        description=product.description,
        small_description=product.small_description,
        price=product.price,
        in_stock=product.in_stock,
        stock_quantity=product.stock_quantity,
        benefits=product.benefits,
        usage_instructions=product.usage_instructions,
        certification_info=product.certification_info,
        is_certified=product.is_certified,
        average_rating=round(sum(r.rating for r in product.reviews) / len(product.reviews), 1) if product.reviews else 0.0,
        review_count=len(product.reviews),
        images=[ProductImageSchema.from_orm(img) for img in product.images],
        features=[FeatureSchema.from_orm(f) for f in product.features],
        reviews=[ReviewSchema.from_orm(r) for r in product.reviews],
        variations=[ProductVariationPriceSchema.from_orm(v) for v in product.variations]
    ) """


@router.get("/{product_id}/recommended", response_model=List[ProductRecommendationSchema])
async def get_recommended(product_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Product).where(Product.product_id != product_id).limit(5)
    result = await db.execute(stmt)
    return [ProductRecommendationSchema.from_orm(p) for p in result.scalars().all()]


@router.get("/{product_id}/prices", response_model=List[ProductVariationPriceSchema])
async def get_price_with_variations(
    product_id: int, 
    variation_type: Optional[str] = None,
    variation_value: Optional[str] = None,
    db: AsyncSession = Depends(get_db)):
    stmt = select(ProductVariation).where(ProductVariation.product_id == product_id)

    if variation_type:
        stmt = stmt.where(ProductVariation.variation_type == "flavor")
    if variation_value:
        stmt = stmt.where(ProductVariation.variation_value == "size")

    result = await db.execute(stmt)
    variation = result.scalar_one_or_none()
    if not variation:
        raise HTTPException(404, detail="Варіацію не знайдено")
    
    return ProductVariationPriceSchema.from_orm(variation)