from app.product.models import Product, ProductInBranch, ProductVariant, ProductVariantInBranch
from app.order.models import Order, OrderItem
from app.utils.request_utils import response
from fastapi import APIRouter, Depends, Request, Response
from app.db.db import db
from app.schema.schemas import order_serializer, order_item_serializer, product_serializer, product_in_branch_serializer, product_variant_serializer, product_variant_in_branch_serializer, category_serializer, category_update_serializer
from bson import ObjectId
from app.product.models import Category
from app.utils.perms_utils import verify_super_admin
from app.utils.jwt_utils import verify_jwt_token

router = APIRouter()

orders_col = db["orders"]
order_items_col = db["order_items"]
products_col = db["products"]
product_in_branch_col = db["product_in_branch"]
product_variant_col = db["product_variant"]
product_variant_in_branch_col = db["product_variant_in_branch"]
category_col = db["category"]

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        return verify_jwt_token(token)
    else:
        return None
    
def has_perm(action: str):
    return True

@router.get("/", response_description="Get all orders")
async def get_products(page: int = 1, limit: int = 10, current_user: any = Depends(get_current_user)):
    can_read_orders = has_perm("read_orders")
    return response(status_code=200, message="Products retrieved successfully", data={"products": [], "page": page, "limit": limit})
    # try:
    #     skip = (page - 1) * limit
    #     find_all_products = products_col.find().skip(skip).limit(limit)
    #     find_all_products = [product_serializer(product) for product in find_all_products]
    #     return response(status_code=200, message="Products retrieved successfully", data={"products": find_all_products, "page": page, "limit": limit})
    # except Exception as e:
    #     return response(status_code=500, message=str(e))
    
