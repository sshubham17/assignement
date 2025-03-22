from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.dto import Response
from app.utils.decorators.logging_api_request import log_api_requests
from app.utils.dependencies import get_db
from app.database.db_table_orm_models import Product, Order, OrderItem
from app.dto.product_schema import ProductCreate, ProductResponse
from app.dto.order_schema import OrderCreate, OrderResponse
from app.utils.logger import logger


@log_api_requests
async def get_products(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Product))
        products = result.scalars().all()

        # Convert ORM objects to Pydantic response models
        serialized_products = [
            ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock
            )
            for product in products
        ]

        return Response(data=serialized_products, message="Products retrieved successfully", status_code=200)

    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving products")



@log_api_requests
async def create_product(request: Request, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_product = Product(**product.dict())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)

        product = ProductResponse(
            id=new_product.id,
            name=new_product.name,
            description=new_product.description,
            price=new_product.price,
            stock=new_product.stock
        )

        logger.info(f"Product '{product.name}' created successfully")

        return Response(data=product, message="Product created successfully", status_code=201)

    except IntegrityError:
        logger.error("Duplicate entry or database constraint violation")
        raise HTTPException(status_code=400, detail="Duplicate entry or constraint violation")

    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the product")


@log_api_requests
async def create_order(request: Request, order: OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        total_price = 0
        order_items = []

        for item in order.products:
            product = await db.get(Product, item.product_id)
            if not product or product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock or invalid product ID: {item.product_id}")

            product.stock -= item.quantity
            total_price += product.price * item.quantity

            order_items.append(OrderItem(product_id=item.product_id, quantity=item.quantity))

        # Create new Order
        new_order = Order(total_price=total_price, status="COMPLETED", order_items=order_items)
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        # Serialize response
        order_response = OrderResponse(
            id=new_order.id,
            total_price=new_order.total_price,
            status=new_order.status.value
        )

        logger.info(f"Order {new_order.id} created successfully with total price {total_price}")
        return Response(data=order_response, message="Order created successfully", status_code=201)

    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the order")

