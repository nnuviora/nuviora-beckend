from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from schemas.product_schema import ProductSchema


router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/products/{product_id}", tags=["Product"])
async def get_product(product_id: int):
    return {"product_id": product_id}


@router.get("/categories/{category_id}", tags=["Product"])
async def get_category(category_id: int):
    return {"category_id": category_id}


@router.get("/subcategories/{subcategory_id}", tags=["Product"])
async def get_subcategory(subcategory_id: int):
    return {"subcategory_id": subcategory_id}


@router.get("/products/{product_id}/categories/{category_id}", tags=["Product"])
async def get_product_category(product_id: int, category_id: int):
    return {"product_id": product_id, "category_id": category_id}


