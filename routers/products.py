from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter()


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int


products = [
    {
        "id": 1,
        "name": "Keyboard",
        "price": 2500,
        "stock": 10,
    },
    {
        "id": 2,
        "name": "Mouse",
        "price": 1200,
        "stock": 20,
    },
]


@router.get("/products", response_model=list[ProductResponse])
def get_products():
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: ProductCreate):
    new_id = max((item["id"] for item in products), default=0) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
    }

    products.append(new_product)

    return new_product


@router.put("/products/{product_id}", response_model=ProductResponse)
def replace_product(product_id: int, product: ProductCreate):
    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:
            updated_product = {
                "id": product_id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
            }

            products[index] = updated_product

            return updated_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    for existing_product in products:
        if existing_product["id"] == product_id:
            update_data = product.model_dump(exclude_unset=True)
            existing_product.update(update_data)

            return existing_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)

            return {"message": "Product deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )
