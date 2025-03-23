# E-Commerce RESTful API  

## Overview  
This is a production-ready RESTful API for an e-commerce platform that allows users to:  
- View available products  
- Add new products  
- Place orders with stock validation  

## Technologies Used  
- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- Docker  

## Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/sshubham17/assignement.git
cd e-commerce-api
```

### 2. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3. Run the Application  
```bash
uvicorn main:app --reload
```

### 4. Run with Docker  
```bash
sudo docker build -t my-fastapi-app .
sudo docker run -p 8000:80 my-fastapi-app
```

## API Endpoints  
- **POST api/v1/setup -> create database
- **GET api/v1/products** → Retrieve all products  
- **POST api/v1/products** → Add a new product  
- **POST api/v1/orders** → Place an order  

## Sample curl URL
# Create database
curl --location --request POST 'http://127.0.0.1:8000/api/v1/setup'

# Retrieve all products
curl --location 'http://127.0.0.1:8000/api/v1/products' \
     --header 'domain: zesto'

# Add a new product
curl --location 'http://127.0.0.1:8000/api/v1/products' \
     --header 'domain: zesto' \
     --header 'Content-Type: application/json' \
     --data '{
         "name": "Laptop",
         "description": "A high-performance laptop",
         "price": 1200.50,
         "stock": 10
     }'

# Place an order
curl --location 'http://127.0.0.1:8000/api/v1/orders' \
     --header 'domain: zesto' \
     --header 'Content-Type: application/json' \
     --data '{
         "products": [
             {
                 "product_id": 1,
                 "quantity": 2
             }
         ],
         "total_price": 2401.00,
         "status": "pending"
     }'


## Author  
Shubham Chincholkar  