@router.post("/", response_description="Create a new order")
async def create_product(product: Product):
    try:
        product_id = products_col.insert_one(product.dict()).inserted_id
        return response(status_code=200, message="Product created successfully", data=product_serializer(products_col.find_one({"_id": ObjectId(product_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.get("/{product_id}", response_description="Get a single product")
async def get_product(product_id: str):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if find_product:
            return response(status_code=200, message="Product retrieved successfully", data=product_serializer(find_product))
        else:
            return response(status_code=404, message="Product not found")
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.put("/{product_id}", response_description="Update a product")
async def update_product(product_id: str, product: Product):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        products_col.update_one({"_id": ObjectId(product_id)}, {"$set": product.dict()})
        return response(status_code=200, message="Product updated successfully", data=product_serializer(products_col.find_one({"_id": ObjectId(product_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.delete("/{product_id}", response_description="Delete a product")
async def delete_product(product_id: str):
    try:
        products_col.delete_one({"_id": ObjectId(product_id)})
        return response(status_code=200, message="Product deleted successfully")
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.get("/{product_id}/branches", response_description="Get all product branches")
async def get_product_branches(product_id: str):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        product_in_branch = product_in_branch_col.find({"product_id": product_id})
        product_in_branch = [product_in_branch_serializer(product) for product in product_in_branch]
        return response(status_code=200, message="Product branches retrieved successfully", data=product_in_branch)
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.post("/{product_id}/branches", response_description="Create a new branch product")
async def create_product_branch(product_id: str, product_in_branch: ProductInBranch):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        product_in_branch.product_id = product_id
        product_in_branch_id = product_in_branch_col.insert_one(product_in_branch.dict()).inserted_id
        return response(status_code=200, message="Product branch created successfully", data=product_in_branch_serializer(product_in_branch_col.find_one({"_id": ObjectId(product_in_branch_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.get("/{product_id}/variants", response_description="Get all product variants")
async def get_product_variants(product_id: str):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        product_variants = product_variant_col.find({"product_id": product_id})
        product_variants = [product_variant_serializer(product) for product in product_variants]
        return response(status_code=200, message="Product variants retrieved successfully", data=product_variants)
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.post("/{product_id}/variants", response_description="Create a new product variant")
async def create_product_variant(product_id: str, product_variant: ProductVariant):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        product_variant.product_id = product_id
        product_variant_id = product_variant_col.insert_one(product_variant.dict()).inserted_id
        return response(status_code=200, message="Product variant created successfully", data=product_variant_serializer(product_variant_col.find_one({"_id": ObjectId(product_variant_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    

@router.get("/{product_id}/variants/{variant_id}/branches", response_description="Get all product variant branches")
async def get_product_variant_branches(product_id: str, variant_id: str):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        find_product_variant = product_variant_col.find_one({"_id": ObjectId(variant_id)})
        if not find_product_variant:
            return response(status_code=404, message="Product variant not found")
        product_variant_in_branch = product_variant_in_branch_col.find({"product_id": product_id, "variant_id": variant_id})
        product_variant_in_branch = [product_variant_in_branch_serializer(product) for product in product_variant_in_branch]
        return response(status_code=200, message="Product variant branches retrieved successfully", data=product_variant_in_branch)
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.post("/{product_id}/variants/{variant_id}/branches", response_description="Create a new product variant branch")
async def create_product_variant_branch(product_id: str, variant_id: str, product_variant_in_branch: ProductVariantInBranch):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        find_product_variant = product_variant_col.find_one({"_id": ObjectId(variant_id)})
        if not find_product_variant:
            return response(status_code=404, message="Product variant not found")
        product_variant_in_branch.product_id = product_id
        product_variant_in_branch.variant_id = variant_id
        product_variant_in_branch_id = product_variant_in_branch_col.insert_one(product_variant_in_branch.dict()).inserted_id
        return response(status_code=200, message="Product variant branch created successfully", data=product_variant_in_branch_serializer(product_variant_in_branch_col.find_one({"_id": ObjectId(product_variant_in_branch_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.get("/{product_id}/orders", response_description="Get all product orders")
async def get_product_orders(product_id: str):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        orders = orders_col.find({"product_id": product_id})
        orders = [order_serializer(order) for order in orders]
        return response(status_code=200, message="Product orders retrieved successfully", data=orders)
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.post("/{product_id}/orders", response_description="Create a new product order")
async def create_product_order(product_id: str, order: Order):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        order.product_id = product_id
        order_id = orders_col.insert_one(order.dict()).inserted_id
        return response(status_code=200, message="Product order created successfully", data=order_serializer(orders_col.find_one({"_id": ObjectId(order_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.get("/{product_id}/orders/{order_id}", response_description="Get a single product order")
async def get_product_order(product_id: str, order_id: str):
    try:
        find_product = products_col.find_one({"_id": ObjectId(product_id)})
        if not find_product:
            return response(status_code=404, message="Product not found")
        find_order = orders_col.find_one({"_id": ObjectId(order_id)})
        if find_order:
            return response(status_code=200, message="Product order retrieved successfully", data=order_serializer(find_order))
        else:
            return response(status_code=404, message="Product order not found")
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.get("/category", response_description="Get all categories")
async def get_categories():
    try:
        categories = list(category_col.find())
        # categories = [category_serializer(category) for category in categories]
        return response(status_code=200, message="Categories retrieved successfully", data=categories)
    except Exception as e:
        return response(status_code=500, message=str(e))
    

@router.post("/category", response_description="Create a new category")
async def create_category(category: Category):
    try:
        category = category.dict()
        check_category = category_col.find_one({"name": category["name"]})
        if check_category:
            return response(status_code=409, message="Category already exists")
        category_id = category_col.insert_one(category).inserted_id
        find_category = category_col.find_one({"_id": ObjectId(category_id)})
        print(find_category)
        return response(status_code=200, message="Category created successfully", data=category_serializer(find_category))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.get("/category/{category_id}", response_description="Get a single category")
async def get_category(category_id: str):
    try:
        find_category = category_col.find_one({"_id": ObjectId(category_id)})
        if find_category:
            return response(status_code=200, message="Category retrieved successfully", data=find_category)
        else:
            return response(status_code=404, message="Category not found")
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.put("/category/{category_id}", response_description="Update a category")
async def update_category(category_id: str, category: Category):
    try:
        find_category = category_col.find_one({"_id": ObjectId(category_id)})
        if not find_category:
            return response(status_code=404, message="Category not found")
        category_col.update_one({"_id": ObjectId(category_id)}, {"$set": category})
        return response(status_code=200, message="Category updated successfully", data=category_col.find_one({"_id": ObjectId(category_id)}))
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.delete("/category/{category_id}", response_description="Delete a category")
async def delete_category(category_id: str):
    try:
        category_col.delete_one({"_id": ObjectId(category_id)})
        return response(status_code=200, message="Category deleted successfully")
    except Exception as e:
        return response(status_code=500, message=str(e))
    
